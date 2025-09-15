#!/usr/bin/env python3
"""
Pigeonhole Streaming Diagnostic Tool
Comprehensive analysis of streaming functionality and configuration
"""

import requests
import json
import base64
import time
from datetime import datetime

class PigeonholeStreamingDiagnostic:
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

    def test_connection(self):
        """Test basic Kodi connection"""
        print("PIGEONHOLE STREAMING DIAGNOSTICS")
        print("=" * 50)
        print(f"Target: {self.fire_tv_ip}:{self.http_port}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        # Test ping
        result = self.send_request({
            "jsonrpc": "2.0",
            "method": "JSONRPC.Ping",
            "id": 1
        })

        if result.get("result") == "pong":
            print("[OK] Kodi HTTP API connection: WORKING")
            return True
        else:
            print("[FAIL] Kodi HTTP API connection: FAILED")
            print(f"   Error: {result}")
            return False

    def check_resolveurl_settings(self):
        """Check ResolveURL configuration"""
        print("\nRESOLVEURL CONFIGURATION CHECK")
        print("-" * 40)

        # Get ResolveURL settings
        result = self.send_request({
            "jsonrpc": "2.0",
            "method": "Settings.GetSettings",
            "params": {
                "filter": {"section": "addons", "category": "script.module.resolveurl"}
            },
            "id": 10
        })

        if "result" in result and "settings" in result["result"]:
            settings = result["result"]["settings"]
            print(f"[OK] Found {len(settings)} ResolveURL settings")

            # Check for critical settings
            critical_settings = [
                "script.module.resolveurl.universal_debrid_priority",
                "script.module.resolveurl.real_debrid_enabled",
                "script.module.resolveurl.real_debrid_api_key"
            ]

            for setting in settings:
                setting_id = setting.get("id", "")
                if any(critical in setting_id for critical in critical_settings):
                    value = setting.get("value", "Not set")
                    if "api_key" in setting_id and value and value != "Not set":
                        value = f"{'*' * (len(str(value)) - 4)}{str(value)[-4:]}"  # Mask API key
                    print(f"   {setting_id}: {value}")
        else:
            print("[FAIL] Could not retrieve ResolveURL settings")

    def check_addon_settings(self, addon_id, addon_name):
        """Check specific addon settings"""
        print(f"\n{addon_name.upper()} SETTINGS")
        print("-" * 40)

        result = self.send_request({
            "jsonrpc": "2.0",
            "method": "Addons.GetAddonDetails",
            "params": {
                "addonid": addon_id,
                "properties": ["enabled", "broken", "version", "dependencies"]
            },
            "id": 20
        })

        if "result" in result and "addon" in result["result"]:
            addon = result["result"]["addon"]
            print(f"[OK] {addon_name} v{addon['version']}")
            print(f"   Enabled: {addon['enabled']}")
            print(f"   Broken: {addon['broken']}")

            if "dependencies" in addon:
                print(f"   Dependencies: {len(addon['dependencies'])} modules")
                for dep in addon["dependencies"]:
                    print(f"     - {dep['addonid']} (v{dep['version']})")
        else:
            print(f"[FAIL] Could not get {addon_name} details")

    def test_streaming_sources(self):
        """Test streaming source resolution"""
        print("\nSTREAMING SOURCE TEST")
        print("-" * 40)

        # Try to get video addons
        result = self.send_request({
            "jsonrpc": "2.0",
            "method": "Addons.GetAddons",
            "params": {
                "type": "xbmc.addon.video",
                "properties": ["name", "enabled", "broken"]
            },
            "id": 30
        })

        if "result" in result and "addons" in result["result"]:
            video_addons = result["result"]["addons"]
            enabled_addons = [addon for addon in video_addons if addon["enabled"] and not addon["broken"]]
            print(f"[OK] Found {len(enabled_addons)} enabled video addons:")

            for addon in enabled_addons[:10]:  # Show first 10
                print(f"   - {addon['name']} ({addon['addonid']})")

            if len(enabled_addons) > 10:
                print(f"   ... and {len(enabled_addons) - 10} more")
        else:
            print("[FAIL] Could not retrieve video addons")

    def check_network_connectivity(self):
        """Check network connectivity to common streaming services"""
        print("\nNETWORK CONNECTIVITY TEST")
        print("-" * 40)

        test_urls = [
            "real-debrid.com",
            "premiumize.me",
            "alldebrid.com",
            "github.com"
        ]

        for url in test_urls:
            try:
                response = requests.get(f"https://{url}", timeout=10)
                status = "[OK] REACHABLE" if response.status_code < 400 else f"[WARN] HTTP {response.status_code}"
                print(f"   {url}: {status}")
            except Exception as e:
                print(f"   {url}: [FAIL] UNREACHABLE ({str(e)[:50]}...)")

    def check_kodi_logs(self):
        """Check for recent Kodi log entries related to streaming"""
        print("\nRECENT LOG ANALYSIS")
        print("-" * 40)

        # Get log entries (this is a simplified check)
        result = self.send_request({
            "jsonrpc": "2.0",
            "method": "System.GetInfoLabels",
            "params": {
                "labels": [
                    "System.LogLevel",
                    "System.BuildDate"
                ]
            },
            "id": 40
        })

        if "result" in result:
            info = result["result"]
            print(f"[OK] Log Level: {info.get('System.LogLevel', 'Unknown')}")
            print(f"[OK] Build Date: {info.get('System.BuildDate', 'Unknown')}")
        else:
            print("[FAIL] Could not retrieve log information")

    def generate_fix_recommendations(self):
        """Generate specific fix recommendations"""
        print("\nSTREAMING FIX RECOMMENDATIONS")
        print("=" * 50)

        recommendations = [
            {
                "priority": "HIGH",
                "issue": "Real-Debrid Configuration",
                "solution": "Configure Real-Debrid API key in ResolveURL settings",
                "steps": [
                    "1. Open Kodi Settings → Add-ons → ResolveURL",
                    "2. Go to Universal Resolvers → Real-Debrid",
                    "3. Enter your Real-Debrid API key",
                    "4. Set priority to High (80-90)",
                    "5. Test authorization"
                ]
            },
            {
                "priority": "HIGH",
                "issue": "Provider Settings",
                "solution": "Configure addon provider accounts",
                "steps": [
                    "1. Open The Crew → Tools → Accounts",
                    "2. Configure Real-Debrid account",
                    "3. Open FEN Lite → Settings → Accounts",
                    "4. Link Real-Debrid service",
                    "5. Verify authentication status"
                ]
            },
            {
                "priority": "MEDIUM",
                "issue": "Free Backup Sources",
                "solution": "Enable free streaming sources as fallback",
                "steps": [
                    "1. In addon settings, enable free sources",
                    "2. Set timeout values for source resolution",
                    "3. Configure source priorities",
                    "4. Test with popular content"
                ]
            },
            {
                "priority": "LOW",
                "issue": "Cache & Performance",
                "solution": "Optimize cache settings for streaming",
                "steps": [
                    "1. Set video cache size to 100MB+",
                    "2. Enable read ahead buffer",
                    "3. Configure network timeout settings",
                    "4. Clear addon cache if needed"
                ]
            }
        ]

        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. [{rec['priority']}] {rec['issue']}")
            print(f"   Solution: {rec['solution']}")
            for step in rec['steps']:
                print(f"   {step}")

    def run_full_diagnostic(self):
        """Run complete streaming diagnostic"""
        if not self.test_connection():
            return False

        # Core checks
        self.check_resolveurl_settings()
        self.check_addon_settings("plugin.video.thecrew", "The Crew")
        self.check_addon_settings("plugin.video.fen.lite", "FEN Lite")
        self.test_streaming_sources()
        self.check_network_connectivity()
        self.check_kodi_logs()

        # Generate recommendations
        self.generate_fix_recommendations()

        print(f"\n[OK] Diagnostic completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return True

if __name__ == "__main__":
    diagnostic = PigeonholeStreamingDiagnostic()
    diagnostic.run_full_diagnostic()