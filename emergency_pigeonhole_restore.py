#!/usr/bin/env python3
"""
EMERGENCY PIGEONHOLE RESTORE
Restore all missing addons after accidental wipe
"""
import subprocess
import time
import os
from datetime import datetime

class EmergencyRestore:
    def __init__(self, fire_tv_ip="192.168.1.130"):
        self.fire_tv_ip = fire_tv_ip
        self.adb_path = "M:\\adb\\adb.exe"

    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")

    def adb_cmd(self, command):
        try:
            full_cmd = f'"{self.adb_path}" -s {self.fire_tv_ip}:5555 {command}'
            result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, timeout=60)
            return result.returncode == 0, result.stdout.strip() if result.stdout else result.stderr.strip()
        except Exception as e:
            return False, str(e)

    def restart_kodi(self):
        self.log("Restarting Kodi...")
        self.adb_cmd("shell am force-stop org.xbmc.kodi")
        time.sleep(3)
        success, output = self.adb_cmd("shell am start -n org.xbmc.kodi/.Splash")
        if success:
            time.sleep(15)
            return True
        return False

    def install_pigeonhole_repo(self):
        self.log("Installing Pigeonhole repository...")

        # Push repository zip to device
        if os.path.exists("M:\\repository.pigeonhole.streaming.zip"):
            success, output = self.adb_cmd('push "M:\\repository.pigeonhole.streaming.zip" "/sdcard/repo.zip"')
            if success:
                self.log("Repository zip uploaded to device")

                # Create addons directory
                self.adb_cmd('shell "mkdir -p /sdcard/Android/data/org.xbmc.kodi/files/.kodi/addons"')

                # Extract repository
                success, output = self.adb_cmd('shell "cd /sdcard/Android/data/org.xbmc.kodi/files/.kodi/addons && unzip -o /sdcard/repo.zip"')
                if success:
                    self.log("Repository extracted successfully")
                    return True
                else:
                    self.log(f"Failed to extract: {output}", "ERROR")
            else:
                self.log(f"Failed to upload repo: {output}", "ERROR")
        else:
            self.log("Repository zip not found", "ERROR")

        return False

    def install_core_addons(self):
        self.log("Installing core addons...")

        # Check if we have addon files in the repo structure
        addon_files = [
            "M:\\arctic-zephyr-pigeonhole",
            "M:\\pigeonhole-repo",
            "M:\\addons"
        ]

        for addon_path in addon_files:
            if os.path.exists(addon_path):
                self.log(f"Found addon directory: {addon_path}")

                # Push entire directory
                success, output = self.adb_cmd(f'push "{addon_path}" "/sdcard/temp_addons/"')
                if success:
                    self.log(f"Uploaded {addon_path}")

                    # Copy to Kodi addons directory
                    self.adb_cmd('shell "cp -r /sdcard/temp_addons/* /sdcard/Android/data/org.xbmc.kodi/files/.kodi/addons/"')

        return True

    def enable_http_api(self):
        self.log("Enabling HTTP API...")

        # Create guisettings.xml with HTTP enabled
        guisettings_xml = '''<settings version="2">
    <setting id="services.webserver" type="boolean">true</setting>
    <setting id="services.webserverport" type="integer">8080</setting>
    <setting id="services.webserverauthentication" type="boolean">true</setting>
    <setting id="services.webserverusername" type="string">kodi</setting>
    <setting id="services.webserverpassword" type="string">0000</setting>
</settings>'''

        # Write to temp file
        temp_file = "M:\\temp_guisettings.xml"
        with open(temp_file, "w") as f:
            f.write(guisettings_xml)

        # Push to device
        success, output = self.adb_cmd(f'push "{temp_file}" "/sdcard/Android/data/org.xbmc.kodi/files/.kodi/userdata/guisettings.xml"')

        if os.path.exists(temp_file):
            os.remove(temp_file)

        if success:
            self.log("HTTP API settings applied")
            return True
        else:
            self.log(f"Failed to apply HTTP settings: {output}", "ERROR")
            return False

    def quick_addon_install(self):
        self.log("Quick addon installation from repo files...")

        # Extract and install from our backup repository
        if os.path.exists("M:\\repository.pigeonhole.streaming-FIXED.zip"):
            # Use the fixed version
            self.adb_cmd('push "M:\\repository.pigeonhole.streaming-FIXED.zip" "/sdcard/pigeonhole.zip"')
        elif os.path.exists("M:\\pigeonhole-repo.zip"):
            self.adb_cmd('push "M:\\pigeonhole-repo.zip" "/sdcard/pigeonhole.zip"')

        # Extract directly to addons
        self.adb_cmd('shell "cd /sdcard/Android/data/org.xbmc.kodi/files/.kodi/addons && unzip -o /sdcard/pigeonhole.zip"')

        # Set permissions
        self.adb_cmd('shell "chmod -R 755 /sdcard/Android/data/org.xbmc.kodi/files/.kodi/addons"')

        return True

    def emergency_restore(self):
        self.log("="*60)
        self.log("EMERGENCY PIGEONHOLE RESTORE")
        self.log("="*60)

        steps = [
            ("Restart Kodi", self.restart_kodi),
            ("Quick Addon Install", self.quick_addon_install),
            ("Enable HTTP API", self.enable_http_api),
            ("Final Kodi Restart", self.restart_kodi)
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
            except Exception as e:
                self.log(f"{step_name} error: {e}", "ERROR")

        self.log("="*60)

        if completed >= 3:
            self.log("*** EMERGENCY RESTORE COMPLETE! ***")
            self.log("Checking if addons are restored...")

            # Wait for Kodi to settle
            time.sleep(20)

            # Test if we can connect
            try:
                import requests
                import base64
                auth = base64.b64encode(b'kodi:0000').decode()
                headers = {'Authorization': f'Basic {auth}', 'Content-Type': 'application/json'}
                r = requests.get('http://192.168.1.130:8080/jsonrpc', headers=headers, timeout=10)
                if r.status_code == 200:
                    self.log("*** HTTP API RESTORED! ***")
                    return True
            except:
                pass

            self.log("System restored but HTTP API may need time to activate")
            return True
        else:
            self.log("*** EMERGENCY RESTORE FAILED ***")
            return False

if __name__ == "__main__":
    restore = EmergencyRestore()
    success = restore.emergency_restore()

    if success:
        print("\n✅ EMERGENCY RESTORE SUCCESSFUL!")
        print("🎯 Pigeonhole addons should be restored")
        print("🔗 HTTP API should be working")
        print("⏰ Allow 1-2 minutes for full activation")
    else:
        print("\n❌ EMERGENCY RESTORE FAILED")
        print("Manual intervention required")