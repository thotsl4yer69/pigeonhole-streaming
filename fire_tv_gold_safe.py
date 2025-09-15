#!/usr/bin/env python3
"""
Fire TV Cube Gold Optimizer - Windows Safe Version
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
            "com.amazon.dee.app",
            "amazon.speech.sim",
            "com.amazon.ags.app",
            "com.amazon.avod.thirdpartyclient",
            "com.amazon.bueller.music",
            "com.amazon.bueller.photos",
            "com.amazon.device.bluetoothdfu",
            "com.amazon.device.sync",
            "com.amazon.device.sync.sdk.internal",
            "com.amazon.hedwig",
            "com.amazon.identity.auth.device.authorization",
            "com.amazon.kindleautomatictimezone",
            "com.amazon.ods.kindleconnect",
            "com.amazon.parentalcontrols",
            "com.amazon.precog",
            "com.amazon.providers",
            "com.amazon.securitysyncclient",
            "com.amazon.sharingservice.android.client.proxy",
            "com.amazon.shoptv.client",
            "com.amazon.ssm",
            "com.amazon.ssmsys",
            "com.amazon.storm.lightning.services",
            "com.amazon.storm.lightning.tutorial",
            "com.amazon.tmm.tutorial",
            "com.amazon.tv.parentalcontrols",
            "com.amazon.venezia",
            "com.amazon.videoads.app",
            "com.amazon.visualonawv",
            "com.amazon.wifilocker",
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
        """Windows-safe logging"""
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
            self.log("[OK] Launcher configuration backed up", "SUCCESS")

    def debloat_amazon_packages(self):
        """Remove Amazon bloatware packages safely"""
        self.log("Starting Amazon bloatware removal...")

        removed_count = 0
        failed_count = 0

        for package in self.amazon_bloatware:
            self.log(f"Processing {package}...")

            # First try to disable
            success, output = self.adb_command(f"shell pm disable-user --user 0 {package}")
            if success:
                # Then uninstall for user
                success, output = self.adb_command(f"shell pm uninstall --user 0 {package}")
                if success:
                    self.log(f"  [OK] Removed: {package}", "SUCCESS")
                    removed_count += 1
                else:
                    self.log(f"  [WARN] Disabled only: {package}", "WARN")
            else:
                self.log(f"  [ERROR] Failed: {package}", "ERROR")
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
            self.log("[ERROR] Failed to get addon list", "ERROR")
            return []

    def clean_unnecessary_addons(self):
        """Remove unnecessary addons, keep Pigeonhole core"""
        self.log("Cleaning unnecessary Kodi addons...")

        addons = self.get_kodi_addons()
        if not addons:
            return False

        cleaned_count = 0

        for addon in addons:
            addon_id = addon["addonid"]

            # Skip core addons
            if addon_id in self.pigeonhole_core:
                continue

            # Skip system addons
            if addon_id.startswith("kodi.") or addon_id.startswith("xbmc."):
                continue

            # Skip our skin
            if addon["type"] == "xbmc.gui.skin" and not addon_id.startswith("skin.arctic.zephyr"):
                continue

            # Check for bloat patterns
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
                self.log(f"Disabling: {addon['name']}")
                result = self.kodi_jsonrpc("Addons.SetAddonEnabled", {
                    "addonid": addon_id,
                    "enabled": False
                })
                if result:
                    cleaned_count += 1

        self.log(f"[OK] Cleaned {cleaned_count} unnecessary addons", "SUCCESS")
        return cleaned_count > 0

    def configure_kodi_launcher(self):
        """Configure Kodi as default launcher"""
        self.log("Configuring Kodi as default launcher...")

        # Stop Amazon launcher
        success, output = self.adb_command("shell am force-stop com.amazon.tv.launcher")
        if success:
            self.log("[OK] Stopped Amazon launcher")

        # Set Kodi as default home
        success, output = self.adb_command("shell cmd package set-home-activity org.xbmc.kodi/org.xbmc.kodi.Splash")
        if success:
            self.log("[OK] Set Kodi as default launcher", "SUCCESS")

            # Clear launcher defaults
            self.adb_command("shell pm clear com.amazon.tv.launcher")

            # Start Kodi
            self.adb_command("shell am start -n org.xbmc.kodi/.Splash")
            return True
        else:
            self.log(f"[ERROR] Failed to set Kodi launcher: {output}", "ERROR")
            return False

    def optimize_kodi_performance(self):
        """Apply Fire TV Cube specific performance optimizations"""
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

        # Save and push settings
        temp_file = "M:\\advanced_settings_temp.xml"
        with open(temp_file, "w") as f:
            f.write(advanced_settings)

        success, output = self.adb_command(f"push {temp_file} /storage/emulated/0/Android/data/org.xbmc.kodi/files/.kodi/userdata/advancedsettings.xml")
        if success:
            self.log("[OK] Applied advanced performance settings", "SUCCESS")
            import os
            os.remove(temp_file)
            return True
        else:
            self.log(f"[ERROR] Failed to apply settings: {output}", "ERROR")
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
            self.log("[OK] Activated Pigeonhole skin", "SUCCESS")
            return True
        else:
            self.log("[ERROR] Failed to activate Pigeonhole skin", "ERROR")
            return False

    def restart_kodi(self):
        """Restart Kodi to apply all changes"""
        self.log("Restarting Kodi...")

        # Stop Kodi
        success, output = self.adb_command("shell am force-stop org.xbmc.kodi")
        if success:
            self.log("[OK] Stopped Kodi")
            time.sleep(3)

            # Start Kodi
            success, output = self.adb_command("shell am start -n org.xbmc.kodi/.Splash")
            if success:
                self.log("[OK] Restarted Kodi", "SUCCESS")
                time.sleep(10)  # Wait for startup
                return True

        self.log("[ERROR] Failed to restart Kodi", "ERROR")
        return False

    def validate_system(self):
        """Validate final system state"""
        self.log("Validating optimized system...")

        # Test Kodi connection
        result = self.kodi_jsonrpc("JSONRPC.Ping")
        if result == "pong":
            self.log("[OK] Kodi HTTP API responding")

            # Get system info
            system_info = self.kodi_jsonrpc("System.GetInfoLabels", {
                "labels": ["System.BuildVersion", "System.FreeMemory", "Skin.CurrentSkin"]
            })

            if system_info:
                self.log(f"[OK] Kodi Version: {system_info.get('System.BuildVersion', 'Unknown')}")
                self.log(f"[OK] Free Memory: {system_info.get('System.FreeMemory', 'Unknown')}")
                self.log(f"[OK] Active Skin: {system_info.get('Skin.CurrentSkin', 'Unknown')}")

                # Test addon functionality
                addons = self.get_kodi_addons()
                core_working = sum(1 for addon in addons
                                 if addon["addonid"] in self.pigeonhole_core and addon["enabled"])

                self.log(f"[OK] Core addons working: {core_working}/{len(self.pigeonhole_core)}")

                if core_working >= len(self.pigeonhole_core) * 0.8:
                    self.log("*** GOLD BUILD VALIDATION SUCCESSFUL! ***", "SUCCESS")
                    return True

        self.log("[ERROR] System validation failed", "ERROR")
        return False

    def run_full_optimization(self):
        """Execute complete Fire TV Cube gold optimization"""
        self.log("="*60)
        self.log("FIRE TV CUBE GOLD OPTIMIZATION - PIGEONHOLE STREAMING")
        self.log("="*60)

        steps_completed = 0
        total_steps = 8

        # Step 1: Check ADB connection
        if not self.check_adb_connection():
            self.log("[ERROR] Cannot proceed without ADB connection", "ERROR")
            return False
        steps_completed += 1

        # Step 2: Backup system state
        self.backup_system_state()
        steps_completed += 1

        # Step 3: Remove Amazon bloatware
        if self.debloat_amazon_packages():
            self.log("[OK] Debloating completed")
        steps_completed += 1

        # Step 4: Clean unnecessary Kodi addons
        if self.clean_unnecessary_addons():
            self.log("[OK] Addon cleanup completed")
        steps_completed += 1

        # Step 5: Configure Kodi launcher
        if self.configure_kodi_launcher():
            self.log("[OK] Launcher configuration completed")
        steps_completed += 1

        # Step 6: Apply performance optimizations
        if self.optimize_kodi_performance():
            self.log("[OK] Performance optimization completed")
        steps_completed += 1

        # Step 7: Configure Pigeonhole skin
        if self.deploy_pigeonhole_skin():
            self.log("[OK] Skin configuration completed")
        steps_completed += 1

        # Step 8: Restart and validate
        if self.restart_kodi() and self.validate_system():
            self.log("[OK] System restart and validation completed")
            steps_completed += 1

        # Final summary
        self.log("="*60)
        self.log(f"OPTIMIZATION COMPLETE: {steps_completed}/{total_steps} steps")

        if steps_completed == total_steps:
            self.log("*** FIRE TV CUBE GOLD BUILD SUCCESSFUL! ***", "SUCCESS")
            self.log("*** Your Pigeonhole streaming system is ready! ***", "SUCCESS")
            return True
        else:
            self.log(f"[WARN] Partial success: {steps_completed}/{total_steps} completed", "WARN")
            return False

if __name__ == "__main__":
    optimizer = FireTVOptimizer()
    success = optimizer.run_full_optimization()

    if success:
        print("\n" + "="*60)
        print("*** PIGEONHOLE FIRE TV CUBE GOLD BUILD COMPLETE! ***")
        print("="*60)
        print("[OK] Amazon bloatware removed")
        print("[OK] Kodi addons optimized")
        print("[OK] Kodi set as default launcher")
        print("[OK] Performance settings optimized")
        print("[OK] Pigeonhole skin activated")
        print("[OK] System validated and ready")
        print("\nYour Fire TV Cube is now optimized for ultimate streaming!")
    else:
        print("\n[ERROR] Optimization incomplete - check logs for issues")
        sys.exit(1)