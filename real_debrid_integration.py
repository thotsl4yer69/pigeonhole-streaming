#!/usr/bin/env python3
"""
Real-Debrid Integration for Pigeonhole Project
Direct configuration and testing of Real-Debrid services
"""

import requests
import json
import base64
import time
from datetime import datetime

class RealDebridIntegration:
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

    def execute_addon_function(self, addon_id, function_name, params=None):
        """Execute a specific function in an addon"""
        if params is None:
            params = []

        result = self.send_request({
            "jsonrpc": "2.0",
            "method": "Addons.ExecuteAddon",
            "params": {
                "addonid": addon_id,
                "params": params,
                "wait": True
            },
            "id": 500
        })
        return result

    def open_resolveurl_settings(self):
        """Open ResolveURL settings directly"""
        print("OPENING RESOLVEURL SETTINGS")
        print("=" * 40)

        # Try to open ResolveURL settings
        result = self.send_request({
            "jsonrpc": "2.0",
            "method": "Addons.ExecuteAddon",
            "params": {
                "addonid": "script.module.resolveurl",
                "params": ["settings"],
                "wait": False
            },
            "id": 510
        })

        if "result" in result:
            print("[OK] ResolveURL settings opened")
            print("MANUAL STEPS REQUIRED:")
            print("1. Navigate to 'Universal Resolvers'")
            print("2. Find 'Real-Debrid' section")
            print("3. Enter your Real-Debrid API token")
            print("4. Set priority to 90")
            print("5. Click 'Authorize Real-Debrid'")
            return True
        else:
            print(f"[FAIL] Could not open ResolveURL settings: {result}")
            return False

    def configure_addon_accounts(self):
        """Configure addon account settings"""
        print("\nCONFIGURING ADDON ACCOUNTS")
        print("=" * 40)

        addons_to_configure = [
            {
                "id": "plugin.video.thecrew",
                "name": "The Crew",
                "settings_path": ["tools", "open_settings"],
                "account_section": "Accounts"
            },
            {
                "id": "plugin.video.fen.lite",
                "name": "FEN Lite",
                "settings_path": ["settings"],
                "account_section": "Accounts"
            }
        ]

        for addon in addons_to_configure:
            print(f"\nConfiguring {addon['name']}:")

            # Try to open addon
            result = self.send_request({
                "jsonrpc": "2.0",
                "method": "Addons.ExecuteAddon",
                "params": {
                    "addonid": addon["id"],
                    "wait": False
                },
                "id": 520
            })

            if "result" in result:
                print(f"  [OK] {addon['name']} opened")
                print(f"  MANUAL STEPS: Navigate to {addon['account_section']} > Real-Debrid")
            else:
                print(f"  [FAIL] Could not open {addon['name']}")

    def test_free_streaming_sources(self):
        """Test free streaming sources availability"""
        print("\nTESTING FREE STREAMING SOURCES")
        print("=" * 40)

        # Test by trying to get sources for a popular movie
        test_content = {
            "title": "Interstellar",
            "year": "2014",
            "imdb": "tt0816692"
        }

        print(f"Testing with: {test_content['title']} ({test_content['year']})")

        # This is a basic test - in reality, we'd need to call addon-specific functions
        # For now, we'll just verify the addons are functional
        addons_to_test = [
            "plugin.video.thecrew",
            "plugin.video.fen.lite"
        ]

        for addon_id in addons_to_test:
            result = self.send_request({
                "jsonrpc": "2.0",
                "method": "Addons.GetAddonDetails",
                "params": {
                    "addonid": addon_id,
                    "properties": ["enabled", "broken", "version"]
                },
                "id": 530
            })

            if "result" in result and "addon" in result["result"]:
                addon = result["result"]["addon"]
                status = "[OK]" if addon["enabled"] and not addon["broken"] else "[ISSUE]"
                print(f"  {status} {addon_id} v{addon['version']}")

                if addon["enabled"] and not addon["broken"]:
                    print(f"    Ready for free source testing")
            else:
                print(f"  [FAIL] Could not check {addon_id}")

    def create_streaming_test_script(self):
        """Create a script to test streaming functionality"""
        print("\nCREATING STREAMING TEST PROCEDURE")
        print("=" * 40)

        test_procedure = """
STREAMING TEST PROCEDURE:

1. TEST THE CREW:
   - Open The Crew addon
   - Navigate to Movies > Popular
   - Select any recent movie
   - Click play and check for sources
   - Look for these source types:
     * Free sources (no prefix)
     * Real-Debrid sources (RD prefix)
     * Other premium sources

2. TEST FEN LITE:
   - Open FEN Lite addon
   - Navigate to Movies > Trending
   - Select any movie
   - Look for source quality indicators:
     * 720p, 1080p sources
     * File size information
     * Source reliability

3. VERIFY PLAYBACK:
   - Sources should resolve within 30 seconds
   - Video should start playing smoothly
   - No buffering on good internet connection
   - Audio and video sync should be correct

4. TROUBLESHOOTING IF NO SOURCES:
   - Check internet connection
   - Verify addon settings
   - Clear addon cache
   - Restart Kodi and try again

5. IF REAL-DEBRID NOT WORKING:
   - Verify API key in ResolveURL
   - Check Real-Debrid account status
   - Ensure subscription is active
   - Test authorization in ResolveURL
        """

        print(test_procedure)

    def perform_streaming_diagnostics(self):
        """Perform comprehensive streaming diagnostics"""
        print("STREAMING DIAGNOSTICS SUMMARY")
        print("=" * 50)

        # Check basic connectivity
        ping_result = self.send_request({
            "jsonrpc": "2.0",
            "method": "JSONRPC.Ping",
            "id": 1
        })

        if ping_result.get("result") == "pong":
            print("[OK] Kodi HTTP API responding")
        else:
            print("[FAIL] Cannot connect to Kodi")
            return False

        # Check critical addons
        critical_addons = [
            "script.module.resolveurl",
            "plugin.video.thecrew",
            "plugin.video.fen.lite"
        ]

        addon_status = {}
        for addon_id in critical_addons:
            result = self.send_request({
                "jsonrpc": "2.0",
                "method": "Addons.GetAddonDetails",
                "params": {
                    "addonid": addon_id,
                    "properties": ["enabled", "broken", "version"]
                },
                "id": 600
            })

            if "result" in result and "addon" in result["result"]:
                addon = result["result"]["addon"]
                addon_status[addon_id] = {
                    "enabled": addon["enabled"],
                    "broken": addon["broken"],
                    "version": addon["version"],
                    "status": "OK" if addon["enabled"] and not addon["broken"] else "ISSUE"
                }
            else:
                addon_status[addon_id] = {"status": "MISSING"}

        print("\nADDON STATUS:")
        for addon_id, status in addon_status.items():
            if status["status"] == "OK":
                print(f"  [OK] {addon_id} v{status['version']}")
            elif status["status"] == "ISSUE":
                print(f"  [ISSUE] {addon_id} (enabled: {status['enabled']}, broken: {status['broken']})")
            else:
                print(f"  [MISSING] {addon_id}")

        # Check if all critical addons are OK
        all_ok = all(status.get("status") == "OK" for status in addon_status.values())

        if all_ok:
            print(f"\n[OK] All critical addons are functional")
            print("STREAMING CAPABILITY: READY FOR CONFIGURATION")
        else:
            print(f"\n[WARN] Some addons have issues")
            print("STREAMING CAPABILITY: NEEDS ATTENTION")

        return all_ok

    def run_integration_setup(self):
        """Run complete Real-Debrid integration setup"""
        print("REAL-DEBRID INTEGRATION SETUP")
        print("=" * 50)
        print(f"Target: {self.fire_tv_ip}:{self.http_port}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        # Perform diagnostics first
        if not self.perform_streaming_diagnostics():
            print("\n[FAIL] Diagnostics failed - fix addon issues first")
            return False

        print()

        # Setup procedures
        self.open_resolveurl_settings()
        self.configure_addon_accounts()
        self.test_free_streaming_sources()
        self.create_streaming_test_script()

        print(f"\n[OK] Integration setup completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\nIMPORTANT NEXT STEPS:")
        print("1. Complete Real-Debrid configuration in ResolveURL (see output above)")
        print("2. Configure Real-Debrid in each addon (The Crew, FEN Lite)")
        print("3. Restart Kodi to ensure all settings take effect")
        print("4. Test streaming with the procedure provided above")
        print("5. Free sources should work immediately without Real-Debrid")

        return True

if __name__ == "__main__":
    integration = RealDebridIntegration()
    integration.run_integration_setup()