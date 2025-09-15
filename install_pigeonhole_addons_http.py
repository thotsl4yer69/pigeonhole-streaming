#!/usr/bin/env python3
"""
HTTP-Based Pigeonhole Addon Installation System
Install core streaming addons using HTTP API for reliable deployment
"""

import requests
import json
import base64
import time
import os
import subprocess
from datetime import datetime

class PigeonholeAddonInstaller:
    def __init__(self):
        self.fire_tv_ip = "192.168.1.130"
        self.http_port = 8080
        self.adb_port = 5555
        self.username = "kodi"
        self.password = "0000"
        self.base_url = f"http://{self.fire_tv_ip}:{self.http_port}/jsonrpc"

        # Create auth header
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_credentials}"
        }

        self.installation_log = []
        self.installation_status = {
            "repositories_installed": [],
            "addons_installed": [],
            "failed_installations": [],
            "manual_steps_required": []
        }

    def log(self, message, level="INFO"):
        """Enhanced logging with installation tracking"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        self.installation_log.append(log_entry)

    def send_rpc_request(self, method, params=None, timeout=15):
        """Send JSON-RPC request to Kodi"""
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "id": 1
        }
        if params:
            payload["params"] = params

        try:
            response = requests.post(
                self.base_url,
                json=payload,
                headers=self.headers,
                timeout=timeout
            )

            if response.status_code == 200:
                result = response.json()
                if "error" in result:
                    self.log(f"Kodi API Error: {result['error']}", "ERROR")
                    return None
                return result.get("result", result)
            else:
                self.log(f"HTTP Error {response.status_code}", "ERROR")
                return None

        except requests.exceptions.RequestException as e:
            self.log(f"Connection error: {e}", "ERROR")
            return None

    def test_connection(self):
        """Test HTTP API connectivity"""
        self.log("Testing Kodi HTTP API connection...")

        response = self.send_rpc_request("JSONRPC.Ping")
        if response and response == "pong":
            self.log("[OK] HTTP API connection successful")
            return True
        else:
            self.log("[FAIL] HTTP API connection failed", "ERROR")
            return False

    def check_adb_availability(self):
        """Check if ADB is available for file operations"""
        try:
            result = subprocess.run(
                f"adb connect {self.fire_tv_ip}:{self.adb_port}",
                shell=True, capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                # Test actual ADB functionality
                test_result = subprocess.run(
                    f"adb -s {self.fire_tv_ip}:{self.adb_port} shell echo test",
                    shell=True, capture_output=True, text=True, timeout=10
                )
                if test_result.returncode == 0:
                    self.log("[OK] ADB connection available")
                    return True
            self.log("[WARN] ADB not available - will use manual installation steps")
            return False
        except Exception as e:
            self.log("[WARN] ADB not available")
            return False

    def get_installed_repositories(self):
        """Get list of currently installed repositories"""
        self.log("Checking installed repositories...")

        repos_response = self.send_rpc_request("Addons.GetAddons", {
            "type": "xbmc.addon.repository",
            "properties": ["name", "version", "enabled"]
        })

        if repos_response and "addons" in repos_response:
            repositories = repos_response["addons"]
            self.log(f"[OK] Found {len(repositories)} installed repositories:")

            for repo in repositories:
                repo_status = "enabled" if repo["enabled"] else "disabled"
                self.log(f"  - {repo['name']} v{repo['version']} ({repo_status})")

            return repositories
        else:
            self.log("[WARN] Could not retrieve repository list")
            return []

    def get_installed_addons(self):
        """Get comprehensive list of installed addons"""
        self.log("Checking installed addons...")

        addons_response = self.send_rpc_request("Addons.GetAddons", {
            "properties": ["name", "version", "enabled", "broken", "type"]
        })

        if addons_response and "addons" in addons_response:
            addons = addons_response["addons"]
            self.log(f"[OK] Found {len(addons)} total installed addons")
            return addons
        else:
            self.log("[WARN] Could not retrieve addon list")
            return []

    def check_core_addons_status(self):
        """Check status of core Pigeonhole addons"""
        self.log("Checking core Pigeonhole addon status...")

        core_addons = {
            "skin.arctic.zephyr.pigeonhole": "Arctic Zephyr Pigeonhole Skin",
            "script.module.resolveurl": "ResolveURL",
            "plugin.video.thecrew": "The Crew",
            "plugin.video.fen.lite": "FEN Lite",
            "plugin.video.madtitansports": "Mad Titan Sports",
            "script.pigeonhole.config": "Pigeonhole Configuration"
        }

        installed_addons = self.get_installed_addons()
        addon_lookup = {addon["addonid"]: addon for addon in installed_addons}

        addon_status = {}
        missing_addons = []
        working_addons = []

        for addon_id, addon_name in core_addons.items():
            if addon_id in addon_lookup:
                addon_info = addon_lookup[addon_id]
                status = {
                    "present": True,
                    "enabled": addon_info["enabled"],
                    "broken": addon_info["broken"],
                    "version": addon_info["version"],
                    "working": addon_info["enabled"] and not addon_info["broken"]
                }
                addon_status[addon_id] = status

                if status["working"]:
                    self.log(f"  [OK] {addon_name} v{addon_info['version']}")
                    working_addons.append(addon_id)
                else:
                    self.log(f"  [ISSUE] {addon_name} - disabled or broken")
            else:
                addon_status[addon_id] = {
                    "present": False,
                    "enabled": False,
                    "broken": False,
                    "version": "Not installed",
                    "working": False
                }
                self.log(f"  [MISSING] {addon_name}")
                missing_addons.append(addon_id)

        self.log(f"Core addon summary: {len(working_addons)}/{len(core_addons)} working properly")
        return addon_status, missing_addons, working_addons

    def install_repository_via_adb(self, repo_file):
        """Install repository via ADB file push"""
        self.log(f"Installing repository {repo_file} via ADB...")

        try:
            if not os.path.exists(repo_file):
                self.log(f"[FAIL] Repository file not found: {repo_file}", "ERROR")
                return False

            # Target path on Fire TV
            target_path = "/sdcard/Download/"
            repo_filename = os.path.basename(repo_file)

            # Push repository file
            push_result = subprocess.run(
                f"adb -s {self.fire_tv_ip}:{self.adb_port} push \"{repo_file}\" {target_path}{repo_filename}",
                shell=True, capture_output=True, text=True, timeout=60
            )

            if push_result.returncode == 0:
                self.log(f"[OK] Repository file pushed to {target_path}{repo_filename}")

                # Now install via HTTP API (Install from zip file)
                install_response = self.send_rpc_request("Addons.InstallAddon", {
                    "addonid": f"zip://{target_path}{repo_filename}/",
                    "wait": True
                })

                if install_response:
                    self.log(f"[OK] Repository {repo_filename} installed successfully")
                    self.installation_status["repositories_installed"].append(repo_filename)
                    return True
                else:
                    self.log(f"[FAIL] Failed to install repository {repo_filename}")
                    return False
            else:
                self.log(f"[FAIL] Failed to push repository file: {push_result.stderr}")
                return False

        except Exception as e:
            self.log(f"[FAIL] Repository installation failed: {e}", "ERROR")
            return False

    def install_primary_repositories(self):
        """Install the primary Pigeonhole repositories"""
        self.log("Installing primary Pigeonhole repositories...")

        # Repository files in priority order
        repository_files = [
            "M:\\repository.pigeonhole.streaming-FIXED.zip",
            "M:\\pigeonhole-streaming-repository.zip",
            "M:\\repository.tikipeter.zip",
            "M:\\repository.nixgates.zip"
        ]

        adb_available = self.check_adb_availability()
        installations_successful = 0

        for repo_file in repository_files:
            if os.path.exists(repo_file):
                repo_name = os.path.basename(repo_file)
                self.log(f"Processing {repo_name}...")

                if adb_available:
                    if self.install_repository_via_adb(repo_file):
                        installations_successful += 1
                        time.sleep(3)  # Brief pause between installations
                else:
                    self.log(f"[MANUAL] Manual installation required for {repo_name}")
                    self.installation_status["manual_steps_required"].append(
                        f"Install {repo_name} via Kodi: Add-ons > Install from zip file"
                    )
            else:
                self.log(f"[WARN] Repository file not found: {repo_file}")

        if adb_available:
            self.log(f"Repository installation complete: {installations_successful}/{len(repository_files)} successful")
            return installations_successful > 0
        else:
            self.log("[MANUAL] All repositories require manual installation")
            return False

    def enable_addon_sources(self):
        """Enable unknown sources and configure addon settings"""
        self.log("Configuring addon installation settings...")

        settings_to_configure = [
            {
                "setting": "addons.unknownsources",
                "value": True,
                "description": "Enable unknown sources"
            },
            {
                "setting": "general.addonupdates",
                "value": 0,  # Disabled
                "description": "Disable automatic addon updates"
            },
            {
                "setting": "general.addonnotifications",
                "value": True,
                "description": "Enable addon notifications"
            }
        ]

        configured_count = 0
        for setting in settings_to_configure:
            response = self.send_rpc_request("Settings.SetSettingValue", {
                "setting": setting["setting"],
                "value": setting["value"]
            })

            if response is True:
                self.log(f"  [OK] {setting['description']}")
                configured_count += 1
            else:
                self.log(f"  [WARN] {setting['description']} - may not be configurable")

        self.log(f"Configured {configured_count}/{len(settings_to_configure)} addon settings")
        return configured_count > 0

    def wait_for_repository_refresh(self):
        """Wait for repository refresh and addon database update"""
        self.log("Waiting for repository refresh...")

        # Trigger repository update
        update_response = self.send_rpc_request("Addons.SetAddonEnabled", {
            "addonid": "repository.pigeonhole.streaming",
            "enabled": True
        })

        # Wait for refresh
        time.sleep(10)

        self.log("[OK] Repository refresh completed")
        return True

    def install_core_addons_from_repository(self):
        """Install core addons from the Pigeonhole repository"""
        self.log("Installing core addons from repository...")

        core_addons_to_install = [
            "script.module.resolveurl",
            "plugin.video.thecrew",
            "plugin.video.fen.lite",
            "plugin.video.madtitansports"
        ]

        installation_results = {}

        for addon_id in core_addons_to_install:
            self.log(f"Installing {addon_id}...")

            install_response = self.send_rpc_request("Addons.InstallAddon", {
                "addonid": addon_id,
                "wait": True
            })

            if install_response:
                self.log(f"  [OK] {addon_id} installation initiated")
                installation_results[addon_id] = True
                self.installation_status["addons_installed"].append(addon_id)
            else:
                self.log(f"  [FAIL] {addon_id} installation failed")
                installation_results[addon_id] = False
                self.installation_status["failed_installations"].append(addon_id)

            time.sleep(5)  # Pause between installations

        successful_installs = sum(1 for success in installation_results.values() if success)
        self.log(f"Addon installation results: {successful_installs}/{len(core_addons_to_install)} successful")

        return successful_installs > 0

    def generate_manual_installation_guide(self):
        """Generate step-by-step manual installation guide"""
        self.log("Generating manual installation guide...")

        guide = []
        guide.append("="*60)
        guide.append("PIGEONHOLE MANUAL INSTALLATION GUIDE")
        guide.append("="*60)
        guide.append("")

        if self.installation_status["manual_steps_required"]:
            guide.append("REPOSITORY INSTALLATION:")
            guide.append("1. Open Kodi")
            guide.append("2. Go to Settings > Add-ons")
            guide.append("3. Select 'Install from zip file'")
            guide.append("4. Enable 'Unknown sources' if prompted")
            guide.append("5. Navigate to the following files and install:")

            for step in self.installation_status["manual_steps_required"]:
                guide.append(f"   - {step}")

            guide.append("")

        if self.installation_status["failed_installations"]:
            guide.append("ADDON INSTALLATION:")
            guide.append("1. After installing repositories, go to Add-ons > Install from repository")
            guide.append("2. Select 'Pigeonhole Streaming Repository'")
            guide.append("3. Install the following addons:")

            for addon in self.installation_status["failed_installations"]:
                guide.append(f"   - {addon}")

            guide.append("")

        guide.append("CONFIGURATION:")
        guide.append("1. Configure ResolveURL with Real-Debrid API key")
        guide.append("2. Configure The Crew with Real-Debrid account")
        guide.append("3. Configure FEN Lite with Real-Debrid account")
        guide.append("4. Test streaming functionality")
        guide.append("")
        guide.append("="*60)

        # Save guide to file
        guide_file = f"M:\\pigeonhole_manual_install_guide_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(guide_file, 'w') as f:
            f.write("\n".join(guide))

        self.log(f"[OK] Manual installation guide saved: {guide_file}")
        return guide_file

    def print_installation_summary(self):
        """Print comprehensive installation summary"""
        print("\n" + "="*80)
        print("PIGEONHOLE ADDON INSTALLATION SUMMARY")
        print("="*80)

        print(f"Target Device: {self.fire_tv_ip}:{self.http_port}")
        print(f"Installation Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        if self.installation_status["repositories_installed"]:
            print(f"\n[SUCCESS] Repositories Installed ({len(self.installation_status['repositories_installed'])}):")
            for repo in self.installation_status["repositories_installed"]:
                print(f"  - {repo}")

        if self.installation_status["addons_installed"]:
            print(f"\n[SUCCESS] Addons Installed ({len(self.installation_status['addons_installed'])}):")
            for addon in self.installation_status["addons_installed"]:
                print(f"  - {addon}")

        if self.installation_status["failed_installations"]:
            print(f"\n[MANUAL] Failed Installations ({len(self.installation_status['failed_installations'])}):")
            for addon in self.installation_status["failed_installations"]:
                print(f"  - {addon}")

        if self.installation_status["manual_steps_required"]:
            print(f"\n[MANUAL] Manual Steps Required ({len(self.installation_status['manual_steps_required'])}):")
            for step in self.installation_status["manual_steps_required"]:
                print(f"  - {step}")

        # Overall assessment
        total_components = len(self.installation_status["repositories_installed"]) + len(self.installation_status["addons_installed"])
        if total_components > 0:
            print(f"\n[STATUS] Installation successful with {total_components} components installed")
        else:
            print(f"\n[STATUS] Manual installation required - see generated guide")

        print("="*80)

    def run_addon_installation(self):
        """Execute complete addon installation process"""
        self.log("="*60)
        self.log("STARTING PIGEONHOLE ADDON INSTALLATION")
        self.log("="*60)

        # Test connection
        if not self.test_connection():
            return False

        # Check current status
        addon_status, missing_addons, working_addons = self.check_core_addons_status()

        if len(working_addons) >= 3:
            self.log("[SUCCESS] Most core addons already installed and working")
            self.print_installation_summary()
            return True

        # Enable addon sources
        self.enable_addon_sources()

        # Install repositories
        self.install_primary_repositories()

        # Wait for repository refresh
        self.wait_for_repository_refresh()

        # Install core addons
        self.install_core_addons_from_repository()

        # Check final status
        final_addon_status, final_missing, final_working = self.check_core_addons_status()

        # Generate manual installation guide if needed
        if final_missing or self.installation_status["manual_steps_required"]:
            self.generate_manual_installation_guide()

        # Print summary
        self.print_installation_summary()

        return len(final_working) > len(working_addons)

def main():
    """Main installation execution"""
    installer = PigeonholeAddonInstaller()

    success = installer.run_addon_installation()

    if success:
        print("\n[SUCCESS] Pigeonhole addon installation completed!")
        print("Configure Real-Debrid settings in the installed addons.")
    else:
        print("\n[MANUAL] Manual installation steps may be required.")
        print("Check the generated installation guide for details.")

if __name__ == "__main__":
    main()