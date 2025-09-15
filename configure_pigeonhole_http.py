#!/usr/bin/env python3
"""
Pigeonhole HTTP Configuration System
Configure Kodi for optimal streaming via HTTP API
"""

import requests
import json
import time
from requests.auth import HTTPBasicAuth

class PigeonholeHTTPConfig:
    def __init__(self, host="192.168.1.130", port=8080, username="kodi", password="0000"):
        self.base_url = f"http://{host}:{port}/jsonrpc"
        self.auth = HTTPBasicAuth(username, password)
        self.headers = {"Content-Type": "application/json"}

    def send_command(self, method, params=None):
        """Send JSON-RPC command to Kodi"""
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": 1
        }

        try:
            response = requests.post(
                self.base_url,
                data=json.dumps(payload),
                headers=self.headers,
                auth=self.auth,
                timeout=10
            )
            result = response.json()
            return result
        except Exception as e:
            print(f"Error: {e}")
            return None

    def configure_cache_settings(self):
        """Configure optimal cache settings for Fire TV Cube"""
        print("Configuring cache settings...")

        # Network buffer settings
        settings = [
            ("network.buffermode", 1),
            ("network.cachemembuffersize", 209715200),  # 200MB
            ("network.readbufferfactor", 4.0),
            ("network.httpproxytype", 0),
            ("network.httpproxyserver", ""),
            ("network.httpproxyport", 8080),
            ("network.httpproxyusername", ""),
            ("network.httpproxypassword", ""),
            ("network.bandwidth", 0),
            ("network.usehttpproxy", False)
        ]

        success_count = 0
        for setting, value in settings:
            result = self.send_command("Settings.SetSettingValue", {"setting": setting, "value": value})
            if result and "result" in result:
                print(f"  Set {setting}: OK")
                success_count += 1
            else:
                print(f"  Set {setting}: FAILED")
            time.sleep(0.5)

        print(f"Cache configuration: {success_count}/{len(settings)} settings applied")
        return success_count > len(settings) * 0.7

    def configure_video_settings(self):
        """Configure video playback settings"""
        print("Configuring video settings...")

        settings = [
            ("videoplayer.adjustrefreshrate", 2),
            ("videoplayer.usedisplayasclock", 2),
            ("videoplayer.errorinaspect", 0),
            ("videoplayer.stretch43", 0),
            ("videoplayer.rendermethod", 0),
            ("videoplayer.usevaapi", False),
            ("videoplayer.usevdpau", False)
        ]

        success_count = 0
        for setting, value in settings:
            result = self.send_command("Settings.SetSettingValue", {"setting": setting, "value": value})
            if result and "result" in result:
                print(f"  Set {setting}: OK")
                success_count += 1
            else:
                print(f"  Set {setting}: FAILED")
            time.sleep(0.5)

        print(f"Video configuration: {success_count}/{len(settings)} settings applied")
        return success_count > len(settings) * 0.7

    def configure_general_settings(self):
        """Configure general Kodi settings"""
        print("Configuring general settings...")

        settings = [
            ("locale.timezone", "Australia/Sydney"),
            ("locale.timezonecountry", "Australia"),
            ("locale.language", "resource.language.en_gb"),
            ("services.webserver", True),
            ("services.webserverport", 8080),
            ("services.webserverusername", "kodi"),
            ("services.webserverpassword", "0000"),
            ("services.zeroconf", True)
        ]

        success_count = 0
        for setting, value in settings:
            result = self.send_command("Settings.SetSettingValue", {"setting": setting, "value": value})
            if result and "result" in result:
                print(f"  Set {setting}: OK")
                success_count += 1
            else:
                print(f"  Set {setting}: FAILED")
            time.sleep(0.5)

        print(f"General configuration: {success_count}/{len(settings)} settings applied")
        return success_count > len(settings) * 0.7

    def install_addon_sources(self):
        """Add addon sources/repositories"""
        print("Adding addon sources...")

        # Add file sources for repositories
        sources = [
            {
                "name": "Magnetic Repository",
                "path": "https://magnetic.website/"
            },
            {
                "name": "FEN Light Repository",
                "path": "https://fenlightanonymouse.github.io/"
            }
        ]

        for source in sources:
            # Add source
            params = {
                "source": {
                    "name": source["name"],
                    "path": source["path"]
                }
            }
            result = self.send_command("Files.AddSource", params)
            print(f"  Added source {source['name']}: {'OK' if result and 'result' in result else 'FAILED'}")
            time.sleep(1)

    def enable_existing_addons(self):
        """Enable any existing relevant addons"""
        print("Enabling existing addons...")

        # Get all addons
        result = self.send_command("Addons.GetAddons", {"type": "unknown"})
        if not result or "result" not in result:
            print("  Could not get addon list")
            return

        addons = result["result"].get("addons", [])

        # Look for relevant addons
        relevant_patterns = ["resolve", "crew", "fen", "pigeonhole", "arctic", "zephyr"]
        enabled_count = 0

        for addon in addons:
            addon_id = addon["addonid"]
            addon_name = addon.get("name", "").lower()

            # Check if this is a relevant addon
            is_relevant = any(pattern in addon_id.lower() or pattern in addon_name for pattern in relevant_patterns)

            if is_relevant:
                # Try to enable it
                enable_result = self.send_command("Addons.SetAddonEnabled", {"addonid": addon_id, "enabled": True})
                if enable_result and "result" in enable_result:
                    print(f"  Enabled {addon_id}: OK")
                    enabled_count += 1
                else:
                    print(f"  Enable {addon_id}: FAILED")
                time.sleep(0.5)

        print(f"Enabled {enabled_count} relevant addons")
        return enabled_count

    def test_streaming_readiness(self):
        """Test if system is ready for streaming"""
        print("Testing streaming readiness...")

        # Test video addon availability
        result = self.send_command("Addons.GetAddons", {"type": "xbmc.addon.video"})
        video_addons = 0
        if result and "result" in result:
            video_addons = len(result["result"].get("addons", []))

        print(f"  Video addons available: {video_addons}")

        # Test if we can execute addon
        if video_addons > 0:
            test_result = self.send_command("Addons.ExecuteAddon", {"addonid": "plugin.video.youtube", "wait": False})
            can_execute = test_result and "result" in test_result
            print(f"  Addon execution test: {'PASS' if can_execute else 'FAIL'}")

        # Test network connectivity
        network_result = self.send_command("JSONRPC.Ping")
        network_ok = network_result and network_result.get("result") == "pong"
        print(f"  Network connectivity: {'PASS' if network_ok else 'FAIL'}")

        return video_addons > 0 and network_ok

    def run_full_configuration(self):
        """Run complete Pigeonhole configuration"""
        print("=" * 60)
        print("PIGEONHOLE HTTP CONFIGURATION SYSTEM")
        print("=" * 60)

        # Test connection
        print("\nTesting HTTP connection...")
        ping_result = self.send_command("JSONRPC.Ping")
        if not ping_result or ping_result.get("result") != "pong":
            print("ERROR: Cannot connect to Kodi HTTP API")
            return False

        print("Connection OK!")

        # Run configuration steps
        steps = [
            ("Cache Settings", self.configure_cache_settings),
            ("Video Settings", self.configure_video_settings),
            ("General Settings", self.configure_general_settings),
            ("Addon Sources", self.install_addon_sources),
            ("Enable Addons", self.enable_existing_addons),
            ("Streaming Test", self.test_streaming_readiness)
        ]

        results = []
        print(f"\nRunning {len(steps)} configuration steps...")

        for step_name, step_func in steps:
            print(f"\n--- {step_name} ---")
            try:
                result = step_func()
                results.append(result)
                print(f"{step_name}: {'SUCCESS' if result else 'PARTIAL'}")
            except Exception as e:
                print(f"{step_name}: ERROR - {e}")
                results.append(False)

        # Summary
        success_count = sum(1 for r in results if r)
        success_rate = (success_count / len(steps)) * 100

        print("\n" + "=" * 60)
        print("CONFIGURATION COMPLETE")
        print("=" * 60)
        print(f"Success Rate: {success_rate:.1f}% ({success_count}/{len(steps)} steps)")

        if success_rate >= 70:
            print("\nSUCCESS: Pigeonhole system configured!")
            print("Your Fire TV is ready for streaming.")
            print("\nNext steps:")
            print("1. Install streaming addons from Kodi addon browser")
            print("2. Configure Real-Debrid for premium streaming")
            print("3. Test streaming with popular content")
        else:
            print("\nPARTIAL: Some configuration steps failed")
            print("The system may still work but manual setup may be needed")

        return success_rate >= 70

if __name__ == "__main__":
    config = PigeonholeHTTPConfig()
    success = config.run_full_configuration()

    if success:
        print("\nConfiguration successful!")
    else:
        print("\nConfiguration needs attention")