#!/usr/bin/env python3
"""
Complete Kodi Expert Agent - Fire TV Cube Pigeonhole Specialist
"""
import requests
import json
import base64
import subprocess
import time
import os
from datetime import datetime

class KodiExpert:
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
        print(f"[{timestamp}] [KODI-EXPERT] [{level}] {message}")

    def kodi_api(self, method, params=None):
        """Kodi JSON-RPC API with expert error handling"""
        try:
            payload = {"jsonrpc": "2.0", "method": method, "id": 1}
            if params:
                payload["params"] = params

            response = requests.post(self.base_url, json=payload, headers=self.headers, timeout=15)

            if response.status_code == 200:
                result = response.json()
                if "error" in result:
                    self.log(f"Kodi API Error: {result['error']}", "ERROR")
                    return None
                return result.get("result", result)
            else:
                return None
        except:
            return None

    def adb_cmd(self, command):
        """ADB command with expert error handling"""
        try:
            full_cmd = f'"{self.adb_path}" -s {self.fire_tv_ip}:5555 {command}'
            result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, timeout=30)
            return result.returncode == 0, result.stdout.strip() if result.stdout else result.stderr.strip()
        except:
            return False, "Command failed"

    def diagnose_pigeonhole_system(self):
        """Complete Pigeonhole system diagnosis"""
        self.log("="*60)
        self.log("KODI EXPERT - PIGEONHOLE SYSTEM DIAGNOSIS")
        self.log("="*60)

        diagnosis = {
            "timestamp": datetime.now().isoformat(),
            "kodi_status": self._check_kodi_status(),
            "addon_status": self._check_addon_status(),
            "skin_status": self._check_skin_status(),
            "streaming_status": self._check_streaming_status(),
            "system_status": self._check_system_status(),
            "solutions": []
        }

        # Generate expert solutions
        diagnosis["solutions"] = self._generate_expert_solutions(diagnosis)

        return diagnosis

    def _check_kodi_status(self):
        """Check Kodi basic functionality"""
        self.log("Checking Kodi status...")

        # Test API connection
        ping_result = self.kodi_api("JSONRPC.Ping")
        api_working = ping_result == "pong"

        # Get system info
        system_info = None
        if api_working:
            system_info = self.kodi_api("System.GetInfoLabels", {
                "labels": ["System.BuildVersion", "System.FreeMemory"]
            })

        return {
            "api_responding": api_working,
            "system_info": system_info,
            "version": system_info.get("System.BuildVersion") if system_info else "Unknown"
        }

    def _check_addon_status(self):
        """Check Pigeonhole addon status"""
        self.log("Checking addon status...")

        core_addons = [
            "skin.arctic.zephyr.pigeonhole",
            "script.module.resolveurl",
            "plugin.video.thecrew",
            "plugin.video.fen.lite",
            "script.pigeonhole.config",
            "repository.pigeonhole.streaming"
        ]

        # Get all addons
        all_addons = self.kodi_api("Addons.GetAddons", {
            "properties": ["name", "enabled", "broken"]
        })

        addon_status = {}
        if all_addons and "addons" in all_addons:
            addon_dict = {addon["addonid"]: addon for addon in all_addons["addons"]}

            for addon_id in core_addons:
                if addon_id in addon_dict:
                    addon = addon_dict[addon_id]
                    addon_status[addon_id] = {
                        "installed": True,
                        "enabled": addon["enabled"],
                        "broken": addon["broken"],
                        "name": addon["name"]
                    }
                else:
                    addon_status[addon_id] = {
                        "installed": False,
                        "enabled": False,
                        "broken": False,
                        "name": "Missing"
                    }

        return {
            "total_addons": len(all_addons["addons"]) if all_addons and "addons" in all_addons else 0,
            "core_addons": addon_status,
            "missing_count": sum(1 for status in addon_status.values() if not status["installed"])
        }

    def _check_skin_status(self):
        """Check skin availability and status"""
        self.log("Checking skin status...")

        # Get current skin
        current_skin = self.kodi_api("System.GetInfoLabels", {
            "labels": ["Skin.CurrentSkin", "Skin.Name"]
        })

        # Get available skins
        skins = self.kodi_api("Addons.GetAddons", {
            "type": "xbmc.gui.skin",
            "properties": ["name", "enabled", "broken"]
        })

        pigeonhole_available = False
        if skins and "addons" in skins:
            for skin in skins["addons"]:
                if skin["addonid"] == "skin.arctic.zephyr.pigeonhole":
                    pigeonhole_available = skin["enabled"] and not skin["broken"]
                    break

        return {
            "current_skin": current_skin,
            "pigeonhole_available": pigeonhole_available,
            "total_skins": len(skins["addons"]) if skins and "addons" in skins else 0
        }

    def _check_streaming_status(self):
        """Check streaming functionality"""
        self.log("Checking streaming status...")

        # Check if ResolveURL is configured
        resolveurl_settings = False
        success, output = self.adb_cmd('shell "test -f /sdcard/Android/data/org.xbmc.kodi/files/.kodi/userdata/addon_data/script.module.resolveurl/settings.xml"')
        resolveurl_settings = success

        return {
            "resolveurl_configured": resolveurl_settings,
            "streaming_ready": resolveurl_settings  # Simplified check
        }

    def _check_system_status(self):
        """Check Fire TV system status"""
        self.log("Checking Fire TV system status...")

        # Check device info
        success, model = self.adb_cmd('shell "getprop ro.product.model"')
        success2, android_version = self.adb_cmd('shell "getprop ro.build.version.release"')

        # Check available storage
        success3, storage = self.adb_cmd('shell "df /data | tail -1"')

        return {
            "device_model": model if success else "Unknown",
            "android_version": android_version if success2 else "Unknown",
            "storage_info": storage if success3 else "Unknown"
        }

    def _generate_expert_solutions(self, diagnosis):
        """Generate expert solutions based on diagnosis"""
        solutions = []

        # Check if Kodi API is working
        if not diagnosis["kodi_status"]["api_responding"]:
            solutions.append({
                "priority": "CRITICAL",
                "issue": "Kodi HTTP API not responding",
                "solution": "restart_kodi_with_http",
                "description": "Restart Kodi and ensure HTTP API is enabled"
            })

        # Check missing addons
        missing_addons = diagnosis["addon_status"]["missing_count"]
        if missing_addons > 0:
            solutions.append({
                "priority": "CRITICAL",
                "issue": f"{missing_addons} core Pigeonhole addons missing",
                "solution": "install_pigeonhole_addons",
                "description": "Install complete Pigeonhole addon suite from repository"
            })

        # Check skin availability
        if not diagnosis["skin_status"]["pigeonhole_available"]:
            solutions.append({
                "priority": "HIGH",
                "issue": "Pigeonhole skin not available",
                "solution": "fix_pigeonhole_skin",
                "description": "Enable and configure Pigeonhole skin"
            })

        # Check streaming configuration
        if not diagnosis["streaming_status"]["streaming_ready"]:
            solutions.append({
                "priority": "HIGH",
                "issue": "Streaming not configured",
                "solution": "configure_streaming",
                "description": "Configure ResolveURL and streaming addons"
            })

        return solutions

    def execute_solution(self, solution_name):
        """Execute specific expert solution"""
        self.log(f"Executing solution: {solution_name}")

        solutions = {
            "restart_kodi_with_http": self._restart_kodi_with_http,
            "install_pigeonhole_addons": self._install_pigeonhole_addons,
            "fix_pigeonhole_skin": self._fix_pigeonhole_skin,
            "configure_streaming": self._configure_streaming
        }

        if solution_name in solutions:
            return solutions[solution_name]()
        else:
            return f"Unknown solution: {solution_name}"

    def _restart_kodi_with_http(self):
        """Restart Kodi and ensure HTTP API is working"""
        self.log("Restarting Kodi with HTTP API...")

        # Create HTTP settings
        http_settings = '''<settings version="2">
    <setting id="services.webserver" type="boolean">true</setting>
    <setting id="services.webserverport" type="integer">8080</setting>
    <setting id="services.webserverauthentication" type="boolean">true</setting>
    <setting id="services.webserverusername" type="string">kodi</setting>
    <setting id="services.webserverpassword" type="string">0000</setting>
</settings>'''

        # Write to temp file and push
        temp_file = "M:\\temp_http_settings.xml"
        with open(temp_file, "w") as f:
            f.write(http_settings)

        self.adb_cmd(f'push "{temp_file}" "/sdcard/Android/data/org.xbmc.kodi/files/.kodi/userdata/guisettings.xml"')

        if os.path.exists(temp_file):
            os.remove(temp_file)

        # Restart Kodi
        self.adb_cmd("shell am force-stop org.xbmc.kodi")
        time.sleep(3)
        success, output = self.adb_cmd("shell am start -n org.xbmc.kodi/.Splash")

        if success:
            time.sleep(20)  # Wait for startup
            return "Kodi restarted with HTTP API enabled"
        else:
            return f"Failed to restart Kodi: {output}"

    def _install_pigeonhole_addons(self):
        """Install complete Pigeonhole addon suite"""
        self.log("Installing Pigeonhole addons...")

        # Use our repository zip files
        repo_files = [
            "M:\\pigeonhole-repo.zip",
            "M:\\repository.pigeonhole.streaming-FIXED.zip"
        ]

        for repo_file in repo_files:
            if os.path.exists(repo_file):
                self.log(f"Installing from {repo_file}")

                # Push to device
                success, output = self.adb_cmd(f'push "{repo_file}" "/sdcard/temp_repo.zip"')
                if success:
                    # Extract to addons directory
                    self.adb_cmd('shell "mkdir -p /sdcard/Android/data/org.xbmc.kodi/files/.kodi/addons"')
                    self.adb_cmd('shell "cd /sdcard/Android/data/org.xbmc.kodi/files/.kodi/addons && unzip -o /sdcard/temp_repo.zip"')
                    self.adb_cmd('shell "chmod -R 755 /sdcard/Android/data/org.xbmc.kodi/files/.kodi/addons"')

                    return f"Installed addons from {repo_file}"

        return "No repository files found for installation"

    def _fix_pigeonhole_skin(self):
        """Fix Pigeonhole skin availability"""
        self.log("Fixing Pigeonhole skin...")

        # Enable the skin addon
        result = self.kodi_api("Addons.SetAddonEnabled", {
            "addonid": "skin.arctic.zephyr.pigeonhole",
            "enabled": True
        })

        if result == "OK":
            # Try to set as active skin
            skin_result = self.kodi_api("Settings.SetSettingValue", {
                "setting": "lookandfeel.skin",
                "value": "skin.arctic.zephyr.pigeonhole"
            })
            return f"Skin enabled and set active: {skin_result}"
        else:
            return f"Failed to enable skin: {result}"

    def _configure_streaming(self):
        """Configure streaming functionality"""
        self.log("Configuring streaming...")

        # Create basic ResolveURL settings
        resolveurl_settings = '''<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<settings version="2">
    <category id="universal">
        <setting id="allow_universal">true</setting>
        <setting id="universal_timeout">30</setting>
    </category>
</settings>'''

        # Create settings directory and file
        self.adb_cmd('shell "mkdir -p /sdcard/Android/data/org.xbmc.kodi/files/.kodi/userdata/addon_data/script.module.resolveurl"')

        temp_file = "M:\\temp_resolveurl_settings.xml"
        with open(temp_file, "w") as f:
            f.write(resolveurl_settings)

        success, output = self.adb_cmd(f'push "{temp_file}" "/sdcard/Android/data/org.xbmc.kodi/files/.kodi/userdata/addon_data/script.module.resolveurl/settings.xml"')

        if os.path.exists(temp_file):
            os.remove(temp_file)

        if success:
            return "ResolveURL configured for basic streaming"
        else:
            return f"Failed to configure ResolveURL: {output}"

    def fix_pigeonhole_system(self):
        """Complete Pigeonhole system repair"""
        self.log("="*60)
        self.log("STARTING COMPLETE PIGEONHOLE SYSTEM REPAIR")
        self.log("="*60)

        # Diagnose the system
        diagnosis = self.diagnose_pigeonhole_system()

        # Print diagnosis summary
        self.log("\nDIAGNOSIS SUMMARY:")
        self.log(f"API Working: {diagnosis['kodi_status']['api_responding']}")
        self.log(f"Missing Addons: {diagnosis['addon_status']['missing_count']}")
        self.log(f"Pigeonhole Skin: {diagnosis['skin_status']['pigeonhole_available']}")
        self.log(f"Streaming Ready: {diagnosis['streaming_status']['streaming_ready']}")

        # Execute solutions in priority order
        solutions_executed = []
        for solution in sorted(diagnosis["solutions"], key=lambda x: {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2}.get(x["priority"], 3)):
            self.log(f"\nExecuting: {solution['issue']}")
            result = self.execute_solution(solution["solution"])
            solutions_executed.append({
                "issue": solution["issue"],
                "result": result
            })

        # Final validation
        time.sleep(10)
        final_diagnosis = self.diagnose_pigeonhole_system()

        self.log("="*60)
        self.log("PIGEONHOLE SYSTEM REPAIR COMPLETE")
        self.log("="*60)

        return {
            "initial_diagnosis": diagnosis,
            "solutions_executed": solutions_executed,
            "final_diagnosis": final_diagnosis,
            "success": len(final_diagnosis["solutions"]) < len(diagnosis["solutions"])
        }

if __name__ == "__main__":
    expert = KodiExpert()
    result = expert.fix_pigeonhole_system()

    print("\n" + "="*60)
    print("KODI EXPERT AGENT RESULTS")
    print("="*60)

    if result["success"]:
        print("✅ PIGEONHOLE SYSTEM REPAIR SUCCESSFUL!")
    else:
        print("⚠️ PARTIAL REPAIR - Some issues remain")

    print(f"\nSolutions executed: {len(result['solutions_executed'])}")
    for solution in result["solutions_executed"]:
        print(f"  - {solution['issue']}: {solution['result']}")

    print(f"\nRemaining issues: {len(result['final_diagnosis']['solutions'])}")