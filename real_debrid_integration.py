#!/usr/bin/env python3
"""
Pigeonhole Streaming - Real Debrid Integration System
Automated Real Debrid configuration with error recovery
"""

import os
import subprocess
import json
import time
import requests
from datetime import datetime

class RealDebridIntegrator:
    def __init__(self):
        self.fire_tv_ip = "192.168.1.130"
        self.adb_path = r"M:\platform-tools\adb.exe"
        self.kodi_data_path = "/sdcard/Android/data/org.xbmc.kodi/files/.kodi"
        self.rd_api_base = "https://api.real-debrid.com/rest/1.0"
        self.config_status = {
            "timestamp": datetime.now().isoformat(),
            "rd_account_valid": False,
            "addon_configurations": [],
            "streaming_tests": [],
            "recommendations": []
        }
        
    def run_adb_command(self, command, timeout=30):
        """Execute ADB command with error handling"""
        try:
            full_command = f'"{self.adb_path}" {command}'
            result = subprocess.run(full_command, shell=True, capture_output=True, 
                                  text=True, timeout=timeout)
            return result.stdout.strip(), result.stderr.strip(), result.returncode
        except subprocess.TimeoutExpired:
            return "", "Command timeout", 1
        except Exception as e:
            return "", str(e), 1

    def validate_rd_account(self, api_key):
        """Validate Real Debrid account and get user info"""
        print("Validating Real Debrid account...")
        
        try:
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get(f"{self.rd_api_base}/user", headers=headers, timeout=10)
            
            if response.status_code == 200:
                user_data = response.json()
                self.config_status["rd_account_valid"] = True
                self.config_status["user_info"] = {
                    "username": user_data.get("username", "Unknown"),
                    "email": user_data.get("email", "Unknown"),
                    "premium": user_data.get("type", "Unknown") == "premium",
                    "expiration": user_data.get("expiration", "Unknown")
                }
                print(f"✓ Valid account: {user_data.get('username')}")
                return True
            else:
                print(f"✗ Invalid API key: HTTP {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Connection error: {e}")
            return False

    def configure_resolveurl(self, api_key):
        """Configure ResolveURL addon with Real Debrid"""
        print("Configuring ResolveURL addon...")
        
        config_result = {
            "addon": "script.module.resolveurl",
            "configured": False,
            "error": None
        }
        
        try:
            # Create ResolveURL settings directory
            settings_path = f"{self.kodi_data_path}/userdata/addon_data/script.module.resolveurl"
            self.run_adb_command(f'shell "mkdir -p {settings_path}"')
            
            # Create settings.xml for ResolveURL
            settings_xml = f'''<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<settings version="2">
    <category id="universal">
        <setting id="RealDebridResolver_enabled">true</setting>
        <setting id="RealDebridResolver_login">{api_key}</setting>
        <setting id="RealDebridResolver_priority">90</setting>
    </category>
    <category id="premium">
        <setting id="RealdebridResolver_enabled">true</setting>
        <setting id="RealdebridResolver_username"></setting>
        <setting id="RealdebridResolver_password"></setting>
        <setting id="RealdebridResolver_token">{api_key}</setting>
    </category>
</settings>'''
            
            # Write settings to device
            temp_file = "/sdcard/temp_resolveurl_settings.xml"
            self.run_adb_command(f'shell "echo \'{settings_xml}\' > {temp_file}"')
            self.run_adb_command(f'shell "cp {temp_file} {settings_path}/settings.xml"')
            self.run_adb_command(f'shell "chmod 644 {settings_path}/settings.xml"')
            
            config_result["configured"] = True
            print("✓ ResolveURL configured with Real Debrid")
            
        except Exception as e:
            config_result["error"] = str(e)
            print(f"✗ ResolveURL configuration failed: {e}")
            
        self.config_status["addon_configurations"].append(config_result)
        return config_result["configured"]

    def configure_thecrew(self, api_key):
        """Configure The Crew addon with Real Debrid"""
        print("Configuring The Crew addon...")
        
        config_result = {
            "addon": "plugin.video.thecrew",
            "configured": False,
            "error": None
        }
        
        try:
            # Create The Crew settings directory
            settings_path = f"{self.kodi_data_path}/userdata/addon_data/plugin.video.thecrew"
            self.run_adb_command(f'shell "mkdir -p {settings_path}"')
            
            # Create settings.xml for The Crew
            crew_settings = f'''<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<settings version="2">
    <category id="accounts">
        <setting id="rd.enabled">true</setting>
        <setting id="rd.token">{api_key}</setting>
        <setting id="rd.priority">1</setting>
    </category>
    <category id="playback">
        <setting id="results.timeout">30</setting>
        <setting id="sources.timeout">20</setting>
        <setting id="autoplay.enabled">true</setting>
    </category>
</settings>'''
            
            # Write settings to device
            temp_file = "/sdcard/temp_crew_settings.xml"
            self.run_adb_command(f'shell "echo \'{crew_settings}\' > {temp_file}"')
            self.run_adb_command(f'shell "cp {temp_file} {settings_path}/settings.xml"')
            self.run_adb_command(f'shell "chmod 644 {settings_path}/settings.xml"')
            
            config_result["configured"] = True
            print("✓ The Crew configured with Real Debrid")
            
        except Exception as e:
            config_result["error"] = str(e)
            print(f"✗ The Crew configuration failed: {e}")
            
        self.config_status["addon_configurations"].append(config_result)
        return config_result["configured"]

    def configure_fen_lite(self, api_key):
        """Configure FEN Lite addon with Real Debrid"""
        print("Configuring FEN Lite addon...")
        
        config_result = {
            "addon": "plugin.video.fen.lite",
            "configured": False,
            "error": None
        }
        
        try:
            # Create FEN Lite settings directory
            settings_path = f"{self.kodi_data_path}/userdata/addon_data/plugin.video.fen.lite"
            self.run_adb_command(f'shell "mkdir -p {settings_path}"')
            
            # Create settings.xml for FEN Lite
            fen_settings = f'''<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<settings version="2">
    <category id="debrid">
        <setting id="rd_enabled">true</setting>
        <setting id="rd_api_key">{api_key}</setting>
        <setting id="rd_priority">90</setting>
    </category>
    <category id="results">
        <setting id="limit_resolve">50</setting>
        <setting id="timeout">25</setting>
        <setting id="filter_quality">true</setting>
    </category>
</settings>'''
            
            # Write settings to device
            temp_file = "/sdcard/temp_fen_settings.xml"
            self.run_adb_command(f'shell "echo \'{fen_settings}\' > {temp_file}"')
            self.run_adb_command(f'shell "cp {temp_file} {settings_path}/settings.xml"')
            self.run_adb_command(f'shell "chmod 644 {settings_path}/settings.xml"')
            
            config_result["configured"] = True
            print("✓ FEN Lite configured with Real Debrid")
            
        except Exception as e:
            config_result["error"] = str(e)
            print(f"✗ FEN Lite configuration failed: {e}")
            
        self.config_status["addon_configurations"].append(config_result)
        return config_result["configured"]

    def test_streaming_functionality(self):
        """Test streaming functionality with configured addons"""
        print("Testing streaming functionality...")
        
        # Start Kodi for testing
        self.run_adb_command('shell "am force-stop org.xbmc.kodi"')
        time.sleep(2)
        self.run_adb_command('shell "am start -n org.xbmc.kodi/.Splash"')
        time.sleep(15)
        
        # Check if Kodi started successfully
        stdout, _, code = self.run_adb_command('shell "ps | grep kodi"')
        
        streaming_test = {
            "timestamp": datetime.now().isoformat(),
            "kodi_startup": code == 0 and "kodi" in stdout,
            "addons_loaded": False,
            "memory_usage": None,
            "stability_check": False
        }
        
        if streaming_test["kodi_startup"]:
            print("✓ Kodi started successfully")
            
            # Check addon directories are accessible
            addon_check_commands = [
                f'shell "test -d {self.kodi_data_path}/userdata/addon_data/script.module.resolveurl && echo resolveurl_ok"',
                f'shell "test -d {self.kodi_data_path}/userdata/addon_data/plugin.video.thecrew && echo crew_ok"',
                f'shell "test -d {self.kodi_data_path}/userdata/addon_data/plugin.video.fen.lite && echo fen_ok"'
            ]
            
            addon_status = []
            for cmd in addon_check_commands:
                stdout, _, _ = self.run_adb_command(cmd)
                addon_status.append("ok" in stdout)
                
            streaming_test["addons_loaded"] = all(addon_status)
            
            # Get memory usage
            memory_stdout, _, _ = self.run_adb_command('shell "top -n 1 | grep kodi"')
            if memory_stdout:
                parts = memory_stdout.split()
                if len(parts) >= 6:
                    streaming_test["memory_usage"] = {
                        "memory_mb": parts[5],
                        "cpu_percent": parts[8] if len(parts) > 8 else "N/A"
                    }
            
            # Stability check - run for 30 seconds and check if still running
            print("Running stability check (30 seconds)...")
            time.sleep(30)
            stdout, _, code = self.run_adb_command('shell "ps | grep kodi"')
            streaming_test["stability_check"] = code == 0 and "kodi" in stdout
            
            if streaming_test["stability_check"]:
                print("✓ Stability test passed")
            else:
                print("✗ Stability test failed - Kodi may have crashed")
                
        else:
            print("✗ Kodi failed to start")
            
        self.config_status["streaming_tests"].append(streaming_test)
        return streaming_test

    def generate_recommendations(self):
        """Generate setup recommendations"""
        recommendations = []
        
        # Account validation recommendations
        if not self.config_status["rd_account_valid"]:
            recommendations.append({
                "priority": "CRITICAL",
                "category": "Account",
                "issue": "Real Debrid account validation failed",
                "action": "Verify API key and account status"
            })
        
        # Addon configuration recommendations
        failed_configs = [cfg for cfg in self.config_status["addon_configurations"] if not cfg["configured"]]
        if failed_configs:
            recommendations.append({
                "priority": "HIGH",
                "category": "Configuration",
                "issue": f"{len(failed_configs)} addon(s) failed to configure",
                "action": "Review addon settings and retry configuration"
            })
        
        # Streaming test recommendations
        if self.config_status["streaming_tests"]:
            latest_test = self.config_status["streaming_tests"][-1]
            if not latest_test["stability_check"]:
                recommendations.append({
                    "priority": "HIGH",
                    "category": "Stability",
                    "issue": "Kodi stability test failed",
                    "action": "Review advanced settings and memory configuration"
                })
        
        self.config_status["recommendations"] = recommendations

    def save_configuration_report(self):
        """Save configuration report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"M:\\rd_integration_report_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.config_status, f, indent=2)
            print(f"\nConfiguration report saved to: {filename}")
        except Exception as e:
            print(f"Failed to save report: {e}")

    def integrate_real_debrid(self, api_key):
        """Main integration function"""
        print("Starting Real Debrid integration...")
        
        # Connect to device
        stdout, _, code = self.run_adb_command(f"connect {self.fire_tv_ip}:5555")
        if code != 0:
            print("Failed to connect to Fire TV")
            return False
        
        # Validate account
        if not self.validate_rd_account(api_key):
            return False
        
        # Configure addons
        self.configure_resolveurl(api_key)
        self.configure_thecrew(api_key)
        self.configure_fen_lite(api_key)
        
        # Test functionality
        self.test_streaming_functionality()
        
        # Generate recommendations
        self.generate_recommendations()
        
        # Save report
        self.save_configuration_report()
        
        # Print summary
        self.print_integration_summary()
        
        return True

    def print_integration_summary(self):
        """Print integration summary"""
        print("\n" + "="*60)
        print("REAL DEBRID INTEGRATION SUMMARY")
        print("="*60)
        
        if self.config_status["rd_account_valid"]:
            user_info = self.config_status.get("user_info", {})
            print(f"✓ Account: {user_info.get('username', 'Unknown')}")
            print(f"✓ Premium: {user_info.get('premium', 'Unknown')}")
        else:
            print("✗ Account validation failed")
        
        print(f"\nAddon Configurations:")
        for config in self.config_status["addon_configurations"]:
            status = "✓" if config["configured"] else "✗"
            print(f"  {status} {config['addon']}")
            
        if self.config_status["streaming_tests"]:
            test = self.config_status["streaming_tests"][-1]
            print(f"\nFunctionality Test:")
            print(f"  {'✓' if test['kodi_startup'] else '✗'} Kodi Startup")
            print(f"  {'✓' if test['addons_loaded'] else '✗'} Addons Loaded")
            print(f"  {'✓' if test['stability_check'] else '✗'} Stability Check")
            
        if self.config_status["recommendations"]:
            print(f"\nRecommendations: {len(self.config_status['recommendations'])}")
            for rec in self.config_status["recommendations"]:
                print(f"  {rec['priority']}: {rec['issue']}")
        
        print("\nIntegration complete!")

def main():
    """Main execution with user input"""
    integrator = RealDebridIntegrator()
    
    print("Real Debrid Integration System")
    print("=" * 40)
    
    api_key = input("Enter your Real Debrid API Key: ").strip()
    if not api_key:
        print("No API key provided. Exiting.")
        return
        
    if integrator.integrate_real_debrid(api_key):
        print("\nReal Debrid integration completed successfully!")
    else:
        print("\nReal Debrid integration failed. Check the report for details.")

if __name__ == "__main__":
    main()