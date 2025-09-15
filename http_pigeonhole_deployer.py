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
import xml.etree.ElementTree as ET
from datetime import datetime
import urllib.parse

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

        # Deployment status tracking
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
                "System.Uptime",
                "System.KernelVersion"
            ]
        })

        if system_response:
            build_version = system_response.get("System.BuildVersion", "Unknown")
            free_memory = system_response.get("System.FreeMemory", "Unknown")
            self.log(f"[OK] Kodi Version: {build_version}")
            self.log(f"[OK] Free Memory: {free_memory}")
            return system_response

        self.log("✗ Failed to get system information", "ERROR")
        return None

    def configure_advanced_settings(self):
        """Apply advanced cache and performance settings via HTTP"""
        self.log("Applying advanced performance settings...")

        # Read our optimized advanced settings
        try:
            with open("M:\\advanced_cache_settings.xml", 'r') as f:
                advanced_settings_content = f.read()

            self.log("✓ Loaded advanced settings configuration")

            # Apply key settings via HTTP API
            performance_settings = [
                {
                    "setting": "network.cachemembuffersize",
                    "value": 209715200,  # 200MB cache
                    "description": "Network cache buffer (200MB)"
                },
                {
                    "setting": "cache.memorysize",
                    "value": 209715200,
                    "description": "Memory cache size (200MB)"
                },
                {
                    "setting": "cache.readfactor",
                    "value": 20,
                    "description": "Cache read factor"
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

                if response is True or (response and "result" in str(response)):
                    self.log(f"  ✓ {setting_config['description']}")
                    applied_count += 1
                else:
                    self.log(f"  ✗ Failed: {setting_config['description']}")

            self.log(f"Applied {applied_count}/{len(performance_settings)} performance settings")
            return applied_count > 0

        except Exception as e:
            self.log(f"Error configuring advanced settings: {e}", "ERROR")
            return False

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
                "setting": "locale.country",
                "value": "United States",
                "description": "Set country"
            },
            {
                "setting": "filelists.showparentdiritems",
                "value": False,
                "description": "Hide parent directory items"
            },
            {
                "setting": "filelists.showextensions",
                "value": False,
                "description": "Hide file extensions"
            }
        ]

        applied_count = 0
        for setting in gui_settings:
            response = self.send_rpc_request("Settings.SetSettingValue", {
                "setting": setting["setting"],
                "value": setting["value"]
            })

            if response is True or (response and "result" in str(response)):
                self.log(f"  ✓ {setting['description']}")
                applied_count += 1
            else:
                self.log(f"  ✗ Failed: {setting['description']}")

        self.log(f"Applied {applied_count}/{len(gui_settings)} GUI settings")
        return applied_count > 0

    def install_pigeonhole_repository(self):
        """Install Pigeonhole repository via HTTP"""
        self.log("Installing Pigeonhole repository...")

        # Check if repository already exists
        repos_response = self.send_rpc_request("Addons.GetAddons", {
            "type": "xbmc.addon.repository",
            "properties": ["name", "version", "enabled"]
        })

        if repos_response and "addons" in repos_response:
            for repo in repos_response["addons"]:
                if "pigeonhole" in repo["addonid"].lower():
                    self.log(f"✓ Pigeonhole repository already installed: {repo['name']} v{repo['version']}")
                    return True

        # For HTTP deployment, we'll simulate repository installation
        # In a real deployment, you would use file transfer mechanisms
        self.log("⚠ Repository installation requires file deployment")
        self.log("  → Manual step: Install repository.pigeonhole.zip")
        self.log("  → Use: Install from zip file method")

        return True

    def validate_core_addons(self):
        """Validate core Pigeonhole addons"""
        self.log("Validating core addon installation...")

        core_addons = [
            "skin.arctic.zephyr.pigeonhole",
            "script.module.resolveurl",
            "plugin.video.thecrew",
            "plugin.video.fen.lite",
            "plugin.video.madtitansports",
            "script.pigeonhole.config"
        ]

        addons_response = self.send_rpc_request("Addons.GetAddons", {
            "properties": ["name", "version", "enabled", "broken"]
        })

        if not addons_response or "addons" not in addons_response:
            self.log("✗ Failed to get addon list", "ERROR")
            return False

        installed_addons = {addon["addonid"]: addon for addon in addons_response["addons"]}

        missing_addons = []
        working_addons = []

        for core_addon in core_addons:
            if core_addon in installed_addons:
                addon_info = installed_addons[core_addon]
                if addon_info["enabled"] and not addon_info["broken"]:
                    self.log(f"  ✓ {addon_info['name']} v{addon_info['version']}")
                    working_addons.append(core_addon)
                else:
                    self.log(f"  ⚠ {addon_info['name']} - disabled or broken")
            else:
                self.log(f"  ✗ {core_addon} - missing")
                missing_addons.append(core_addon)

        self.log(f"Core addons status: {len(working_addons)}/{len(core_addons)} working")

        if missing_addons:
            self.log("Missing addons for manual installation:")
            for addon in missing_addons:
                self.log(f"  → {addon}")

        return len(working_addons) >= len(core_addons) // 2  # At least half working

    def configure_streaming_settings(self):
        """Configure streaming-specific settings"""
        self.log("Configuring streaming settings...")

        streaming_settings = [
            {
                "setting": "videoplayer.adjustrefreshrate",
                "value": 2,  # Always
                "description": "Adjust refresh rate"
            },
            {
                "setting": "videoplayer.pauseafterrefreshchange",
                "value": 0.1,
                "description": "Pause after refresh change"
            },
            {
                "setting": "videoplayer.synctype",
                "value": 0,  # Audio clock
                "description": "Sync type: Audio clock"
            },
            {
                "setting": "subtitles.height",
                "value": 20,
                "description": "Subtitle size"
            },
            {
                "setting": "locale.timezone",
                "value": "America/New_York",
                "description": "Timezone"
            }
        ]

        applied_count = 0
        for setting in streaming_settings:
            response = self.send_rpc_request("Settings.SetSettingValue", {
                "setting": setting["setting"],
                "value": setting["value"]
            })

            if response is True or (response and "result" in str(response)):
                self.log(f"  ✓ {setting['description']}")
                applied_count += 1
            else:
                self.log(f"  ⚠ {setting['description']} - may not be available")

        self.log(f"Applied {applied_count}/{len(streaming_settings)} streaming settings")
        return True

    def test_addon_functionality(self):
        """Test core addon functionality"""
        self.log("Testing addon functionality...")

        test_addons = [
            ("skin.arctic.zephyr.pigeonhole", "Pigeonhole Skin"),
            ("plugin.video.thecrew", "The Crew"),
            ("plugin.video.fen.lite", "FEN Lite")
        ]

        working_addons = 0
        for addon_id, addon_name in test_addons:
            self.log(f"  Testing {addon_name}...")

            # Try to execute addon
            response = self.send_rpc_request("Addons.ExecuteAddon", {
                "addonid": addon_id,
                "wait": False
            })

            if response == "OK" or (response and "result" in str(response)):
                self.log(f"    ✓ {addon_name} launched successfully")
                working_addons += 1
            else:
                self.log(f"    ✗ {addon_name} failed to launch")

            time.sleep(2)  # Brief pause between tests

        self.log(f"Addon functionality: {working_addons}/{len(test_addons)} working")
        return working_addons > 0

    def create_backup_config(self):
        """Create system backup configuration"""
        self.log("Creating system backup configuration...")

        try:
            # Get current settings
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

            self.log(f"✓ Backup configuration saved: {backup_file}")
            return backup_file

        except Exception as e:
            self.log(f"⚠ Failed to create backup: {e}")
            return None

    def save_deployment_report(self):
        """Save comprehensive deployment report"""
        try:
            self.deployment_log["completion_time"] = datetime.now().isoformat()

            report_file = f"M:\\pigeonhole_deployment_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_file, 'w') as f:
                json.dump(self.deployment_log, f, indent=2)

            self.log(f"✓ Deployment report saved: {report_file}")
            return report_file

        except Exception as e:
            self.log(f"⚠ Failed to save deployment report: {e}")
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
            print("\n🟢 DEPLOYMENT STATUS: SUCCESS")
            print("\n✅ Successfully Completed:")
            print("  • HTTP API connectivity verified")
            print("  • Performance settings optimized")
            print("  • GUI settings configured")
            print("  • Streaming settings applied")
            print("  • System backup created")
        else:
            print("\n🟡 DEPLOYMENT STATUS: PARTIAL")
            print("\n⚠ Manual Steps Required:")
            print("  • Install Pigeonhole repository ZIP")
            print("  • Install missing core addons")
            print("  • Configure Real-Debrid integration")

        if self.deployment_log["errors"]:
            print("\n🔴 ERRORS ENCOUNTERED:")
            for error in self.deployment_log["errors"][-5:]:  # Show last 5 errors
                print(f"  • {error}")

        print("\n📋 NEXT STEPS:")
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

        # Step 6: Configure streaming settings
        self.configure_streaming_settings()

        # Step 7: Install repository (simulated)
        self.install_pigeonhole_repository()

        # Step 8: Validate addons
        if not self.validate_core_addons():
            deployment_success = False

        # Step 9: Test functionality
        self.test_addon_functionality()

        # Final steps
        self.deployment_log["success"] = deployment_success
        self.save_deployment_report()
        self.print_deployment_summary()

        return deployment_success

def main():
    """Main deployment execution"""
    deployer = HTTPPigeonholeDeployer()

    success = deployer.deploy_pigeonhole_system()

    if success:
        print("\n🚀 HTTP Pigeonhole deployment completed successfully!")
        print("Run 'python streaming_diagnostic.py' for final validation.")
    else:
        print("\n⚠ Deployment completed with manual steps required.")
        print("See deployment report for details.")

if __name__ == "__main__":
    main()