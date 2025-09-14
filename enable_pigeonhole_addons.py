#!/usr/bin/env python3
"""
Enable and Configure Pigeonhole Addons via HTTP API
"""

import requests
import json
import base64
import time

class PigeonholeAddonManager:
    def __init__(self):
        self.fire_tv_ip = "192.168.1.130"
        self.http_port = 8080
        self.username = "kodi"
        self.password = "0000"
        
        # Create auth header
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_credentials}"
        }
        
        self.base_url = f"http://{self.fire_tv_ip}:{self.http_port}/jsonrpc"
        
        # Core Pigeonhole addons to enable
        self.core_addons = [
            "script.module.resolveurl",
            "skin.arctic.zephyr.pigeonhole", 
            "plugin.video.thecrew",
            "plugin.video.fen.lite",
            "plugin.video.madtitansports",
            "script.pigeonhole.config"
        ]

    def send_rpc_request(self, method, params=None, timeout=15):
        """Send JSON-RPC request to Kodi"""
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
                return response.json()
            else:
                print(f"HTTP Error {response.status_code}: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}")
            return None

    def enable_addon(self, addon_id):
        """Enable specific addon"""
        print(f"Enabling addon: {addon_id}")
        
        response = self.send_rpc_request("Addons.SetAddonEnabled", {
            "addonid": addon_id,
            "enabled": True
        })
        
        if response and "result" in response:
            if response["result"] == "OK":
                print(f"  [OK] {addon_id} enabled successfully")
                return True
            else:
                print(f"  [ISSUE] Enable failed: {response}")
                return False
        else:
            print(f"  [FAIL] No response for {addon_id}")
            return False

    def get_addon_details(self, addon_id):
        """Get detailed addon information"""
        response = self.send_rpc_request("Addons.GetAddonDetails", {
            "addonid": addon_id,
            "properties": ["name", "version", "summary", "enabled", "broken", "dependencies"]
        })
        
        if response and "result" in response:
            return response["result"]["addon"]
        return None

    def check_addon_dependencies(self, addon_id):
        """Check and resolve addon dependencies"""
        print(f"Checking dependencies for: {addon_id}")
        
        details = self.get_addon_details(addon_id)
        if not details:
            print(f"  [FAIL] Could not get details for {addon_id}")
            return False
            
        if "dependencies" in details:
            for dep in details["dependencies"]:
                dep_id = dep.get("addonid")
                if dep_id and dep_id != "xbmc.python":  # Skip system dependencies
                    print(f"  Checking dependency: {dep_id}")
                    
                    # Try to enable the dependency
                    dep_response = self.send_rpc_request("Addons.SetAddonEnabled", {
                        "addonid": dep_id,
                        "enabled": True
                    })
                    
                    if dep_response and dep_response.get("result") == "OK":
                        print(f"    [OK] Dependency {dep_id} enabled")
                    else:
                        print(f"    [ISSUE] Could not enable dependency {dep_id}")
        
        return True

    def set_arctic_zephyr_skin(self):
        """Set Arctic Zephyr as the active skin"""
        print("Setting Arctic Zephyr Pigeonhole as active skin...")
        
        response = self.send_rpc_request("Settings.SetSettingValue", {
            "setting": "lookandfeel.skin",
            "value": "skin.arctic.zephyr.pigeonhole"
        })
        
        if response and "result" in response and response["result"] is True:
            print("  [OK] Arctic Zephyr skin activated")
            return True
        else:
            print("  [ISSUE] Failed to activate Arctic Zephyr skin")
            return False

    def configure_basic_settings(self):
        """Configure basic Kodi settings for Fire TV optimization"""
        print("Configuring basic Fire TV optimizations...")
        
        settings_to_configure = [
            {
                "setting": "videoplayer.usemediacodec",
                "value": 2,  # Always use MediaCodec
                "description": "MediaCodec acceleration"
            },
            {
                "setting": "videoplayer.usemediacodecsurface", 
                "value": True,
                "description": "MediaCodec surface rendering"
            },
            {
                "setting": "debug.showloginfo",
                "value": False,
                "description": "Hide debug info"
            },
            {
                "setting": "network.cachemembuffersize",
                "value": 20971520,  # 20MB
                "description": "Network cache buffer"
            }
        ]
        
        configured_count = 0
        for setting_config in settings_to_configure:
            response = self.send_rpc_request("Settings.SetSettingValue", {
                "setting": setting_config["setting"],
                "value": setting_config["value"]
            })
            
            if response and "result" in response and response["result"] is True:
                print(f"  [OK] {setting_config['description']}")
                configured_count += 1
            else:
                print(f"  [ISSUE] Failed: {setting_config['description']}")
        
        print(f"Basic settings: {configured_count}/{len(settings_to_configure)} configured")
        return configured_count > 0

    def test_addon_functionality(self):
        """Test that addons are working"""
        print("Testing addon functionality...")
        
        test_results = {}
        
        # Test each core addon
        for addon_id in self.core_addons:
            print(f"  Testing {addon_id}...")
            
            # Get current status
            details = self.get_addon_details(addon_id)
            if details:
                enabled = details.get("enabled", False)
                broken = details.get("broken", True)
                
                test_results[addon_id] = {
                    "present": True,
                    "enabled": enabled,
                    "broken": broken,
                    "functional": enabled and not broken
                }
                
                status = "[OK]" if enabled and not broken else "[ISSUE]"
                print(f"    {status} Enabled: {enabled}, Broken: {broken}")
            else:
                test_results[addon_id] = {
                    "present": False,
                    "enabled": False, 
                    "broken": True,
                    "functional": False
                }
                print(f"    [FAIL] Addon not found")
        
        # Summary
        functional_count = sum(1 for result in test_results.values() if result["functional"])
        total_count = len(test_results)
        
        print(f"Addon functionality test: {functional_count}/{total_count} addons working")
        return test_results

    def enable_all_pigeonhole_addons(self):
        """Enable all Pigeonhole addons and configure system"""
        print("PIGEONHOLE ADDON ENABLEMENT AND CONFIGURATION")
        print("=" * 50)
        
        # Test connection first
        ping_response = self.send_rpc_request("JSONRPC.Ping")
        if not ping_response or ping_response.get("result") != "pong":
            print("[FAIL] Cannot connect to Kodi HTTP API")
            return False
        
        print("[OK] Connected to Kodi HTTP API")
        
        # Enable each core addon
        enabled_count = 0
        for addon_id in self.core_addons:
            # Check and resolve dependencies first
            self.check_addon_dependencies(addon_id)
            
            # Enable the addon
            if self.enable_addon(addon_id):
                enabled_count += 1
                
            # Wait briefly between addon enables
            time.sleep(1)
        
        print(f"\nAddon enablement: {enabled_count}/{len(self.core_addons)} addons enabled")
        
        # Set Arctic Zephyr skin
        skin_success = self.set_arctic_zephyr_skin()
        
        # Configure basic settings
        settings_success = self.configure_basic_settings()
        
        # Test functionality
        test_results = self.test_addon_functionality()
        
        # Final assessment
        functional_addons = sum(1 for result in test_results.values() if result["functional"])
        
        print(f"\nFINAL RESULTS:")
        print(f"  Addons enabled: {enabled_count}/{len(self.core_addons)}")
        print(f"  Addons functional: {functional_addons}/{len(self.core_addons)}")
        print(f"  Skin activated: {skin_success}")
        print(f"  Settings optimized: {settings_success}")
        
        if functional_addons >= len(self.core_addons) - 1:  # Allow 1 addon to have issues
            print(f"\n[SUCCESS] Pigeonhole system is functional!")
            return True
        else:
            print(f"\n[WARNING] Some addons need attention")
            return False

def main():
    """Main execution function"""
    manager = PigeonholeAddonManager()
    
    if manager.enable_all_pigeonhole_addons():
        print("\nPigeonhole addon configuration completed successfully!")
    else:
        print("\nPigeonhole addon configuration completed with issues.")
        print("Review the output above for specific problems.")

if __name__ == "__main__":
    main()