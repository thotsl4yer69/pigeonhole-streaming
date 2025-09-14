#!/usr/bin/env python3
"""
Pigeonhole Fleet Monitoring System
Real-time monitoring and management for Fire TV fleet
"""

import asyncio
import json
import logging
import sqlite3
import subprocess
import time
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import aiohttp
import psutil
from prometheus_client import Counter, Gauge, Histogram, start_http_server

# Configuration
CONFIG_FILE = Path("/opt/pigeonhole/config/fleet-config.yaml")
DB_FILE = Path("/opt/pigeonhole/data/fleet.db")
LOG_FILE = Path("/var/log/pigeonhole/fleet-monitor.log")

# Prometheus metrics
device_status = Gauge('firetv_device_status', 'Device online status', ['device_id', 'model'])
device_temperature = Gauge('firetv_device_temperature', 'Device temperature in Celsius', ['device_id'])
device_cpu_usage = Gauge('firetv_device_cpu_usage', 'Device CPU usage percentage', ['device_id'])
device_memory_usage = Gauge('firetv_device_memory_usage', 'Device memory usage percentage', ['device_id'])
device_storage_usage = Gauge('firetv_device_storage_usage', 'Device storage usage percentage', ['device_id'])
kodi_status = Gauge('kodi_status', 'Kodi running status', ['device_id'])
vpn_status = Gauge('vpn_status', 'VPN connection status', ['device_id'])
deployment_counter = Counter('deployment_operations_total', 'Total deployment operations', ['device_id', 'operation', 'status'])

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class FireTVDevice:
    """Represents a Fire TV device in the fleet"""
    
    def __init__(self, device_id: str, ip_address: str, model: str):
        self.device_id = device_id
        self.ip_address = ip_address
        self.model = model
        self.last_seen = datetime.now()
        self.status = "unknown"
        self.metrics = {}
        
    def update_metrics(self, metrics: Dict):
        """Update device metrics"""
        self.metrics.update(metrics)
        self.last_seen = datetime.now()
        
    def is_online(self) -> bool:
        """Check if device is considered online"""
        return (datetime.now() - self.last_seen).seconds < 300  # 5 minutes

class FleetMonitor:
    """Main fleet monitoring class"""
    
    def __init__(self):
        self.devices: Dict[str, FireTVDevice] = {}
        self.config = self.load_config()
        self.db_connection = None
        self.running = False
        
    def load_config(self) -> Dict:
        """Load configuration from YAML file"""
        try:
            with open(CONFIG_FILE, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {}
    
    def init_database(self):
        """Initialize SQLite database for fleet data"""
        self.db_connection = sqlite3.connect(str(DB_FILE), check_same_thread=False)
        cursor = self.db_connection.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS devices (
                device_id TEXT PRIMARY KEY,
                ip_address TEXT,
                model TEXT,
                first_seen TIMESTAMP,
                last_seen TIMESTAMP,
                status TEXT,
                firmware_version TEXT,
                kodi_version TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT,
                timestamp TIMESTAMP,
                metric_name TEXT,
                metric_value REAL,
                FOREIGN KEY (device_id) REFERENCES devices (device_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT,
                timestamp TIMESTAMP,
                event_type TEXT,
                event_data TEXT,
                FOREIGN KEY (device_id) REFERENCES devices (device_id)
            )
        ''')
        
        self.db_connection.commit()
        logger.info("Database initialized successfully")
    
    async def discover_devices(self) -> List[Tuple[str, str]]:
        """Discover Fire TV devices on the network"""
        logger.info("Starting device discovery...")
        discovered = []
        
        # ADB device discovery
        try:
            result = subprocess.run(['adb', 'devices', '-l'], 
                                  capture_output=True, text=True, timeout=10)
            for line in result.stdout.split('\n'):
                if 'device' in line and ('AFTMM' in line or 'AFTBK' in line or 
                                       'AFTKA' in line or 'AFTGAZL' in line):
                    parts = line.split()
                    ip_address = parts[0]
                    if ':5555' in ip_address:
                        ip_address = ip_address.replace(':5555', '')
                    discovered.append((ip_address, 'unknown'))
        except Exception as e:
            logger.error(f"ADB discovery failed: {e}")
        
        # Network scan for additional devices
        network_range = self.config.get('deployment', {}).get('discovery_range', '192.168.1.0/24')
        try:
            result = subprocess.run(['nmap', '-sn', network_range], 
                                  capture_output=True, text=True, timeout=30)
            # Parse nmap output for Fire TV devices
            lines = result.stdout.split('\n')
            current_ip = None
            for line in lines:
                if 'Nmap scan report for' in line:
                    current_ip = line.split()[-1].strip('()')
                elif current_ip and 'amazon' in line.lower():
                    discovered.append((current_ip, 'amazon'))
        except Exception as e:
            logger.error(f"Network discovery failed: {e}")
        
        logger.info(f"Discovered {len(discovered)} potential Fire TV devices")
        return discovered
    
    async def get_device_info(self, ip_address: str) -> Optional[Dict]:
        """Get device information via ADB"""
        device_address = f"{ip_address}:5555"
        
        try:
            # Connect to device
            subprocess.run(['adb', 'connect', device_address], 
                         capture_output=True, timeout=10)
            
            # Get device properties
            result = subprocess.run(['adb', '-s', device_address, 'shell', 'getprop'],
                                  capture_output=True, text=True, timeout=15)
            
            if result.returncode != 0:
                return None
            
            # Parse properties
            props = {}
            for line in result.stdout.split('\n'):
                if ': [' in line:
                    key, value = line.split(': [', 1)
                    key = key.strip('[]')
                    value = value.rstrip(']')
                    props[key] = value
            
            return {
                'device_id': props.get('ro.serialno', 'unknown'),
                'model': props.get('ro.product.model', 'unknown'),
                'android_version': props.get('ro.build.version.release', 'unknown'),
                'firmware_version': props.get('ro.build.version.name', 'unknown'),
                'ip_address': ip_address
            }
            
        except Exception as e:
            logger.debug(f"Failed to get device info for {ip_address}: {e}")
            return None
    
    async def get_device_metrics(self, device: FireTVDevice) -> Dict:
        """Collect device performance metrics"""
        device_address = f"{device.ip_address}:5555"
        metrics = {}
        
        try:
            # CPU usage
            result = subprocess.run(['adb', '-s', device_address, 'shell', 
                                   'top -n 1 | grep "CPU:"'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                cpu_line = result.stdout.strip()
                # Parse CPU usage from top output
                if 'user' in cpu_line:
                    parts = cpu_line.split()
                    for i, part in enumerate(parts):
                        if part.endswith('%') and i > 0:
                            if 'user' in parts[i-1] or 'sys' in parts[i-1]:
                                cpu_usage = float(part.rstrip('%'))
                                metrics['cpu_usage'] = cpu_usage
                                break
            
            # Memory usage
            result = subprocess.run(['adb', '-s', device_address, 'shell', 
                                   'cat /proc/meminfo'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                mem_info = {}
                for line in result.stdout.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        value = value.strip().split()[0]  # Remove 'kB' unit
                        try:
                            mem_info[key] = int(value)
                        except ValueError:
                            pass
                
                if 'MemTotal' in mem_info and 'MemAvailable' in mem_info:
                    total = mem_info['MemTotal']
                    available = mem_info['MemAvailable']
                    used = total - available
                    memory_usage = (used / total) * 100
                    metrics['memory_usage'] = memory_usage
            
            # Storage usage
            result = subprocess.run(['adb', '-s', device_address, 'shell', 'df /data'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) >= 2:
                    data_line = lines[-1].split()
                    if len(data_line) >= 5:
                        usage_percent = data_line[4].rstrip('%')
                        try:
                            metrics['storage_usage'] = float(usage_percent)
                        except ValueError:
                            pass
            
            # Temperature
            temp_files = [
                '/sys/class/thermal/thermal_zone0/temp',
                '/sys/devices/system/cpu/cpu0/cpufreq/cpu_temp',
                '/sys/class/hwmon/hwmon0/temp1_input'
            ]
            
            for temp_file in temp_files:
                result = subprocess.run(['adb', '-s', device_address, 'shell', f'cat {temp_file}'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    try:
                        temp = float(result.stdout.strip())
                        if temp > 1000:  # Convert millidegrees to degrees
                            temp = temp / 1000
                        if 10 <= temp <= 100:  # Reasonable temperature range
                            metrics['temperature'] = temp
                            break
                    except ValueError:
                        continue
            
            # Check Kodi status
            result = subprocess.run(['adb', '-s', device_address, 'shell', 
                                   'ps | grep kodi'], 
                                  capture_output=True, text=True, timeout=5)
            metrics['kodi_running'] = 1 if result.returncode == 0 and result.stdout.strip() else 0
            
            # Check VPN status
            result = subprocess.run(['adb', '-s', device_address, 'shell', 
                                   'ps | grep -E "(surfshark|openvpn|wireguard)"'], 
                                  capture_output=True, text=True, timeout=5)
            metrics['vpn_running'] = 1 if result.returncode == 0 and result.stdout.strip() else 0
            
            # Network connectivity test
            result = subprocess.run(['adb', '-s', device_address, 'shell', 
                                   'ping -c 1 -W 3 8.8.8.8'], 
                                  capture_output=True, text=True, timeout=10)
            metrics['network_connectivity'] = 1 if result.returncode == 0 else 0
            
        except Exception as e:
            logger.error(f"Failed to collect metrics for {device.device_id}: {e}")
        
        return metrics
    
    def update_prometheus_metrics(self, device: FireTVDevice):
        """Update Prometheus metrics for a device"""
        device_status.labels(device_id=device.device_id, model=device.model).set(
            1 if device.is_online() else 0
        )
        
        metrics = device.metrics
        if 'temperature' in metrics:
            device_temperature.labels(device_id=device.device_id).set(metrics['temperature'])
        if 'cpu_usage' in metrics:
            device_cpu_usage.labels(device_id=device.device_id).set(metrics['cpu_usage'])
        if 'memory_usage' in metrics:
            device_memory_usage.labels(device_id=device.device_id).set(metrics['memory_usage'])
        if 'storage_usage' in metrics:
            device_storage_usage.labels(device_id=device.device_id).set(metrics['storage_usage'])
        if 'kodi_running' in metrics:
            kodi_status.labels(device_id=device.device_id).set(metrics['kodi_running'])
        if 'vpn_running' in metrics:
            vpn_status.labels(device_id=device.device_id).set(metrics['vpn_running'])
    
    def store_metrics(self, device: FireTVDevice):
        """Store device metrics in database"""
        if not self.db_connection:
            return
        
        cursor = self.db_connection.cursor()
        timestamp = datetime.now()
        
        # Update device record
        cursor.execute('''
            INSERT OR REPLACE INTO devices 
            (device_id, ip_address, model, first_seen, last_seen, status)
            VALUES (?, ?, ?, 
                    COALESCE((SELECT first_seen FROM devices WHERE device_id = ?), ?),
                    ?, ?)
        ''', (device.device_id, device.ip_address, device.model, 
              device.device_id, timestamp, timestamp, device.status))
        
        # Store metrics
        for metric_name, metric_value in device.metrics.items():
            if isinstance(metric_value, (int, float)):
                cursor.execute('''
                    INSERT INTO metrics (device_id, timestamp, metric_name, metric_value)
                    VALUES (?, ?, ?, ?)
                ''', (device.device_id, timestamp, metric_name, metric_value))
        
        self.db_connection.commit()
    
    async def check_device_health(self, device: FireTVDevice):
        """Check device health and trigger alerts if needed"""
        metrics = device.metrics
        alerts = []
        
        # Temperature check
        if 'temperature' in metrics and metrics['temperature'] > 70:
            alerts.append(f"High temperature: {metrics['temperature']}°C")
        
        # Storage check
        if 'storage_usage' in metrics and metrics['storage_usage'] > 90:
            alerts.append(f"Low storage: {100 - metrics['storage_usage']}% free")
        
        # Memory check
        if 'memory_usage' in metrics and metrics['memory_usage'] > 95:
            alerts.append(f"High memory usage: {metrics['memory_usage']}%")
        
        # Kodi check
        if 'kodi_running' in metrics and metrics['kodi_running'] == 0:
            alerts.append("Kodi not running")
        
        # VPN check
        if 'vpn_running' in metrics and metrics['vpn_running'] == 0:
            alerts.append("VPN not connected")
        
        # Network check
        if 'network_connectivity' in metrics and metrics['network_connectivity'] == 0:
            alerts.append("Network connectivity issues")
        
        if alerts:
            logger.warning(f"Device {device.device_id} health issues: {', '.join(alerts)}")
            await self.send_alert(device, alerts)
    
    async def send_alert(self, device: FireTVDevice, alerts: List[str]):
        """Send alert notification"""
        alert_data = {
            'device_id': device.device_id,
            'model': device.model,
            'ip_address': device.ip_address,
            'timestamp': datetime.now().isoformat(),
            'alerts': alerts
        }
        
        # Log alert
        logger.warning(f"ALERT for {device.device_id}: {', '.join(alerts)}")
        
        # Store in database
        if self.db_connection:
            cursor = self.db_connection.cursor()
            cursor.execute('''
                INSERT INTO events (device_id, timestamp, event_type, event_data)
                VALUES (?, ?, ?, ?)
            ''', (device.device_id, datetime.now(), 'alert', json.dumps(alert_data)))
            self.db_connection.commit()
        
        # Send webhook notification if configured
        webhook_url = self.config.get('monitoring', {}).get('webhook_url')
        if webhook_url:
            try:
                async with aiohttp.ClientSession() as session:
                    await session.post(webhook_url, json=alert_data)
            except Exception as e:
                logger.error(f"Failed to send webhook alert: {e}")
    
    async def monitoring_loop(self):
        """Main monitoring loop"""
        logger.info("Starting monitoring loop...")
        
        while self.running:
            try:
                # Discover devices
                discovered = await self.discover_devices()
                
                # Process each discovered device
                for ip_address, _ in discovered:
                    device_info = await self.get_device_info(ip_address)
                    if not device_info:
                        continue
                    
                    device_id = device_info['device_id']
                    
                    # Create or update device
                    if device_id not in self.devices:
                        self.devices[device_id] = FireTVDevice(
                            device_id=device_id,
                            ip_address=ip_address,
                            model=device_info['model']
                        )
                        logger.info(f"New device discovered: {device_id} ({device_info['model']})")
                    
                    device = self.devices[device_id]
                    device.ip_address = ip_address  # Update IP if changed
                    device.status = "online"
                    
                    # Collect metrics
                    metrics = await self.get_device_metrics(device)
                    device.update_metrics(metrics)
                    
                    # Update monitoring systems
                    self.update_prometheus_metrics(device)
                    self.store_metrics(device)
                    
                    # Health checks
                    await self.check_device_health(device)
                
                # Mark offline devices
                current_time = datetime.now()
                for device in self.devices.values():
                    if (current_time - device.last_seen).seconds > 300:  # 5 minutes
                        device.status = "offline"
                        device_status.labels(device_id=device.device_id, model=device.model).set(0)
                
                logger.info(f"Monitoring cycle completed. {len(self.devices)} devices in fleet.")
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
            
            # Wait before next cycle
            await asyncio.sleep(60)  # Monitor every minute
    
    async def start(self):
        """Start the fleet monitoring system"""
        logger.info("Starting Pigeonhole Fleet Monitoring System...")
        
        # Initialize database
        self.init_database()
        
        # Start Prometheus metrics server
        start_http_server(8000)
        logger.info("Prometheus metrics server started on port 8000")
        
        # Start monitoring
        self.running = True
        await self.monitoring_loop()
    
    def stop(self):
        """Stop the monitoring system"""
        logger.info("Stopping fleet monitoring system...")
        self.running = False
        if self.db_connection:
            self.db_connection.close()

async def main():
    """Main application entry point"""
    monitor = FleetMonitor()
    
    try:
        await monitor.start()
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
    finally:
        monitor.stop()

if __name__ == "__main__":
    asyncio.run(main())