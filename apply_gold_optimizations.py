#!/usr/bin/env python3
"""
Apply Gold Build Cache and Performance Optimizations
Deploy advanced settings and perform system optimizations
"""

import requests
import json
import base64
import time
import os
import subprocess
from datetime import datetime

class GoldBuildOptimizer:
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

        self.optimization_log = []

    def log(self, message, level="INFO"):
        """Enhanced logging"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        self.optimization_log.append(log_entry)

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
        """Test both HTTP API and ADB connectivity"""
        self.log("Testing system connectivity...")

        # Test HTTP API
        response = self.send_rpc_request("JSONRPC.Ping")
        if response and response == "pong":
            self.log("[OK] HTTP API connection successful")
            http_ok = True
        else:
            self.log("[FAIL] HTTP API connection failed", "ERROR")
            http_ok = False

        # Test ADB if available
        adb_ok = False
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
                    self.log("[OK] ADB connection successful")
                    adb_ok = True
                else:
                    self.log("[WARN] ADB connection failed")
            else:
                self.log("[WARN] ADB not available")
        except Exception as e:
            self.log("[WARN] ADB not available or failed")

        return http_ok, adb_ok

    def deploy_advanced_settings_adb(self):
        """Deploy advanced settings XML file via ADB"""
        self.log("Deploying advanced settings via ADB...")

        try:
            # Check if advanced settings file exists
            if not os.path.exists("M:\\advanced_cache_settings.xml"):
                self.log("[FAIL] Advanced settings file not found", "ERROR")
                return False

            # Push advanced settings to Kodi userdata directory
            kodi_userdata_path = "/sdcard/Android/data/org.xbmc.kodi/files/.kodi/userdata/"

            # Create userdata directory if it doesn't exist
            mkdir_result = subprocess.run(
                f"adb -s {self.fire_tv_ip}:{self.adb_port} shell mkdir -p {kodi_userdata_path}",
                shell=True, capture_output=True, text=True, timeout=30
            )

            # Push the advanced settings file
            push_result = subprocess.run(
                f"adb -s {self.fire_tv_ip}:{self.adb_port} push \"M:\\advanced_cache_settings.xml\" {kodi_userdata_path}advancedsettings.xml",
                shell=True, capture_output=True, text=True, timeout=30
            )

            if push_result.returncode == 0:
                self.log("[OK] Advanced settings deployed successfully")

                # Set proper permissions
                chmod_result = subprocess.run(
                    f"adb -s {self.fire_tv_ip}:{self.adb_port} shell chmod 644 {kodi_userdata_path}advancedsettings.xml",
                    shell=True, capture_output=True, text=True, timeout=10
                )

                self.log("[OK] File permissions set")
                return True
            else:
                self.log(f"[FAIL] Failed to push advanced settings: {push_result.stderr}", "ERROR")
                return False

        except Exception as e:
            self.log(f"[FAIL] ADB deployment failed: {e}", "ERROR")
            return False

    def apply_kodi_settings_http(self):
        """Apply optimization settings via HTTP API"""
        self.log("Applying Kodi optimizations via HTTP API...")

        optimization_settings = [
            # Video player optimizations
            {
                "setting": "videoplayer.usemediacodec",
                "value": True,
                "description": "Enable MediaCodec hardware acceleration"
            },
            {
                "setting": "videoplayer.useamcodec",
                "value": True,
                "description": "Enable AMCodec acceleration"
            },
            {
                "setting": "videoplayer.adjustrefreshrate",
                "value": 2,  # Always adjust
                "description": "Always adjust refresh rate"
            },
            {
                "setting": "videoplayer.pauseafterrefreshchange",
                "value": 0.1,
                "description": "Minimal pause after refresh change"
            },

            # Audio optimizations
            {
                "setting": "audiooutput.passthrough",
                "value": True,
                "description": "Enable audio passthrough"
            },
            {
                "setting": "audiooutput.passthroughdevice",
                "value": "HDMI",
                "description": "Use HDMI for passthrough"
            },

            # Network optimizations
            {
                "setting": "network.usehttpproxy",
                "value": False,
                "description": "Disable HTTP proxy"
            },

            # Interface optimizations
            {
                "setting": "lookandfeel.skin",
                "value": "skin.arctic.zephyr.pigeonhole",
                "description": "Set Pigeonhole skin as default"
            },
            {
                "setting": "filelists.showparentdiritems",
                "value": False,
                "description": "Hide parent directory items"
            },
            {
                "setting": "filelists.showextensions",
                "value": False,
                "description": "Hide file extensions"
            },
            {
                "setting": "debug.showloginfo",
                "value": False,
                "description": "Disable debug overlay"
            },
            {
                "setting": "general.addonupdates",
                "value": 0,  # Disabled
                "description": "Disable automatic addon updates"
            }
        ]

        applied_count = 0
        failed_count = 0

        for setting in optimization_settings:
            response = self.send_rpc_request("Settings.SetSettingValue", {
                "setting": setting["setting"],
                "value": setting["value"]
            })

            if response is True:
                self.log(f"  [OK] {setting['description']}")
                applied_count += 1
            else:
                self.log(f"  [WARN] {setting['description']} - may not be available")
                failed_count += 1

            time.sleep(0.5)  # Brief pause between settings

        self.log(f"Applied {applied_count}/{len(optimization_settings)} optimization settings")
        self.log(f"Failed/Unavailable: {failed_count}")

        return applied_count > len(optimization_settings) // 2

    def restart_kodi(self, method="http"):
        """Restart Kodi to apply advanced settings"""
        self.log(f"Restarting Kodi via {method.upper()}...")

        if method == "adb":
            try:
                # Force stop Kodi
                stop_result = subprocess.run(
                    f"adb -s {self.fire_tv_ip}:{self.adb_port} shell am force-stop org.xbmc.kodi",
                    shell=True, capture_output=True, text=True, timeout=10
                )

                time.sleep(3)

                # Start Kodi
                start_result = subprocess.run(
                    f"adb -s {self.fire_tv_ip}:{self.adb_port} shell am start -n org.xbmc.kodi/.Splash",
                    shell=True, capture_output=True, text=True, timeout=10
                )

                if start_result.returncode == 0:
                    self.log("[OK] Kodi restarted successfully via ADB")
                    return True
                else:
                    self.log("[FAIL] Failed to restart Kodi via ADB", "ERROR")
                    return False

            except Exception as e:
                self.log(f"[FAIL] ADB restart failed: {e}", "ERROR")
                return False

        elif method == "http":
            # Try to restart via HTTP API
            response = self.send_rpc_request("System.Reboot")
            if response:
                self.log("[OK] Restart command sent via HTTP")
                return True
            else:
                self.log("[WARN] HTTP restart may not be supported")
                return False

    def verify_optimizations(self):
        """Verify that optimizations were applied"""
        self.log("Verifying applied optimizations...")

        # Wait for Kodi to restart
        self.log("Waiting for Kodi to restart...")
        time.sleep(15)

        # Test connection after restart
        max_retries = 6
        for attempt in range(max_retries):
            response = self.send_rpc_request("JSONRPC.Ping", timeout=5)
            if response and response == "pong":
                self.log("[OK] Kodi is responding after restart")
                break
            else:
                self.log(f"  Attempt {attempt + 1}/{max_retries} - waiting for Kodi...")
                time.sleep(5)
        else:
            self.log("[WARN] Kodi may still be starting up", "ERROR")
            return False

        # Verify key settings
        verification_settings = [
            "lookandfeel.skin",
            "videoplayer.usemediacodec",
            "debug.showloginfo"
        ]

        verified_count = 0
        for setting in verification_settings:
            response = self.send_rpc_request("Settings.GetSettingValue", {
                "setting": setting
            })

            if response and "value" in response:
                value = response["value"]
                self.log(f"  [OK] {setting} = {value}")
                verified_count += 1
            else:
                self.log(f"  [WARN] Could not verify {setting}")

        self.log(f"Verified {verified_count}/{len(verification_settings)} settings")
        return verified_count > 0

    def clean_cache_and_optimize(self):
        """Clean cache and apply final optimizations"""
        self.log("Performing cache cleanup and final optimizations...")

        # Clear various caches via HTTP API
        cache_operations = [
            ("Textures.GetTextures", "Get texture cache"),
            ("VideoLibrary.Clean", "Clean video library"),
            ("AudioLibrary.Clean", "Clean audio library")
        ]

        for operation, description in cache_operations:
            self.log(f"  {description}...")
            try:
                response = self.send_rpc_request(operation)
                if response:
                    self.log(f"    [OK] {description} completed")
                else:
                    self.log(f"    [WARN] {description} may not be supported")
            except:
                self.log(f"    [WARN] {description} failed")

        return True

    def run_gold_optimization(self):
        """Execute complete Gold Build optimization"""
        self.log("="*60)
        self.log("STARTING FIRE TV CUBE GOLD BUILD OPTIMIZATION")
        self.log("="*60)

        # Test connectivity
        http_ok, adb_ok = self.test_connection()

        if not http_ok:
            self.log("[FAIL] Cannot proceed without HTTP API", "ERROR")
            return False

        optimization_success = True

        # Apply HTTP-based optimizations
        if not self.apply_kodi_settings_http():
            optimization_success = False

        # Deploy advanced settings if ADB is available
        if adb_ok:
            if self.deploy_advanced_settings_adb():
                self.log("[OK] Advanced settings deployed - restart required")

                # Restart Kodi to apply advanced settings
                if self.restart_kodi("adb"):
                    # Verify optimizations after restart
                    self.verify_optimizations()
                else:
                    optimization_success = False
            else:
                optimization_success = False
        else:
            self.log("[WARN] ADB not available - advanced settings require manual deployment")
            self.log("  Manual step: Copy M:\\advanced_cache_settings.xml to Kodi userdata folder")

        # Final cleanup and optimization
        self.clean_cache_and_optimize()

        # Summary
        print("\n" + "="*60)
        print("GOLD BUILD OPTIMIZATION SUMMARY")
        print("="*60)

        if optimization_success:
            print("[SUCCESS] Gold Build optimizations applied successfully!")
            print("\n[APPLIED] Optimizations:")
            print("  - Hardware acceleration enabled")
            print("  - Video/audio settings optimized")
            print("  - Interface optimized")
            print("  - Debug overlay disabled")
            if adb_ok:
                print("  - Advanced cache settings deployed")

        else:
            print("[PARTIAL] Gold Build optimizations partially applied")
            print("\n[MANUAL] Manual steps may be required")

        print(f"\n[LOGS] Total operations: {len(self.optimization_log)}")
        print("="*60)

        return optimization_success

def main():
    """Main optimization execution"""
    optimizer = GoldBuildOptimizer()

    success = optimizer.run_gold_optimization()

    if success:
        print("\n[SUCCESS] Gold Build optimization completed!")
        print("Your Fire TV Cube is now optimized for streaming.")
    else:
        print("\n[PARTIAL] Optimization completed with some manual steps required.")

if __name__ == "__main__":
    main()