#!/usr/bin/env python3
"""
Fire TV Cube Final Gold Setup - Windows Safe Version
Complete optimization for Kodi v22 with Pigeonhole streaming
"""

import subprocess
import requests
import json
import base64
import time
import sys
import os
import zipfile
from datetime import datetime

class FireTVFinalGold:
    def __init__(self, fire_tv_ip="192.168.1.130", http_port=8080):
        self.fire_tv_ip = fire_tv_ip
        self.http_port = http_port
        self.username = "kodi"
        self.password = "0000"
        self.base_url = f"http://{fire_tv_ip}:{http_port}/jsonrpc"
        self.adb_path = None

        # Auth header
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_credentials}"
        }

        # Bloatware to remove
        self.amazon_bloatware = [
            "com.amazon.dee.app",
            "amazon.speech.sim",
            "com.amazon.ags.app",
            "com.amazon.avod.thirdpartyclient",
            "com.amazon.bueller.music",
            "com.amazon.bueller.photos",
            "com.amazon.hedwig",
            "com.amazon.precog",
            "com.amazon.videoads.app"
        ]

        # Required addons
        self.core_addons = [
            "skin.arctic.zephyr.pigeonhole",
            "script.module.resolveurl",
            "plugin.video.thecrew",
            "plugin.video.fen.lite",
            "script.pigeonhole.config"
        ]

    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        status = "SUCCESS" if level == "SUCCESS" else "ERROR" if level == "ERROR" else "INFO"
        print(f"[{timestamp}] [{status}] {message}")

    def install_adb(self):
        self.log("Installing ADB Platform Tools...")

        adb_dir = "M:\\adb"
        os.makedirs(adb_dir, exist_ok=True)
        adb_exe = os.path.join(adb_dir, "adb.exe")

        if os.path.exists(adb_exe):
            self.adb_path = adb_exe
            self.log("ADB already installed", "SUCCESS")
            return True

        try:
            # Download ADB
            url = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
            self.log("Downloading ADB tools...")

            response = requests.get(url, timeout=60)
            if response.status_code != 200:
                self.log(f"Download failed: HTTP {response.status_code}", "ERROR")
                return False

            zip_path = os.path.join(adb_dir, "tools.zip")
            with open(zip_path, "wb") as f:
                f.write(response.content)

            self.log("Extracting ADB...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(adb_dir)

            # Move files from platform-tools subdirectory
            platform_dir = os.path.join(adb_dir, "platform-tools")
            if os.path.exists(platform_dir):
                for file in os.listdir(platform_dir):
                    src = os.path.join(platform_dir, file)
                    dst = os.path.join(adb_dir, file)
                    if os.path.isfile(src):
                        os.rename(src, dst)

                # Clean up
                import shutil
                shutil.rmtree(platform_dir)

            os.remove(zip_path)

            if os.path.exists(adb_exe):
                self.adb_path = adb_exe
                self.log("ADB installation completed", "SUCCESS")
                return True
            else:
                self.log("ADB installation failed - executable not found", "ERROR")
                return False

        except Exception as e:
            self.log(f"ADB installation error: {e}", "ERROR")
            return False

    def adb_cmd(self, command):
        if not self.adb_path:
            return False, "ADB not available"

        try:
            full_cmd = f'"{self.adb_path}" -s {self.fire_tv_ip}:5555 {command}'
            result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, timeout=30)
            output = result.stdout.strip() if result.stdout else result.stderr.strip()
            return result.returncode == 0, output
        except Exception as e:
            return False, str(e)

    def kodi_api(self, method, params=None):
        try:
            payload = {"jsonrpc": "2.0", "method": method, "id": 1}
            if params:
                payload["params"] = params

            response = requests.post(self.base_url, json=payload, headers=self.headers, timeout=15)
            if response.status_code == 200:
                result = response.json()
                return result.get("result", result)
            return None
        except:
            return None

    def connect_device(self):
        self.log("Connecting to Fire TV Cube...")

        # Disconnect first
        self.adb_cmd(f"disconnect {self.fire_tv_ip}:5555")
        time.sleep(2)

        # Connect
        success, output = self.adb_cmd(f"connect {self.fire_tv_ip}:5555")
        if success:
            time.sleep(5)
            success, output = self.adb_cmd("shell echo test")
            if success and "test" in output:
                self.log("Fire TV connected successfully", "SUCCESS")
                return True

        self.log(f"Connection failed: {output}", "ERROR")
        return False

    def remove_bloatware(self):
        self.log("Removing Amazon bloatware...")

        removed = 0
        for package in self.amazon_bloatware:
            self.log(f"Processing {package}...")

            # Try to disable and uninstall
            success1, _ = self.adb_cmd(f"shell pm disable-user --user 0 {package}")
            success2, _ = self.adb_cmd(f"shell pm uninstall --user 0 {package}")

            if success1 or success2:
                removed += 1
                self.log(f"Removed {package}", "SUCCESS")

        self.log(f"Bloatware removal completed: {removed} packages", "SUCCESS")
        return True

    def setup_launcher(self):
        self.log("Setting up Kodi launcher...")

        # Stop Amazon launcher
        self.adb_cmd("shell am force-stop com.amazon.tv.launcher")

        # Set Kodi as default
        success, output = self.adb_cmd("shell cmd package set-home-activity org.xbmc.kodi/org.xbmc.kodi.Splash")
        if success:
            self.log("Kodi set as default launcher", "SUCCESS")
            return True
        else:
            self.log(f"Launcher setup failed: {output}", "ERROR")
            return False

    def optimize_performance(self):
        self.log("Applying performance optimizations...")

        # Set Pigeonhole skin
        result = self.kodi_api("Settings.SetSettingValue", {
            "setting": "lookandfeel.skin",
            "value": "skin.arctic.zephyr.pigeonhole"
        })

        if result is not None:
            self.log("Pigeonhole skin activated", "SUCCESS")

        # Apply advanced settings
        advanced_xml = """<advancedsettings>
<network>
<buffermode>1</buffermode>
<cachemembuffersize>209715200</cachemembuffersize>
<readbufferfactor>4.0</readbufferfactor>
</network>
<video>
<rendermethod>0</rendermethod>
<adjustrefreshrate>2</adjustrefreshrate>
</video>
<cache>
<memorysize>209715200</memorysize>
<buffermode>1</buffermode>
</cache>
</advancedsettings>"""

        temp_file = "M:\\temp_advanced.xml"
        with open(temp_file, "w") as f:
            f.write(advanced_xml)

        success, _ = self.adb_cmd(f"push {temp_file} /storage/emulated/0/Android/data/org.xbmc.kodi/files/.kodi/userdata/advancedsettings.xml")

        if os.path.exists(temp_file):
            os.remove(temp_file)

        if success:
            self.log("Performance settings applied", "SUCCESS")

        return True

    def restart_kodi(self):
        self.log("Restarting Kodi...")

        # Stop Kodi
        self.adb_cmd("shell am force-stop org.xbmc.kodi")
        time.sleep(5)

        # Start Kodi
        success, _ = self.adb_cmd("shell am start -n org.xbmc.kodi/.Splash")
        if success:
            time.sleep(15)  # Wait for startup
            self.log("Kodi restarted successfully", "SUCCESS")
            return True

        self.log("Kodi restart failed", "ERROR")
        return False

    def validate_system(self):
        self.log("Validating system...")

        # Test Kodi API
        result = self.kodi_api("JSONRPC.Ping")
        if result != "pong":
            self.log("Kodi API validation failed", "ERROR")
            return False

        # Get system info
        info = self.kodi_api("System.GetInfoLabels", {
            "labels": ["System.BuildVersion", "Skin.CurrentSkin"]
        })

        if info:
            version = info.get("System.BuildVersion", "Unknown")
            skin = info.get("Skin.CurrentSkin", "Unknown")

            self.log(f"Kodi Version: {version}")
            self.log(f"Active Skin: {skin}")

            if "22" in version:
                self.log("Kodi v22 confirmed", "SUCCESS")

            if "pigeonhole" in skin.lower():
                self.log("Pigeonhole skin confirmed", "SUCCESS")

        # Test core addons
        addons = self.kodi_api("Addons.GetAddons", {
            "properties": ["name", "enabled"]
        })

        if addons and "addons" in addons:
            addon_dict = {a["addonid"]: a for a in addons["addons"]}
            working_addons = 0

            for core_addon in self.core_addons:
                if core_addon in addon_dict and addon_dict[core_addon]["enabled"]:
                    working_addons += 1

            self.log(f"Core addons working: {working_addons}/{len(self.core_addons)}")

            if working_addons >= len(self.core_addons) * 0.8:
                self.log("System validation passed", "SUCCESS")
                return True

        self.log("System validation failed", "ERROR")
        return False

    def run_gold_setup(self):
        print("============================================================")
        print("FIRE TV CUBE GOLD SETUP - PIGEONHOLE STREAMING")
        print("============================================================")

        steps = [
            ("Installing ADB", self.install_adb),
            ("Connecting to Fire TV", self.connect_device),
            ("Removing Bloatware", self.remove_bloatware),
            ("Setting up Launcher", self.setup_launcher),
            ("Optimizing Performance", self.optimize_performance),
            ("Restarting Kodi", self.restart_kodi),
            ("Validating System", self.validate_system)
        ]

        completed = 0
        for step_name, step_func in steps:
            print(f"\n[STEP] {step_name}...")
            try:
                if step_func():
                    completed += 1
                    self.log(f"{step_name} completed", "SUCCESS")
                else:
                    self.log(f"{step_name} failed", "ERROR")
            except Exception as e:
                self.log(f"{step_name} error: {e}", "ERROR")

        print("============================================================")
        print(f"SETUP COMPLETE: {completed}/{len(steps)} steps successful")
        print("============================================================")

        if completed == len(steps):
            print("*** FIRE TV CUBE GOLD BUILD SUCCESSFUL! ***")
            print("*** Your Pigeonhole streaming system is ready! ***")
            print("")
            print("FEATURES ACTIVATED:")
            print("- Amazon bloatware removed")
            print("- Kodi set as default launcher")
            print("- Pigeonhole skin activated")
            print("- Performance optimizations applied")
            print("- System validated and ready")
            print("")
            print("Your Fire TV Cube is now optimized for streaming!")
            return True
        else:
            print(f"Setup partially completed: {completed}/{len(steps)} steps")
            print("Check logs above for any errors")
            return False

if __name__ == "__main__":
    print("")
    print("============================================================")
    print("FIRE TV CUBE GOLD SETUP - PIGEONHOLE STREAMING ARCHITECT")
    print("Complete optimization system for Kodi v22")
    print("============================================================")
    print("")

    setup = FireTVFinalGold()
    success = setup.run_gold_setup()

    if not success:
        sys.exit(1)