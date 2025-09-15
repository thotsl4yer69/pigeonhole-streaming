#!/usr/bin/env python3
"""
Pigeonhole Streaming Configurator
Automates streaming configuration for Real-Debrid and provider setup
"""

import requests
import json
import base64
import time
from datetime import datetime

class PigeonholeStreamingConfigurator:
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

    def send_request(self, payload):
        """Send JSON-RPC request to Kodi"""
        try:
            response = requests.post(self.base_url, json=payload, headers=self.headers, timeout=15)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}: {response.text}"}
        except Exception as e:
            return {"error": str(e)}

    def configure_resolveurl_settings(self):
        """Configure ResolveURL for optimal streaming"""
        print("CONFIGURING RESOLVEURL SETTINGS")
        print("=" * 40)

        # Key ResolveURL settings for streaming
        settings_to_configure = [
            {
                "id": "script.module.resolveurl.universal_debrid_priority",
                "value": 90,
                "description": "Set Real-Debrid priority to high"
            },
            {
                "id": "script.module.resolveurl.universal_debrid_timeout",
                "value": 30,
                "description": "Set timeout for debrid services"
            },
            {
                "id": "script.module.resolveurl.universal_source_timeout",
                "value": 20,
                "description": "Set source resolution timeout"
            },
            {
                "id": "script.module.resolveurl.universal_max_retries",
                "value": 3,
                "description": "Set maximum retries for sources"
            }
        ]

        for setting in settings_to_configure:
            print(f"Setting: {setting['description']}")

            result = self.send_request({
                "jsonrpc": "2.0",
                "method": "Settings.SetSettingValue",
                "params": {
                    "setting": setting["id"],
                    "value": setting["value"]
                },
                "id": 100
            })

            if "result" in result and result["result"]:
                print(f"  [OK] {setting['id']} = {setting['value']}")
            else:
                print(f"  [FAIL] Could not set {setting['id']}")

    def enable_free_sources(self):
        """Enable free streaming sources as fallback"""
        print("\nENABLING FREE STREAMING SOURCES")
        print("=" * 40)

        # Enable free sources in addons
        free_source_settings = [
            {
                "addon": "plugin.video.thecrew",
                "settings": [
                    {"id": "thecrew.enable_free_sources", "value": True},
                    {"id": "thecrew.source_timeout", "value": 30},
                    {"id": "thecrew.max_quality", "value": "1080p"}
                ]
            },
            {
                "addon": "plugin.video.fen.lite",
                "settings": [
                    {"id": "fenlite.enable_free_providers", "value": True},
                    {"id": "fenlite.timeout_free_sources", "value": 25},
                    {"id": "fenlite.quality_filter", "value": "HD"}
                ]
            }
        ]

        for addon_config in free_source_settings:
            print(f"Configuring {addon_config['addon']}:")

            for setting in addon_config["settings"]:
                setting_id = f"{addon_config['addon']}.{setting['id']}"

                result = self.send_request({
                    "jsonrpc": "2.0",
                    "method": "Settings.SetSettingValue",
                    "params": {
                        "setting": setting_id,
                        "value": setting["value"]
                    },
                    "id": 200
                })

                if "result" in result:
                    print(f"  [OK] {setting['id']} = {setting['value']}")
                else:
                    print(f"  [INFO] Setting {setting['id']} (may not exist)")

    def configure_kodi_cache_settings(self):
        """Optimize Kodi cache settings for streaming"""
        print("\nOPTIMIZING KODI CACHE SETTINGS")
        print("=" * 40)

        cache_settings = [
            {
                "id": "cache.buffermode",
                "value": 1,  # Buffer all internet filesystems
                "description": "Enable buffering for internet streams"
            },
            {
                "id": "cache.memorysize",
                "value": 104857600,  # 100MB
                "description": "Set video cache to 100MB"
            },
            {
                "id": "cache.readfactor",
                "value": 4,
                "description": "Set read ahead buffer factor"
            },
            {
                "id": "network.timeout",
                "value": 30,
                "description": "Set network timeout to 30 seconds"
            }
        ]

        for setting in cache_settings:
            print(f"Setting: {setting['description']}")

            result = self.send_request({
                "jsonrpc": "2.0",
                "method": "Settings.SetSettingValue",
                "params": {
                    "setting": setting["id"],
                    "value": setting["value"]
                },
                "id": 300
            })

            if "result" in result and result["result"]:
                print(f"  [OK] {setting['id']} = {setting['value']}")
            else:
                print(f"  [INFO] {setting['id']} (may require different approach)")

    def test_streaming_functionality(self):
        """Test basic streaming functionality"""
        print("\nTESTING STREAMING FUNCTIONALITY")
        print("=" * 40)

        # Test addon availability
        test_addons = [
            "plugin.video.thecrew",
            "plugin.video.fen.lite",
            "script.module.resolveurl"
        ]

        for addon_id in test_addons:
            result = self.send_request({
                "jsonrpc": "2.0",
                "method": "Addons.GetAddonDetails",
                "params": {
                    "addonid": addon_id,
                    "properties": ["enabled", "broken"]
                },
                "id": 400
            })

            if "result" in result and "addon" in result["result"]:
                addon = result["result"]["addon"]
                if addon["enabled"] and not addon["broken"]:
                    print(f"  [OK] {addon_id} is ready for streaming")
                else:
                    print(f"  [WARN] {addon_id} has issues (enabled: {addon['enabled']}, broken: {addon['broken']})")
            else:
                print(f"  [FAIL] Could not check {addon_id}")

    def create_real_debrid_setup_guide(self):
        """Create step-by-step Real-Debrid setup guide"""
        print("\nREAL-DEBRID SETUP GUIDE")
        print("=" * 40)

        guide_steps = [
            "1. SIGN UP FOR REAL-DEBRID:",
            "   - Visit https://real-debrid.com",
            "   - Create account or login",
            "   - Subscribe to premium service",
            "",
            "2. GET YOUR API KEY:",
            "   - Login to Real-Debrid website",
            "   - Go to https://real-debrid.com/apitoken",
            "   - Generate or copy your API token",
            "",
            "3. CONFIGURE IN KODI:",
            "   - Open Kodi Settings > Add-ons",
            "   - Find 'ResolveURL' in dependencies",
            "   - Go to Configure > Universal Resolvers",
            "   - Find 'Real-Debrid' section",
            "   - Enter your API token",
            "   - Set priority to 90",
            "   - Click 'Authorize Real-Debrid'",
            "",
            "4. CONFIGURE IN ADDONS:",
            "   - Open The Crew > Tools > Open Settings",
            "   - Go to Accounts section",
            "   - Enter Real-Debrid credentials",
            "   - Repeat for FEN Lite addon",
            "",
            "5. TEST STREAMING:",
            "   - Try playing any movie/TV show",
            "   - Look for 'RD' or 'Real-Debrid' in source names",
            "   - These sources should play instantly"
        ]

        for step in guide_steps:
            print(step)

    def run_full_configuration(self):
        """Run complete streaming configuration"""
        print("PIGEONHOLE STREAMING CONFIGURATOR")
        print("=" * 50)
        print(f"Target: {self.fire_tv_ip}:{self.http_port}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        # Test connection first
        result = self.send_request({
            "jsonrpc": "2.0",
            "method": "JSONRPC.Ping",
            "id": 1
        })

        if result.get("result") != "pong":
            print("[FAIL] Cannot connect to Kodi HTTP API")
            return False

        print("[OK] Connected to Kodi HTTP API")
        print()

        # Run configuration steps
        self.configure_resolveurl_settings()
        self.enable_free_sources()
        self.configure_kodi_cache_settings()
        self.test_streaming_functionality()
        self.create_real_debrid_setup_guide()

        print(f"\n[OK] Configuration completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\nNEXT STEPS:")
        print("1. Set up Real-Debrid account and API key (see guide above)")
        print("2. Restart Kodi to apply all settings")
        print("3. Test streaming with any addon")
        print("4. If issues persist, check addon-specific account settings")

        return True

if __name__ == "__main__":
    configurator = PigeonholeStreamingConfigurator()
    configurator.run_full_configuration()