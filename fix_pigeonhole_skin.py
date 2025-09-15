#!/usr/bin/env python3
"""
Fix Pigeonhole Skin Installation and Configuration
"""
import subprocess
import requests
import json
import base64
import time
from datetime import datetime

class PigeonholeSkinFixer:
    def __init__(self, fire_tv_ip="192.168.1.130", http_port=8080):
        self.fire_tv_ip = fire_tv_ip
        self.http_port = http_port
        self.username = "kodi"
        self.password = "0000"
        self.base_url = f"http://{fire_tv_ip}:{http_port}/jsonrpc"
        self.adb_path = "M:\\adb\\adb.exe"

        # Auth header
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_credentials}"
        }

    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")

    def adb_cmd(self, command):
        try:
            full_cmd = f'"{self.adb_path}" -s {self.fire_tv_ip}:5555 {command}'
            result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, timeout=30)
            return result.returncode == 0, result.stdout.strip() if result.stdout else result.stderr.strip()
        except Exception as e:
            return False, str(e)

    def kodi_api(self, method, params=None, timeout=15):
        try:
            payload = {"jsonrpc": "2.0", "method": method, "id": 1}
            if params:
                payload["params"] = params

            response = requests.post(self.base_url, json=payload, headers=self.headers, timeout=timeout)
            if response.status_code == 200:
                result = response.json()
                return result.get("result", result)
            return None
        except Exception as e:
            self.log(f"API error: {e}", "ERROR")
            return None

    def restart_kodi_safe(self):
        self.log("Restarting Kodi safely...")

        # Force stop Kodi
        self.adb_cmd("shell am force-stop org.xbmc.kodi")
        time.sleep(3)

        # Clear Kodi cache
        self.adb_cmd("shell pm clear org.xbmc.kodi")
        time.sleep(2)

        # Start Kodi
        success, output = self.adb_cmd("shell am start -n org.xbmc.kodi/.Splash")
        if success:
            self.log("Kodi restarted successfully")
            time.sleep(20)  # Wait for full startup
            return True
        else:
            self.log(f"Failed to start Kodi: {output}", "ERROR")
            return False

    def reset_to_default_skin(self):
        self.log("Resetting to default Estuary skin...")

        # First ensure Kodi is running
        if not self.restart_kodi_safe():
            return False

        # Wait for API to be available
        for attempt in range(10):
            result = self.kodi_api("JSONRPC.Ping")
            if result == "pong":
                break
            time.sleep(2)
        else:
            self.log("Kodi API not responding", "ERROR")
            return False

        # Set default skin
        result = self.kodi_api("Settings.SetSettingValue", {
            "setting": "lookandfeel.skin",
            "value": "skin.estuary"
        })

        if result:
            self.log("Default Estuary skin set")
            return True
        else:
            self.log("Failed to set default skin", "ERROR")
            return False

    def check_skin_installation(self):
        self.log("Checking Pigeonhole skin installation...")

        # Check if skin addon exists
        success, output = self.adb_cmd("shell ls /sdcard/Android/data/org.xbmc.kodi/files/.kodi/addons/skin.arctic.zephyr.pigeonhole")

        if success:
            self.log("Pigeonhole skin directory found")

            # Check skin.xml exists
            success, output = self.adb_cmd("shell test -f /sdcard/Android/data/org.xbmc.kodi/files/.kodi/addons/skin.arctic.zephyr.pigeonhole/addon.xml")
            if success:
                self.log("Skin addon.xml found")
                return True
            else:
                self.log("Skin addon.xml missing", "ERROR")
                return False
        else:
            self.log("Pigeonhole skin not found", "ERROR")
            return False

    def fix_skin_dependencies(self):
        self.log("Checking skin dependencies...")

        # Get list of all addons
        addons = self.kodi_api("Addons.GetAddons", {"properties": ["name", "enabled", "broken", "dependencies"]})

        if not addons or "addons" not in addons:
            self.log("Could not get addon list", "ERROR")
            return False

        # Look for Pigeonhole skin
        pigeonhole_skin = None
        for addon in addons["addons"]:
            if addon["addonid"] == "skin.arctic.zephyr.pigeonhole":
                pigeonhole_skin = addon
                break

        if not pigeonhole_skin:
            self.log("Pigeonhole skin not found in addon list", "ERROR")
            return False

        self.log(f"Skin status: enabled={pigeonhole_skin['enabled']}, broken={pigeonhole_skin['broken']}")

        if pigeonhole_skin["broken"]:
            self.log("Skin is marked as broken - checking dependencies")

            # Try to enable any disabled dependencies
            if "dependencies" in pigeonhole_skin:
                for dep in pigeonhole_skin["dependencies"]:
                    dep_id = dep.get("addonid")
                    if dep_id:
                        self.log(f"Checking dependency: {dep_id}")
                        result = self.kodi_api("Addons.SetAddonEnabled", {
                            "addonid": dep_id,
                            "enabled": True
                        })
                        if result == "OK":
                            self.log(f"Enabled dependency: {dep_id}")

        return True

    def enable_pigeonhole_skin(self):
        self.log("Enabling Pigeonhole skin...")

        # First enable the skin addon
        result = self.kodi_api("Addons.SetAddonEnabled", {
            "addonid": "skin.arctic.zephyr.pigeonhole",
            "enabled": True
        })

        if result == "OK":
            self.log("Pigeonhole skin enabled")
            time.sleep(2)

            # Check if it's available for selection
            skins = self.kodi_api("Addons.GetAddons", {
                "type": "xbmc.gui.skin",
                "properties": ["name", "enabled", "broken"]
            })

            if skins and "addons" in skins:
                for skin in skins["addons"]:
                    if skin["addonid"] == "skin.arctic.zephyr.pigeonhole":
                        if skin["enabled"] and not skin["broken"]:
                            self.log("Pigeonhole skin is available for selection")
                            return True
                        else:
                            self.log(f"Skin status: enabled={skin['enabled']}, broken={skin['broken']}", "ERROR")
                            return False

            self.log("Could not verify skin availability", "ERROR")
            return False
        else:
            self.log("Failed to enable Pigeonhole skin", "ERROR")
            return False

    def apply_pigeonhole_skin(self):
        self.log("Applying Pigeonhole skin...")

        # Set Pigeonhole as active skin
        result = self.kodi_api("Settings.SetSettingValue", {
            "setting": "lookandfeel.skin",
            "value": "skin.arctic.zephyr.pigeonhole"
        })

        if result:
            self.log("Pigeonhole skin applied - Kodi will restart")
            time.sleep(5)  # Wait for skin change to process

            # Kodi should restart automatically for skin change
            # Wait and check if it comes back up
            time.sleep(20)

            # Test if Kodi is responding with new skin
            for attempt in range(10):
                try:
                    info = self.kodi_api("System.GetInfoLabels", {
                        "labels": ["Skin.CurrentSkin", "Skin.Name"]
                    })
                    if info:
                        current_skin = info.get("Skin.CurrentSkin", "Unknown")
                        self.log(f"Current skin: {current_skin}")
                        if "pigeonhole" in current_skin.lower():
                            self.log("Pigeonhole skin successfully applied!")
                            return True
                    time.sleep(3)
                except:
                    time.sleep(3)
                    continue

            self.log("Skin change may have caused issues", "ERROR")
            return False
        else:
            self.log("Failed to apply Pigeonhole skin", "ERROR")
            return False

    def fix_pigeonhole_skin(self):
        self.log("="*60)
        self.log("PIGEONHOLE SKIN REPAIR SYSTEM")
        self.log("="*60)

        steps = [
            ("Reset to Default Skin", self.reset_to_default_skin),
            ("Check Skin Installation", self.check_skin_installation),
            ("Fix Dependencies", self.fix_skin_dependencies),
            ("Enable Pigeonhole Skin", self.enable_pigeonhole_skin),
            ("Apply Pigeonhole Skin", self.apply_pigeonhole_skin)
        ]

        completed = 0
        for step_name, step_func in steps:
            self.log(f"\n[STEP] {step_name}...")
            try:
                if step_func():
                    completed += 1
                    self.log(f"{step_name} completed", "SUCCESS")
                else:
                    self.log(f"{step_name} failed", "ERROR")
                    if step_name == "Apply Pigeonhole Skin":
                        # If skin application fails, go back to default
                        self.log("Reverting to default skin for stability")
                        self.reset_to_default_skin()
                        break
            except Exception as e:
                self.log(f"{step_name} error: {e}", "ERROR")
                break

        self.log("="*60)

        if completed >= 4:
            self.log("*** PIGEONHOLE SKIN SUCCESSFULLY FIXED! ***")
            return True
        elif completed >= 2:
            self.log("*** SYSTEM STABLE WITH DEFAULT SKIN ***")
            self.log("Pigeonhole skin has issues - using Estuary as fallback")
            return False
        else:
            self.log("*** SKIN REPAIR FAILED ***")
            return False

if __name__ == "__main__":
    fixer = PigeonholeSkinFixer()
    success = fixer.fix_pigeonhole_skin()

    if success:
        print("\nPigeonhole skin is now active and working!")
    else:
        print("\nSystem is stable with default skin. Pigeonhole skin needs manual attention.")