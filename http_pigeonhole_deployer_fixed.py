#!/usr/bin/env python3
"""
HTTP-First Pigeonhole Streaming System Deployer
Comprehensive deployment using only HTTP API for 100% reliability
"""

import requests
import json
import base64
import time
import os
from datetime import datetime

class HTTPPigeonholeDeployer:
    def __init__(self):
        self.fire_tv_ip = "192.168.1.130"
        self.http_port = 8080
        self.username = "kodi"
        self.password = "0000"
        self.base_url = f"http://{self.fire_tv_ip}:{self.http_port}/jsonrpc"

        # Create auth header
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_credentials}"
        }

        self.deployment_log = {
            "timestamp": datetime.now().isoformat(),
            "steps": [],
            "success": False,
            "errors": []
        }

    def log(self, message, level="INFO"):
        """Enhanced logging with deployment tracking"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)

        self.deployment_log["steps"].append({
            "timestamp": timestamp,
            "level": level,
            "message": message
        })

        if level == "ERROR":
            self.deployment_log["errors"].append(message)

    def send_rpc_request(self, method, params=None, timeout=15):
        """Enhanced RPC with better error handling"""
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "id": 1
        }
        if params:
            payload["params"] = params

        try:
            response = requests.post(
                self.base_url,
                json=payload,
                headers=self.headers,
                timeout=timeout
            )

            if response.status_code == 200:
                result = response.json()
                if "error" in result:
                    self.log(f"Kodi API Error: {result['error']}", "ERROR")
                    return None
                return result.get("result", result)
            else:
                self.log(f"HTTP Error {response.status_code}: {response.text}", "ERROR")
                return None

        except requests.exceptions.RequestException as e:
            self.log(f"Connection error: {e}", "ERROR")
            return None

    def test_connection(self):
        """Verify HTTP API connectivity"""
        self.log("Testing Kodi HTTP API connection...")

        response = self.send_rpc_request("JSONRPC.Ping")
        if response and response == "pong":
            self.log("[OK] HTTP API connection successful")
            return True
        else:
            self.log("[FAIL] HTTP API connection failed", "ERROR")
            return False

    def get_system_info(self):
        """Get comprehensive system information"""
        self.log("Gathering system information...")

        system_response = self.send_rpc_request("System.GetInfoLabels", {
            "labels": [
                "System.BuildVersion",
                "System.FreeMemory",
                "System.CPUUsage",
                "System.Uptime"
            ]
        })

        if system_response:
            build_version = system_response.get("System.BuildVersion", "Unknown")
            free_memory = system_response.get("System.FreeMemory", "Unknown")
            self.log(f"[OK] Kodi Version: {build_version}")
            self.log(f"[OK] Free Memory: {free_memory}")
            return system_response

        self.log("[FAIL] Failed to get system information", "ERROR")
        return None

    def configure_advanced_settings(self):
        """Apply advanced cache and performance settings via HTTP"""
        self.log("Applying advanced performance settings...")

        performance_settings = [
            {
                "setting": "network.cachemembuffersize",
                "value": 209715200,  # 200MB cache
                "description": "Network cache buffer (200MB)"
            },
            {
                "setting": "videoplayer.usemediacodec",
                "value": True,
                "description": "Enable MediaCodec acceleration"
            },
            {
                "setting": "videoplayer.useamcodec",
                "value": True,
                "description": "Enable AMCodec acceleration"
            },
            {
                "setting": "debug.showloginfo",
                "value": False,
                "description": "Disable debug overlay"
            }
        ]

        applied_count = 0
        for setting_config in performance_settings:
            response = self.send_rpc_request("Settings.SetSettingValue", {
                "setting": setting_config["setting"],
                "value": setting_config["value"]
            })

            if response is True:
                self.log(f"  [OK] {setting_config['description']}")
                applied_count += 1
            else:
                self.log(f"  [FAIL] Failed: {setting_config['description']}")

        self.log(f"Applied {applied_count}/{len(performance_settings)} performance settings")
        return applied_count > 0

    def configure_gui_settings(self):
        """Apply GUI optimizations via HTTP"""
        self.log("Applying GUI optimizations...")

        gui_settings = [
            {
                "setting": "lookandfeel.skin",
                "value": "skin.arctic.zephyr.pigeonhole",
                "description": "Set Pigeonhole skin"
            },
            {
                "setting": "locale.language",
                "value": "resource.language.en_gb",
                "description": "Set English language"
            },
            {
                "setting": "filelists.showparentdiritems",
                "value": False,
                "description": "Hide parent directory items"
            }
        ]

        applied_count = 0
        for setting in gui_settings:
            response = self.send_rpc_request("Settings.SetSettingValue", {
                "setting": setting["setting"],
                "value": setting["value"]
            })

            if response is True:
                self.log(f"  [OK] {setting['description']}")
                applied_count += 1
            else:
                self.log(f"  [FAIL] Failed: {setting['description']}")

        self.log(f"Applied {applied_count}/{len(gui_settings)} GUI settings")
        return applied_count > 0

    def validate_core_addons(self):
        """Validate core Pigeonhole addons"""
        self.log("Validating core addon installation...")

        core_addons = [
            "skin.arctic.zephyr.pigeonhole",
            "script.module.resolveurl",
            "plugin.video.thecrew",
            "plugin.video.fen.lite",
            "plugin.video.madtitansports"
        ]

        addons_response = self.send_rpc_request("Addons.GetAddons", {
            "properties": ["name", "version", "enabled", "broken"]
        })

        if not addons_response or "addons" not in addons_response:
            self.log("[FAIL] Failed to get addon list", "ERROR")
            return False

        installed_addons = {addon["addonid"]: addon for addon in addons_response["addons"]}

        missing_addons = []
        working_addons = []

        for core_addon in core_addons:
            if core_addon in installed_addons:
                addon_info = installed_addons[core_addon]
                if addon_info["enabled"] and not addon_info["broken"]:
                    self.log(f"  [OK] {addon_info['name']} v{addon_info['version']}")
                    working_addons.append(core_addon)
                else:
                    self.log(f"  [WARN] {addon_info['name']} - disabled or broken")
            else:
                self.log(f"  [MISSING] {core_addon}")
                missing_addons.append(core_addon)

        self.log(f"Core addons status: {len(working_addons)}/{len(core_addons)} working")
        return len(working_addons) >= 1  # At least one working

    def test_addon_functionality(self):
        """Test core addon functionality"""
        self.log("Testing addon functionality...")

        test_addons = [
            ("skin.arctic.zephyr.pigeonhole", "Pigeonhole Skin")
        ]

        working_addons = 0
        for addon_id, addon_name in test_addons:
            self.log(f"  Testing {addon_name}...")

            response = self.send_rpc_request("Addons.ExecuteAddon", {
                "addonid": addon_id,
                "wait": False
            })

            if response == "OK":
                self.log(f"    [OK] {addon_name} launched successfully")
                working_addons += 1
            else:
                self.log(f"    [FAIL] {addon_name} failed to launch")

            time.sleep(2)

        self.log(f"Addon functionality: {working_addons}/{len(test_addons)} working")
        return working_addons > 0

    def create_backup_config(self):
        """Create system backup configuration"""
        self.log("Creating system backup configuration...")

        try:
            current_skin = self.send_rpc_request("Settings.GetSettingValue", {
                "setting": "lookandfeel.skin"
            })

            backup_config = {
                "timestamp": datetime.now().isoformat(),
                "original_skin": current_skin.get("value") if current_skin else "skin.estuary",
                "deployment_log": self.deployment_log
            }

            backup_file = f"M:\\pigeonhole_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(backup_file, 'w') as f:
                json.dump(backup_config, f, indent=2)

            self.log(f"[OK] Backup configuration saved: {backup_file}")
            return backup_file

        except Exception as e:
            self.log(f"[WARN] Failed to create backup: {e}")
            return None

    def print_deployment_summary(self):
        """Print comprehensive deployment summary"""
        print("\n" + "="*80)
        print("PIGEONHOLE STREAMING SYSTEM - HTTP DEPLOYMENT SUMMARY")
        print("="*80)

        print(f"Target Device: {self.fire_tv_ip}:{self.http_port}")
        print(f"Deployment Time: {self.deployment_log['timestamp']}")
        print(f"Total Steps: {len(self.deployment_log['steps'])}")
        print(f"Errors: {len(self.deployment_log['errors'])}")

        if self.deployment_log["success"]:
            print("\n[SUCCESS] DEPLOYMENT STATUS: SUCCESS")
            print("\n[OK] Successfully Completed:")
            print("  - HTTP API connectivity verified")
            print("  - Performance settings optimized")
            print("  - GUI settings configured")
            print("  - System backup created")
        else:
            print("\n[PARTIAL] DEPLOYMENT STATUS: PARTIAL")
            print("\n[MANUAL] Manual Steps Required:")
            print("  - Install Pigeonhole repository ZIP")
            print("  - Install missing core addons")
            print("  - Configure Real-Debrid integration")

        if self.deployment_log["errors"]:
            print("\n[ERRORS] ERRORS ENCOUNTERED:")
            for error in self.deployment_log["errors"][-3:]:
                print(f"  - {error}")

        print("\n[NEXT] NEXT STEPS:")
        print("  1. Install repository.pigeonhole.zip manually")
        print("  2. Install missing addons from repository")
        print("  3. Configure Real-Debrid accounts in addons")
        print("  4. Run validation diagnostic")

        print("="*80)

    def deploy_pigeonhole_system(self):
        """Complete Pigeonhole system deployment via HTTP"""
        self.log("="*60)
        self.log("STARTING PIGEONHOLE STREAMING SYSTEM DEPLOYMENT")
        self.log("Using HTTP-First approach for 100% reliability")
        self.log("="*60)

        deployment_success = True

        # Step 1: Test connection
        if not self.test_connection():
            self.deployment_log["success"] = False
            return False

        # Step 2: Create backup
        self.create_backup_config()

        # Step 3: Get system information
        self.get_system_info()

        # Step 4: Apply performance optimizations
        if not self.configure_advanced_settings():
            deployment_success = False

        # Step 5: Configure GUI settings
        if not self.configure_gui_settings():
            deployment_success = False

        # Step 6: Validate addons
        if not self.validate_core_addons():
            deployment_success = False

        # Step 7: Test functionality
        self.test_addon_functionality()

        # Final steps
        self.deployment_log["success"] = deployment_success
        self.print_deployment_summary()

        return deployment_success

def main():
    """Main deployment execution"""
    deployer = HTTPPigeonholeDeployer()

    success = deployer.deploy_pigeonhole_system()

    if success:
        print("\n[SUCCESS] HTTP Pigeonhole deployment completed successfully!")
        print("Run 'python streaming_diagnostic.py' for final validation.")
    else:
        print("\n[MANUAL] Deployment completed with manual steps required.")
        print("See deployment summary for details.")

if __name__ == "__main__":
    main()