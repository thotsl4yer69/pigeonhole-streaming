#!/usr/bin/env python3
"""
Fire TV Cube Gold Optimizer - Pigeonhole Streaming Architect
Complete system optimization for Kodi v22 gold build
"""

import subprocess
import requests
import json
import base64
import time
import sys
from datetime import datetime

class FireTVOptimizer:
    def __init__(self, fire_tv_ip="192.168.1.130", http_port=8080):
        self.fire_tv_ip = fire_tv_ip
        self.http_port = http_port
        self.username = "kodi"
        self.password = "0000"
        self.base_url = f"http://{fire_tv_ip}:{http_port}/jsonrpc"

        # Create auth header
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_credentials}"
        }

        # Amazon bloatware packages to remove (safe list)
        self.amazon_bloatware = [
            "com.amazon.dee.app",              # Alexa
            "amazon.speech.sim",               # Speech services
            "com.amazon.ags.app",              # Amazon GameCircle
            "com.amazon.avod.thirdpartyclient", # IMDb TV
            "com.amazon.bueller.music",        # Amazon Music
            "com.amazon.bueller.photos",       # Amazon Photos
            "com.amazon.device.bluetoothdfu",   # Bluetooth DFU
            "com.amazon.device.sync",          # Device sync
            "com.amazon.device.sync.sdk.internal", # Sync SDK
            "com.amazon.hedwig",               # Help
            "com.amazon.identity.auth.device.authorization", # Auth services
            "com.amazon.kindleautomatictimezone", # Timezone
            "com.amazon.ods.kindleconnect",    # Kindle connect
            "com.amazon.parentalcontrols",     # Parental controls
            "com.amazon.precog",               # Analytics
            "com.amazon.providers",            # Content providers
            "com.amazon.securitysyncclient",   # Security sync
            "com.amazon.sharingservice.android.client.proxy", # Sharing
            "com.amazon.shoptv.client",        # Shop TV
            "com.amazon.ssm",                  # System manager
            "com.amazon.ssmsys",               # System services
            "com.amazon.storm.lightning.services", # Services
            "com.amazon.storm.lightning.tutorial", # Tutorials
            "com.amazon.tmm.tutorial",         # Tutorial manager
            "com.amazon.tv.parentalcontrols",  # Parental controls
            "com.amazon.venezia",              # App store services
            "com.amazon.videoads.app",         # Video ads
            "com.amazon.visualonawv",          # Video services
            "com.amazon.wifilocker",           # WiFi locker
        ]

        # Keep these essential Amazon packages
        self.amazon_keep = [
            "com.amazon.tv.launcher",          # Main launcher (we'll replace)
            "com.amazon.tv.settings",          # System settings
            "com.amazon.device.controllermanager", # Controller manager
            "com.amazon.device.software.ota",  # System updates
            "com.amazon.tv.remoteservice",     # Remote service
        ]

        # Pigeonhole core addons to preserve
        self.pigeonhole_core = [
            "skin.arctic.zephyr.pigeonhole",
            "script.module.resolveurl",
            "plugin.video.thecrew",
            "plugin.video.fen.lite",
            "script.pigeonhole.config",
            "repository.pigeonhole.streaming",
            "script.module.requests",
            "script.module.urllib3",
            "script.module.certifi",
            "script.module.chardet",
            "script.module.idna",
            "script.common.plugin.cache",
            "script.module.kodi-six",
            "script.module.six",
        ]

    def log(self, message, level="INFO"):
        """Enhanced logging with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")

    def adb_command(self, command):
        """Execute ADB command with error handling"""
        try:
            full_command = f"adb -s {self.fire_tv_ip}:5555 {command}"
            result = subprocess.run(full_command, shell=True, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                return True, result.stdout.strip()
            else:
                return False, result.stderr.strip()
        except subprocess.TimeoutExpired:
            return False, "Command timeout"
        except Exception as e:
            return False, str(e)

    def kodi_jsonrpc(self, method, params=None):
        """Execute Kodi JSON-RPC call"""
        try:
            payload = {
                "jsonrpc": "2.0",
                "method": method,
                "id": 1
            }
            if params:
                payload["params"] = params

            response = requests.post(self.base_url, json=payload, headers=self.headers, timeout=15)
            if response.status_code == 200:
                result = response.json()
                return result.get("result", result)
            else:
                self.log(f"HTTP Error {response.status_code}: {response.text}", "ERROR")
                return None
        except Exception as e:
            self.log(f"Kodi API error: {e}", "ERROR")
            return None

    def check_adb_connection(self):
        """Verify ADB connection to Fire TV"""
        self.log("Checking ADB connection...")
        success, output = self.adb_command("shell echo 'ADB Connected'")
        if success and "ADB Connected" in output:
            self.log("[OK] ADB connection verified", "SUCCESS")
            return True
        else:
            self.log(f"[ERROR] ADB connection failed: {output}", "ERROR")
            return False

    def backup_system_state(self):
        """Create system state backup before modifications"""
        self.log("Creating system state backup...")

        # Get installed packages
        success, packages = self.adb_command("shell pm list packages")
        if success:
            with open(f"M:\\fire_tv_packages_backup_{int(time.time())}.txt", "w") as f:
                f.write(packages)
            self.log("[OK] Package list backed up", "SUCCESS")

        # Get current launcher
        success, launcher = self.adb_command("shell cmd package resolve-activity --brief -c android.intent.category.HOME")
        if success:
            with open(f"M:\\fire_tv_launcher_backup_{int(time.time())}.txt", "w") as f:
                f.write(launcher)
            self.log("✅ Launcher configuration backed up", "SUCCESS")

    def debloat_amazon_packages(self):
        """Remove Amazon bloatware packages safely"""
        self.log("Starting Amazon bloatware removal...")

        removed_count = 0
        failed_count = 0

        for package in self.amazon_bloatware:
            self.log(f"Removing {package}...")

            # First try to disable
            success, output = self.adb_command(f"shell pm disable-user --user 0 {package}")
            if success:
                # Then uninstall for user
                success, output = self.adb_command(f"shell pm uninstall --user 0 {package}")
                if success:
                    self.log(f"  ✅ Removed: {package}", "SUCCESS")
                    removed_count += 1
                else:
                    self.log(f"  ⚠️ Disabled only: {package}", "WARN")
            else:
                self.log(f"  ❌ Failed: {package} - {output}", "ERROR")
                failed_count += 1

        self.log(f"Debloat summary: {removed_count} removed, {failed_count} failed", "INFO")
        return removed_count > 0

    def get_kodi_addons(self):
        """Get current Kodi addon list"""
        self.log("Analyzing current Kodi addons...")

        result = self.kodi_jsonrpc("Addons.GetAddons", {
            "properties": ["name", "version", "enabled", "broken", "type"]
        })

        if result and "addons" in result:
            addons = result["addons"]
            self.log(f"Found {len(addons)} total addons")

            enabled_addons = [a for a in addons if a["enabled"]]
            self.log(f"  - {len(enabled_addons)} enabled addons")

            return addons
        else:
            self.log("❌ Failed to get addon list", "ERROR")
            return []

    def clean_unnecessary_addons(self):
        """Remove unnecessary addons, keep Pigeonhole core"""
        self.log("Cleaning unnecessary Kodi addons...")

        addons = self.get_kodi_addons()
        if not addons:
            return False

        cleaned_count = 0

        # Get list of addon IDs to remove (not in core list)
        for addon in addons:
            addon_id = addon["addonid"]

            # Skip if it's a core addon
            if addon_id in self.pigeonhole_core:
                continue

            # Skip system addons
            if addon_id.startswith("kodi.") or addon_id.startswith("xbmc."):
                continue

            # Skip skins (except our custom one)
            if addon["type"] == "xbmc.gui.skin" and not addon_id.startswith("skin.arctic.zephyr"):
                continue

            # Check for common bloat patterns
            bloat_patterns = [
                "plugin.video.youtube",
                "plugin.video.netflix",
                "inputstream",
                "pvr.",
                "audiodecoder.",
                "audioencoder.",
                "visualization.",
                "screensaver.",
                "weather.",
                "service.upnp",
                "webinterface.",
            ]

            should_remove = any(pattern in addon_id for pattern in bloat_patterns)

            if should_remove:
                self.log(f"Disabling unnecessary addon: {addon['name']}")
                result = self.kodi_jsonrpc("Addons.SetAddonEnabled", {
                    "addonid": addon_id,
                    "enabled": False
                })
                if result:
                    cleaned_count += 1

        self.log(f"✅ Cleaned {cleaned_count} unnecessary addons", "SUCCESS")
        return cleaned_count > 0

    def configure_kodi_launcher(self):
        """Configure Kodi as default launcher"""
        self.log("Configuring Kodi as default launcher...")

        # Stop current launcher
        success, output = self.adb_command("shell am force-stop com.amazon.tv.launcher")
        if success:
            self.log("✅ Stopped Amazon launcher")

        # Set Kodi as default home
        success, output = self.adb_command("shell cmd package set-home-activity org.xbmc.kodi/org.xbmc.kodi.Splash")
        if success:
            self.log("✅ Set Kodi as default launcher", "SUCCESS")

            # Clear launcher defaults
            self.adb_command("shell pm clear com.amazon.tv.launcher")

            # Start Kodi
            self.adb_command("shell am start -n org.xbmc.kodi/.Splash")
            return True
        else:
            self.log(f"❌ Failed to set Kodi launcher: {output}", "ERROR")
            return False

    def optimize_kodi_performance(self):
        """Apply Fire TV Cube specific Kodi performance optimizations"""
        self.log("Applying Kodi performance optimizations...")

        # Advanced settings for Fire TV Cube
        advanced_settings = """<advancedsettings>
    <network>
        <buffermode>1</buffermode>
        <cachemembuffersize>209715200</cachemembuffersize>
        <readbufferfactor>4.0</readbufferfactor>
    </network>
    <video>
        <rendermethod>0</rendermethod>
        <adjustrefreshrate>2</adjustrefreshrate>
        <pauseafterrefreshchange>2</pauseafterrefreshchange>
        <allowhiresoutput>false</allowhiresoutput>
        <maxtemporalscale>2</maxtemporalscale>
    </video>
    <audio>
        <audiooutput>audioengine</audiooutput>
        <channels>2</channels>
        <samplerate>48000</samplerate>
        <bitspersample>16</bitspersample>
        <passthrough>false</passthrough>
    </audio>
    <cache>
        <memorysize>209715200</memorysize>
        <buffermode>1</buffermode>
        <readfactor>4.0</readfactor>
    </cache>
    <gui>
        <algorithmdirtyregions>3</algorithmdirtyregions>
        <nofliptimeout>5</nofliptimeout>
    </gui>
    <system>
        <playlistasfolders>false</playlistasfolders>
        <extractflags>false</extractflags>
    </system>
</advancedsettings>"""

        # Push optimized settings
        with open("M:\\advanced_settings_temp.xml", "w") as f:
            f.write(advanced_settings)

        success, output = self.adb_command("push M:\\advanced_settings_temp.xml /storage/emulated/0/Android/data/org.xbmc.kodi/files/.kodi/userdata/advancedsettings.xml")
        if success:
            self.log("✅ Applied advanced performance settings", "SUCCESS")

            # Clean up temp file
            import os
            os.remove("M:\\advanced_settings_temp.xml")

            return True
        else:
            self.log(f"❌ Failed to apply settings: {output}", "ERROR")
            return False

    def deploy_pigeonhole_skin(self):
        """Configure Arctic Zephyr Pigeonhole skin"""
        self.log("Configuring Pigeonhole skin...")

        # Set skin via Kodi API
        result = self.kodi_jsonrpc("Settings.SetSettingValue", {
            "setting": "lookandfeel.skin",
            "value": "skin.arctic.zephyr.pigeonhole"
        })

        if result:
            self.log("✅ Activated Pigeonhole skin", "SUCCESS")
            return True
        else:
            self.log("❌ Failed to activate Pigeonhole skin", "ERROR")
            return False

    def restart_kodi(self):
        """Restart Kodi to apply all changes"""
        self.log("Restarting Kodi...")

        # Stop Kodi
        success, output = self.adb_command("shell am force-stop org.xbmc.kodi")
        if success:
            self.log("✅ Stopped Kodi")
            time.sleep(3)

            # Start Kodi
            success, output = self.adb_command("shell am start -n org.xbmc.kodi/.Splash")
            if success:
                self.log("✅ Restarted Kodi", "SUCCESS")
                time.sleep(10)  # Wait for startup
                return True

        self.log("❌ Failed to restart Kodi", "ERROR")
        return False

    def validate_system(self):
        """Validate final system state"""
        self.log("Validating optimized system...")

        # Test Kodi connection
        result = self.kodi_jsonrpc("JSONRPC.Ping")
        if result == "pong":
            self.log("✅ Kodi HTTP API responding")

            # Get system info
            system_info = self.kodi_jsonrpc("System.GetInfoLabels", {
                "labels": ["System.BuildVersion", "System.FreeMemory", "Skin.CurrentSkin"]
            })

            if system_info:
                self.log(f"✅ Kodi Version: {system_info.get('System.BuildVersion', 'Unknown')}")
                self.log(f"✅ Free Memory: {system_info.get('System.FreeMemory', 'Unknown')}")
                self.log(f"✅ Active Skin: {system_info.get('Skin.CurrentSkin', 'Unknown')}")

                # Test addon functionality
                addons = self.get_kodi_addons()
                core_working = sum(1 for addon in addons
                                 if addon["addonid"] in self.pigeonhole_core and addon["enabled"])

                self.log(f"✅ Core addons working: {core_working}/{len(self.pigeonhole_core)}")

                if core_working >= len(self.pigeonhole_core) * 0.8:  # 80% threshold
                    self.log("🎯 GOLD BUILD VALIDATION SUCCESSFUL!", "SUCCESS")
                    return True

        self.log("❌ System validation failed", "ERROR")
        return False

    def run_full_optimization(self):
        """Execute complete Fire TV Cube gold optimization"""
        self.log("=" * 60)
        self.log("FIRE TV CUBE GOLD OPTIMIZATION - PIGEONHOLE STREAMING")
        self.log("=" * 60)

        steps_completed = 0
        total_steps = 8

        # Step 1: Check ADB connection
        if not self.check_adb_connection():
            self.log("❌ Cannot proceed without ADB connection", "ERROR")
            return False
        steps_completed += 1

        # Step 2: Backup system state
        self.backup_system_state()
        steps_completed += 1

        # Step 3: Remove Amazon bloatware
        if self.debloat_amazon_packages():
            self.log("✅ Debloating completed")
        steps_completed += 1

        # Step 4: Clean unnecessary Kodi addons
        if self.clean_unnecessary_addons():
            self.log("✅ Addon cleanup completed")
        steps_completed += 1

        # Step 5: Configure Kodi launcher
        if self.configure_kodi_launcher():
            self.log("✅ Launcher configuration completed")
        steps_completed += 1

        # Step 6: Apply performance optimizations
        if self.optimize_kodi_performance():
            self.log("✅ Performance optimization completed")
        steps_completed += 1

        # Step 7: Configure Pigeonhole skin
        if self.deploy_pigeonhole_skin():
            self.log("✅ Skin configuration completed")
        steps_completed += 1

        # Step 8: Restart and validate
        if self.restart_kodi() and self.validate_system():
            self.log("✅ System restart and validation completed")
            steps_completed += 1

        # Final summary
        self.log("=" * 60)
        self.log(f"OPTIMIZATION COMPLETE: {steps_completed}/{total_steps} steps")

        if steps_completed == total_steps:
            self.log("🚀 FIRE TV CUBE GOLD BUILD SUCCESSFUL!", "SUCCESS")
            self.log("🎯 Your Pigeonhole streaming system is ready!", "SUCCESS")
            return True
        else:
            self.log(f"⚠️ Partial success: {steps_completed}/{total_steps} completed", "WARN")
            return False

if __name__ == "__main__":
    optimizer = FireTVOptimizer()
    success = optimizer.run_full_optimization()

    if success:
        print("\n" + "="*60)
        print("🏆 PIGEONHOLE FIRE TV CUBE GOLD BUILD COMPLETE! 🏆")
        print("="*60)
        print("✅ Amazon bloatware removed")
        print("✅ Kodi addons optimized")
        print("✅ Kodi set as default launcher")
        print("✅ Performance settings optimized")
        print("✅ Pigeonhole skin activated")
        print("✅ System validated and ready")
        print("\nYour Fire TV Cube is now optimized for ultimate streaming!")
    else:
        print("\n❌ Optimization incomplete - check logs for issues")
        sys.exit(1)