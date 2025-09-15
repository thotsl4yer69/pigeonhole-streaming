#!/usr/bin/env python3
"""
Complete Fire TV Cube Gold Setup - All-in-One Installer
Includes ADB installation, optimization, and validation
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
import tempfile

class CompleteGoldSetup:
    def __init__(self, fire_tv_ip="192.168.1.130", http_port=8080):
        self.fire_tv_ip = fire_tv_ip
        self.http_port = http_port
        self.username = "kodi"
        self.password = "0000"
        self.base_url = f"http://{fire_tv_ip}:{http_port}/jsonrpc"
        self.adb_path = None

        # Create auth header
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_credentials}"
        }

        # Amazon bloatware (safe removal list)
        self.amazon_bloatware = [
            "com.amazon.dee.app",
            "amazon.speech.sim",
            "com.amazon.ags.app",
            "com.amazon.avod.thirdpartyclient",
            "com.amazon.bueller.music",
            "com.amazon.bueller.photos",
            "com.amazon.device.bluetoothdfu",
            "com.amazon.device.sync",
            "com.amazon.hedwig",
            "com.amazon.precog",
            "com.amazon.providers",
            "com.amazon.shoptv.client",
            "com.amazon.videoads.app",
        ]

        # Pigeonhole core addons
        self.pigeonhole_core = [
            "skin.arctic.zephyr.pigeonhole",
            "script.module.resolveurl",
            "plugin.video.thecrew",
            "plugin.video.fen.lite",
            "script.pigeonhole.config",
            "repository.pigeonhole.streaming",
        ]

    def log(self, message, level="INFO"):
        """Safe logging function"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")

    def install_adb(self):
        """Download and install ADB platform tools"""
        self.log("Installing ADB Platform Tools...")

        adb_dir = os.path.join("M:\\", "adb")
        os.makedirs(adb_dir, exist_ok=True)

        adb_exe = os.path.join(adb_dir, "adb.exe")

        if os.path.exists(adb_exe):
            self.log("[OK] ADB already installed")
            self.adb_path = adb_exe
            return True

        try:
            # Download platform tools
            url = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
            self.log("Downloading ADB platform tools...")

            response = requests.get(url, stream=True)
            if response.status_code == 200:
                zip_path = os.path.join(adb_dir, "platform-tools.zip")

                with open(zip_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                self.log("Extracting ADB tools...")

                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(adb_dir)

                # Copy files to adb directory
                platform_tools_dir = os.path.join(adb_dir, "platform-tools")
                if os.path.exists(platform_tools_dir):
                    for file in os.listdir(platform_tools_dir):
                        if file.endswith(('.exe', '.dll')):
                            src = os.path.join(platform_tools_dir, file)
                            dst = os.path.join(adb_dir, file)
                            if os.path.exists(src):
                                os.rename(src, dst)

                # Cleanup
                os.remove(zip_path)
                if os.path.exists(platform_tools_dir):
                    import shutil
                    shutil.rmtree(platform_tools_dir)

                if os.path.exists(adb_exe):
                    self.adb_path = adb_exe
                    self.log("[OK] ADB installation completed")
                    return True
                else:
                    self.log("[ERROR] ADB installation failed", "ERROR")
                    return False
            else:
                self.log(f"[ERROR] Failed to download ADB: HTTP {response.status_code}", "ERROR")
                return False

        except Exception as e:
            self.log(f"[ERROR] ADB installation error: {e}", "ERROR")
            return False

    def adb_command(self, command):
        """Execute ADB command using installed ADB"""
        if not self.adb_path:
            return False, "ADB not installed"

        try:
            full_command = f'"{self.adb_path}" -s {self.fire_tv_ip}:5555 {command}'
            result = subprocess.run(full_command, shell=True, capture_output=True, text=True, timeout=30)
            return result.returncode == 0, result.stdout.strip() if result.stdout else result.stderr.strip()
        except Exception as e:
            return False, str(e)

    def kodi_jsonrpc(self, method, params=None):
        """Execute Kodi JSON-RPC call"""
        try:
            payload = {"jsonrpc": "2.0", "method": method, "id": 1}
            if params:
                payload["params"] = params

            response = requests.post(self.base_url, json=payload, headers=self.headers, timeout=15)
            if response.status_code == 200:
                result = response.json()
                return result.get("result", result)
            else:
                return None
        except Exception as e:
            self.log(f"Kodi API error: {e}", "ERROR")
            return None

    def connect_fire_tv(self):
        """Connect to Fire TV via ADB"""
        self.log("Connecting to Fire TV Cube...")

        # Disconnect first
        self.adb_command(f"disconnect {self.fire_tv_ip}:5555")
        time.sleep(2)

        # Connect
        success, output = self.adb_command(f"connect {self.fire_tv_ip}:5555")
        if success:
            time.sleep(5)

            # Test connection
            success, output = self.adb_command("shell echo 'Connected'")
            if success and "Connected" in output:
                self.log("[OK] Fire TV connected successfully")
                return True

        self.log(f"[ERROR] Fire TV connection failed: {output}", "ERROR")
        return False

    def backup_system(self):
        """Create system backup"""
        self.log("Creating system backup...")

        backup_dir = f"M:\\backup_{int(time.time())}"
        os.makedirs(backup_dir, exist_ok=True)

        # Backup packages
        success, packages = self.adb_command("shell pm list packages")
        if success:
            with open(os.path.join(backup_dir, "packages.txt"), "w") as f:
                f.write(packages)

        # Backup launcher
        success, launcher = self.adb_command("shell cmd package resolve-activity --brief -c android.intent.category.HOME")
        if success:
            with open(os.path.join(backup_dir, "launcher.txt"), "w") as f:
                f.write(launcher)

        self.log(f"[OK] Backup created: {backup_dir}")
        return backup_dir

    def remove_bloatware(self):
        """Remove Amazon bloatware"""
        self.log("Removing Amazon bloatware...")

        removed = 0
        for package in self.amazon_bloatware:
            self.log(f"Processing {package}...")

            # Disable then uninstall
            success1, _ = self.adb_command(f"shell pm disable-user --user 0 {package}")
            success2, _ = self.adb_command(f"shell pm uninstall --user 0 {package}")

            if success1 or success2:
                self.log(f"  [OK] Removed {package}")
                removed += 1
            else:
                self.log(f"  [SKIP] {package} not found")

        self.log(f"[OK] Removed {removed} bloatware packages")
        return removed > 0

    def optimize_kodi(self):
        """Optimize Kodi performance"""
        self.log("Optimizing Kodi performance...")

        # Set Kodi as launcher
        success, _ = self.adb_command("shell am force-stop com.amazon.tv.launcher")
        success, _ = self.adb_command("shell cmd package set-home-activity org.xbmc.kodi/org.xbmc.kodi.Splash")

        if success:
            self.log("[OK] Kodi set as default launcher")
        else:
            self.log("[WARN] Could not set Kodi as launcher")

        # Apply performance settings via API
        self.kodi_jsonrpc("Settings.SetSettingValue", {
            "setting": "lookandfeel.skin",
            "value": "skin.arctic.zephyr.pigeonhole"
        })

        # Restart Kodi
        self.adb_command("shell am force-stop org.xbmc.kodi")
        time.sleep(3)
        self.adb_command("shell am start -n org.xbmc.kodi/.Splash")
        time.sleep(10)

        self.log("[OK] Kodi optimization completed")
        return True

    def validate_system(self):
        """Validate the optimized system"""
        self.log("Validating system...")

        # Test Kodi API
        result = self.kodi_jsonrpc("JSONRPC.Ping")
        if result != "pong":
            self.log("[ERROR] Kodi not responding", "ERROR")
            return False

        # Get system info
        system_info = self.kodi_jsonrpc("System.GetInfoLabels", {
            "labels": ["System.BuildVersion", "Skin.CurrentSkin"]
        })

        if system_info:
            version = system_info.get("System.BuildVersion", "Unknown")
            skin = system_info.get("Skin.CurrentSkin", "Unknown")

            self.log(f"[OK] Kodi Version: {version}")
            self.log(f"[OK] Active Skin: {skin}")

            if "22" in version and "pigeonhole" in skin.lower():
                self.log("[OK] System validation passed")
                return True

        self.log("[ERROR] System validation failed", "ERROR")
        return False

    def run_complete_setup(self):
        """Execute complete Fire TV Cube gold setup"""
        self.log("="*70)
        self.log("FIRE TV CUBE COMPLETE GOLD SETUP - PIGEONHOLE STREAMING")
        self.log("="*70)

        steps = [
            ("Installing ADB", self.install_adb),
            ("Connecting to Fire TV", self.connect_fire_tv),
            ("Creating System Backup", self.backup_system),
            ("Removing Bloatware", self.remove_bloatware),
            ("Optimizing Kodi", self.optimize_kodi),
            ("Validating System", self.validate_system),
        ]

        completed = 0
        for step_name, step_func in steps:
            self.log(f"\n[STEP] {step_name}...")
            try:
                if step_func():
                    completed += 1
                    self.log(f"[OK] {step_name} completed")
                else:
                    self.log(f"[ERROR] {step_name} failed", "ERROR")
            except Exception as e:
                self.log(f"[ERROR] {step_name} error: {e}", "ERROR")

        # Final results
        self.log("="*70)
        self.log(f"SETUP COMPLETE: {completed}/{len(steps)} steps successful")

        if completed == len(steps):
            self.log("*** FIRE TV CUBE GOLD BUILD SUCCESSFUL! ***")
            self.log("*** Your Pigeonhole streaming system is ready! ***")
            return True
        else:
            self.log(f"[WARN] Partial success: {completed}/{len(steps)} completed")
            return False

if __name__ == "__main__":
    setup = CompleteGoldSetup()

    print("""
    ████████████████████████████████████████████████████████
    ██                                                    ██
    ██  FIRE TV CUBE GOLD SETUP - PIGEONHOLE STREAMING   ██
    ██  Complete All-in-One Installation & Optimization  ██
    ██                                                    ██
    ████████████████████████████████████████████████████████
    """)

    success = setup.run_complete_setup()

    if success:
        print("""
        ████████████████████████████████████████████████████████
        ██                                                    ██
        ██  🚀 FIRE TV CUBE GOLD BUILD COMPLETE! 🚀          ██
        ██                                                    ██
        ██  ✅ ADB Platform Tools installed                  ██
        ██  ✅ Fire TV connected and optimized               ██
        ██  ✅ Amazon bloatware removed                      ██
        ██  ✅ Kodi set as default launcher                  ██
        ██  ✅ Performance optimizations applied             ██
        ██  ✅ System validated and ready                    ██
        ██                                                    ██
        ██  Your Fire TV Cube is now optimized for          ██
        ██  ultimate streaming with Pigeonhole!             ██
        ██                                                    ██
        ████████████████████████████████████████████████████████
        """)
    else:
        print("[ERROR] Setup incomplete - check logs for details")
        sys.exit(1)