#!/usr/bin/env python3
"""
Pigeonhole Device Manager
Abstract base classes and utilities for device management and ADB operations
"""

import subprocess
import socket
import time
import logging
from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

from pigeonhole_config import get_config

class DeviceType(Enum):
    """Supported device types"""
    FIRE_TV_CUBE = "cube"
    FIRE_TV_STICK = "stick"
    FIRE_TV = "firetv"
    ANDROID_TV = "androidtv"
    NVIDIA_SHIELD = "shield"
    UNKNOWN = "unknown"

class DeviceStatus(Enum):
    """Device connection status"""
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    ERROR = "error"
    UNKNOWN = "unknown"

@dataclass
class Device:
    """Device information and status"""
    ip: str
    name: str
    device_type: DeviceType
    model: str
    profile: str = "corporate"
    status: DeviceStatus = DeviceStatus.UNKNOWN
    last_seen: Optional[float] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class ADBConnectionError(Exception):
    """ADB connection related errors"""
    pass

class DeviceNotFoundError(Exception):
    """Device not found or not accessible"""
    pass

class ADBManager:
    """Manages ADB connections and commands with connection pooling"""
    
    def __init__(self, adb_path: str = "./platform-tools/adb.exe"):
        self.adb_path = adb_path
        self.logger = logging.getLogger('pigeonhole.adb')
        self.config = get_config()
        self.timeout = self.config.get_config('deployment.adb_timeout', 30)
        self.retry_attempts = self.config.get_config('deployment.retry_attempts', 3)
        self._connection_lock = threading.Lock()
        self._connected_devices = set()
    
    def _execute_command(self, command: List[str], timeout: Optional[int] = None) -> Tuple[str, str, int]:
        """Execute ADB command with timeout and error handling"""
        cmd_timeout = timeout or self.timeout
        
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=cmd_timeout,
                encoding='utf-8',
                errors='replace'
            )
            return result.stdout.strip(), result.stderr.strip(), result.returncode
            
        except subprocess.TimeoutExpired:
            self.logger.error(f"Command timeout after {cmd_timeout}s: {' '.join(command)}")
            raise ADBConnectionError(f"Command timeout: {' '.join(command)}")
        except Exception as e:
            self.logger.error(f"Command execution failed: {e}")
            raise ADBConnectionError(f"Command execution failed: {e}")
    
    def connect_device(self, ip: str, port: int = 5555) -> bool:
        """Connect to device via ADB"""
        device_addr = f"{ip}:{port}"
        
        with self._connection_lock:
            if device_addr in self._connected_devices:
                return True
            
            try:
                # First check if device is reachable
                if not self._is_device_reachable(ip, port):
                    raise DeviceNotFoundError(f"Device {device_addr} not reachable")
                
                # Connect via ADB
                command = [self.adb_path, "connect", device_addr]
                stdout, stderr, returncode = self._execute_command(command)
                
                if returncode == 0 and ("connected" in stdout.lower() or "already connected" in stdout.lower()):
                    self._connected_devices.add(device_addr)
                    self.logger.info(f"Connected to device: {device_addr}")
                    return True
                else:
                    self.logger.error(f"Failed to connect to {device_addr}: {stderr}")
                    return False
                    
            except Exception as e:
                self.logger.error(f"Connection error for {device_addr}: {e}")
                return False
    
    def disconnect_device(self, ip: str, port: int = 5555) -> bool:
        """Disconnect from device"""
        device_addr = f"{ip}:{port}"
        
        with self._connection_lock:
            try:
                command = [self.adb_path, "disconnect", device_addr]
                stdout, stderr, returncode = self._execute_command(command)
                
                self._connected_devices.discard(device_addr)
                self.logger.info(f"Disconnected from device: {device_addr}")
                return True
                
            except Exception as e:
                self.logger.error(f"Disconnect error for {device_addr}: {e}")
                return False
    
    def execute_shell_command(self, device_addr: str, command: str, timeout: Optional[int] = None) -> Tuple[str, bool]:
        """Execute shell command on device"""
        try:
            adb_command = [self.adb_path, "-s", device_addr, "shell", command]
            stdout, stderr, returncode = self._execute_command(adb_command, timeout)
            
            if returncode == 0:
                return stdout, True
            else:
                self.logger.error(f"Shell command failed on {device_addr}: {stderr}")
                return stderr, False
                
        except Exception as e:
            self.logger.error(f"Shell command error on {device_addr}: {e}")
            return str(e), False
    
    def push_file(self, device_addr: str, local_path: str, remote_path: str) -> bool:
        """Push file to device"""
        try:
            command = [self.adb_path, "-s", device_addr, "push", local_path, remote_path]
            stdout, stderr, returncode = self._execute_command(command)
            
            if returncode == 0:
                self.logger.info(f"File pushed: {local_path} -> {device_addr}:{remote_path}")
                return True
            else:
                self.logger.error(f"File push failed: {stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"File push error: {e}")
            return False
    
    def pull_file(self, device_addr: str, remote_path: str, local_path: str) -> bool:
        """Pull file from device"""
        try:
            command = [self.adb_path, "-s", device_addr, "pull", remote_path, local_path]
            stdout, stderr, returncode = self._execute_command(command)
            
            if returncode == 0:
                self.logger.info(f"File pulled: {device_addr}:{remote_path} -> {local_path}")
                return True
            else:
                self.logger.error(f"File pull failed: {stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"File pull error: {e}")
            return False
    
    def get_device_property(self, device_addr: str, property_name: str) -> Optional[str]:
        """Get device property via getprop"""
        command = f"getprop {property_name}"
        output, success = self.execute_shell_command(device_addr, command)
        
        if success and output.strip():
            return output.strip()
        return None
    
    def _is_device_reachable(self, ip: str, port: int) -> bool:
        """Check if device is reachable on network"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except Exception:
            return False
    
    @contextmanager
    def device_connection(self, ip: str, port: int = 5555):
        """Context manager for device connections"""
        device_addr = f"{ip}:{port}"
        connected = False
        
        try:
            connected = self.connect_device(ip, port)
            if not connected:
                raise ADBConnectionError(f"Failed to connect to {device_addr}")
            
            yield device_addr
            
        finally:
            if connected:
                self.disconnect_device(ip, port)

class BaseDeviceManager(ABC):
    """Abstract base class for device management"""
    
    def __init__(self):
        self.adb = ADBManager()
        self.logger = logging.getLogger('pigeonhole.device_manager')
        self.config = get_config()
        self.devices: Dict[str, Device] = {}
    
    @abstractmethod
    def discover_devices(self, network_range: str) -> List[Device]:
        """Discover devices on network"""
        pass
    
    @abstractmethod
    def classify_device(self, model: str) -> DeviceType:
        """Classify device type from model string"""
        pass
    
    def add_device(self, device: Device) -> None:
        """Add device to managed devices"""
        self.devices[device.ip] = device
        self.logger.info(f"Added device: {device.name} ({device.ip})")
    
    def remove_device(self, ip: str) -> None:
        """Remove device from managed devices"""
        if ip in self.devices:
            device = self.devices.pop(ip)
            self.logger.info(f"Removed device: {device.name} ({ip})")
    
    def get_device(self, ip: str) -> Optional[Device]:
        """Get device by IP address"""
        return self.devices.get(ip)
    
    def get_devices_by_type(self, device_type: DeviceType) -> List[Device]:
        """Get all devices of specified type"""
        return [device for device in self.devices.values() if device.device_type == device_type]
    
    def update_device_status(self, ip: str, status: DeviceStatus) -> None:
        """Update device status"""
        if ip in self.devices:
            self.devices[ip].status = status
            self.devices[ip].last_seen = time.time()

class FireTVManager(BaseDeviceManager):
    """Specialized manager for Fire TV devices"""
    
    def discover_devices(self, network_range: str = "192.168.1.1-254") -> List[Device]:
        """Discover Fire TV and Android TV devices on network"""
        devices = []
        base_ip = ".".join(network_range.split("-")[0].split(".")[:-1])
        start_range = int(network_range.split("-")[0].split(".")[-1])
        end_range = int(network_range.split("-")[1])
        
        def check_device(ip: str) -> Optional[Device]:
            try:
                # Check if ADB port is open
                if not self.adb._is_device_reachable(ip, 5555):
                    return None
                
                # Try to get device info
                with self.adb.device_connection(ip) as device_addr:
                    device_info = self._get_device_info(device_addr)
                    if device_info:
                        self.add_device(device_info)
                        return device_info
                        
            except Exception as e:
                self.logger.debug(f"Failed to check device {ip}: {e}")
                return None
        
        # Parallel device discovery
        if self.config.get_config('deployment.parallel_deployments', True):
            with ThreadPoolExecutor(max_workers=50) as executor:
                futures = {}
                
                for i in range(start_range, end_range + 1):
                    ip = f"{base_ip}.{i}"
                    future = executor.submit(check_device, ip)
                    futures[future] = ip
                
                for future in as_completed(futures, timeout=60):
                    device = future.result()
                    if device:
                        devices.append(device)
        else:
            # Sequential discovery
            for i in range(start_range, end_range + 1):
                ip = f"{base_ip}.{i}"
                device = check_device(ip)
                if device:
                    devices.append(device)
        
        self.logger.info(f"Discovered {len(devices)} devices")
        return devices
    
    def classify_device(self, model: str) -> DeviceType:
        """Classify Fire TV device type from model string"""
        model_lower = model.lower()
        
        if 'fire tv cube' in model_lower or 'aftt' in model_lower:
            return DeviceType.FIRE_TV_CUBE
        elif 'fire tv stick' in model_lower or 'afts' in model_lower:
            return DeviceType.FIRE_TV_STICK
        elif 'shield' in model_lower:
            return DeviceType.NVIDIA_SHIELD
        elif 'fire tv' in model_lower or 'aftm' in model_lower:
            return DeviceType.FIRE_TV
        else:
            return DeviceType.ANDROID_TV
    
    def _get_device_info(self, device_addr: str) -> Optional[Device]:
        """Get detailed device information"""
        try:
            # Get device model
            model = self.adb.get_device_property(device_addr, "ro.product.model")
            if not model:
                return None
            
            # Get device name
            name = self.adb.get_device_property(device_addr, "ro.product.name") or model
            
            # Get additional info
            manufacturer = self.adb.get_device_property(device_addr, "ro.product.manufacturer")
            android_version = self.adb.get_device_property(device_addr, "ro.build.version.release")
            
            # Classify device type
            device_type = self.classify_device(model)
            
            # Extract IP from device address
            ip = device_addr.split(':')[0]
            
            return Device(
                ip=ip,
                name=name,
                device_type=device_type,
                model=model,
                profile='corporate',
                status=DeviceStatus.CONNECTED,
                last_seen=time.time(),
                metadata={
                    'manufacturer': manufacturer,
                    'android_version': android_version,
                    'device_addr': device_addr
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error getting device info for {device_addr}: {e}")
            return None

# Factory function
def create_device_manager() -> BaseDeviceManager:
    """Create appropriate device manager"""
    return FireTVManager()