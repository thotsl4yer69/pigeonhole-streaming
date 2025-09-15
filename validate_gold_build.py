#!/usr/bin/env python3
"""
Fire TV Cube Gold Build Validator - Pigeonhole Streaming
Comprehensive validation of optimized Kodi v22 system
"""

import subprocess
import requests
import json
import base64
import time
import sys
from datetime import datetime

class GoldBuildValidator:
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

        # Expected performance benchmarks
        self.performance_targets = {
            "api_response_time": 1.0,  # seconds
            "startup_time": 15.0,      # seconds
            "memory_threshold": 512,   # MB minimum free
            "cpu_threshold": 80,       # max CPU usage %
        }

        # Required Pigeonhole addons
        self.required_addons = [
            "skin.arctic.zephyr.pigeonhole",
            "script.module.resolveurl",
            "plugin.video.thecrew",
            "plugin.video.fen.lite",
            "script.pigeonhole.config",
            "repository.pigeonhole.streaming",
        ]

        # Validation results
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests_passed": 0,
            "tests_failed": 0,
            "critical_failures": [],
            "warnings": [],
            "performance_metrics": {},
            "system_info": {}
        }

    def log(self, message, level="INFO"):
        """Enhanced logging with results tracking"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")

        if level == "ERROR":
            self.results["tests_failed"] += 1
            self.results["critical_failures"].append(message)
        elif level == "WARN":
            self.results["warnings"].append(message)
        elif level == "SUCCESS":
            self.results["tests_passed"] += 1

    def adb_command(self, command):
        """Execute ADB command with timeout"""
        try:
            full_command = f"adb -s {self.fire_tv_ip}:5555 {command}"
            result = subprocess.run(full_command, shell=True, capture_output=True, text=True, timeout=30)
            return result.returncode == 0, result.stdout.strip()
        except Exception as e:
            return False, str(e)

    def kodi_jsonrpc(self, method, params=None):
        """Execute Kodi JSON-RPC call with timing"""
        try:
            start_time = time.time()

            payload = {
                "jsonrpc": "2.0",
                "method": method,
                "id": 1
            }
            if params:
                payload["params"] = params

            response = requests.post(self.base_url, json=payload, headers=self.headers, timeout=15)
            response_time = time.time() - start_time

            if method == "JSONRPC.Ping":
                self.results["performance_metrics"]["api_response_time"] = response_time

            if response.status_code == 200:
                result = response.json()
                return result.get("result", result)
            else:
                return None
        except Exception as e:
            self.log(f"Kodi API error: {e}", "ERROR")
            return None

    def test_system_connectivity(self):
        """Test basic system connectivity"""
        self.log("Testing system connectivity...")

        # Test ADB connection
        success, output = self.adb_command("shell echo 'ADB_OK'")
        if success and "ADB_OK" in output:
            self.log("✅ ADB connection verified", "SUCCESS")
        else:
            self.log("❌ ADB connection failed", "ERROR")
            return False

        # Test Kodi HTTP API
        result = self.kodi_jsonrpc("JSONRPC.Ping")
        if result == "pong":
            response_time = self.results["performance_metrics"].get("api_response_time", 0)
            if response_time <= self.performance_targets["api_response_time"]:
                self.log(f"✅ Kodi HTTP API responding ({response_time:.2f}s)", "SUCCESS")
            else:
                self.log(f"⚠️ Kodi HTTP API slow ({response_time:.2f}s)", "WARN")
            return True
        else:
            self.log("❌ Kodi HTTP API not responding", "ERROR")
            return False

    def test_system_information(self):
        """Gather and validate system information"""
        self.log("Gathering system information...")

        # Get Kodi system info
        system_info = self.kodi_jsonrpc("System.GetInfoLabels", {
            "labels": [
                "System.BuildVersion",
                "System.FreeMemory",
                "System.CPUUsage",
                "System.Uptime",
                "Skin.CurrentSkin",
                "System.TotalUptime"
            ]
        })

        if system_info:
            self.results["system_info"] = system_info

            # Validate Kodi version
            version = system_info.get("System.BuildVersion", "Unknown")
            if "22." in version:
                self.log(f"✅ Kodi v22 confirmed: {version}", "SUCCESS")
            else:
                self.log(f"⚠️ Unexpected Kodi version: {version}", "WARN")

            # Check memory
            free_memory = system_info.get("System.FreeMemory", "0 MB")
            try:
                memory_mb = int(free_memory.split()[0])
                self.results["performance_metrics"]["free_memory_mb"] = memory_mb
                if memory_mb >= self.performance_targets["memory_threshold"]:
                    self.log(f"✅ Sufficient free memory: {free_memory}", "SUCCESS")
                else:
                    self.log(f"⚠️ Low memory: {free_memory}", "WARN")
            except:
                self.log(f"⚠️ Could not parse memory: {free_memory}", "WARN")

            # Check CPU usage
            cpu_usage = system_info.get("System.CPUUsage", "0%")
            try:
                cpu_percent = int(cpu_usage.rstrip('%'))
                self.results["performance_metrics"]["cpu_usage_percent"] = cpu_percent
                if cpu_percent <= self.performance_targets["cpu_threshold"]:
                    self.log(f"✅ CPU usage acceptable: {cpu_usage}", "SUCCESS")
                else:
                    self.log(f"⚠️ High CPU usage: {cpu_usage}", "WARN")
            except:
                self.log(f"⚠️ Could not parse CPU usage: {cpu_usage}", "WARN")

            # Check skin
            skin = system_info.get("Skin.CurrentSkin", "Unknown")
            if "pigeonhole" in skin.lower() or "arctic" in skin.lower():
                self.log(f"✅ Pigeonhole skin active: {skin}", "SUCCESS")
            else:
                self.log(f"⚠️ Non-Pigeonhole skin: {skin}", "WARN")

            return True
        else:
            self.log("❌ Could not get system information", "ERROR")
            return False

    def test_addon_configuration(self):
        """Test addon configuration and status"""
        self.log("Testing addon configuration...")

        # Get all addons
        result = self.kodi_jsonrpc("Addons.GetAddons", {
            "properties": ["name", "version", "enabled", "broken", "type"]
        })

        if not result or "addons" not in result:
            self.log("❌ Could not get addon list", "ERROR")
            return False

        addons = result["addons"]
        addon_dict = {addon["addonid"]: addon for addon in addons}

        self.log(f"Found {len(addons)} total addons")

        # Check required addons
        required_found = 0
        for required_addon in self.required_addons:
            if required_addon in addon_dict:
                addon = addon_dict[required_addon]
                if addon["enabled"] and not addon["broken"]:
                    self.log(f"✅ {addon['name']} v{addon['version']}", "SUCCESS")
                    required_found += 1
                else:
                    status = "broken" if addon["broken"] else "disabled"
                    self.log(f"❌ {addon['name']} is {status}", "ERROR")
            else:
                self.log(f"❌ Missing required addon: {required_addon}", "ERROR")

        # Calculate success rate
        success_rate = (required_found / len(self.required_addons)) * 100
        self.results["performance_metrics"]["addon_success_rate"] = success_rate

        if success_rate >= 80:
            self.log(f"✅ Core addons operational: {required_found}/{len(self.required_addons)} ({success_rate:.0f}%)", "SUCCESS")
            return True
        else:
            self.log(f"❌ Critical addon failures: {required_found}/{len(self.required_addons)} ({success_rate:.0f}%)", "ERROR")
            return False

    def test_launcher_configuration(self):
        """Test Fire TV launcher configuration"""
        self.log("Testing launcher configuration...")

        # Check default launcher
        success, output = self.adb_command("shell cmd package resolve-activity --brief -c android.intent.category.HOME")
        if success:
            if "org.xbmc.kodi" in output:
                self.log("✅ Kodi set as default launcher", "SUCCESS")
                return True
            elif "amazon.tv.launcher" in output:
                self.log("⚠️ Amazon launcher still default", "WARN")
                return False
            else:
                self.log(f"⚠️ Unexpected launcher: {output}", "WARN")
                return False
        else:
            self.log("❌ Could not check launcher configuration", "ERROR")
            return False

    def test_performance_benchmarks(self):
        """Test system performance benchmarks"""
        self.log("Running performance benchmarks...")

        # Test navigation performance
        start_time = time.time()
        result = self.kodi_jsonrpc("GUI.ActivateWindow", {"window": "home"})
        nav_time = time.time() - start_time

        if result:
            self.results["performance_metrics"]["navigation_time"] = nav_time
            if nav_time <= 2.0:
                self.log(f"✅ Navigation responsive: {nav_time:.2f}s", "SUCCESS")
            else:
                self.log(f"⚠️ Navigation slow: {nav_time:.2f}s", "WARN")

        # Test addon execution
        start_time = time.time()
        result = self.kodi_jsonrpc("Addons.ExecuteAddon", {
            "addonid": "script.pigeonhole.config",
            "wait": False
        })
        addon_time = time.time() - start_time

        if result:
            self.results["performance_metrics"]["addon_execution_time"] = addon_time
            if addon_time <= 3.0:
                self.log(f"✅ Addon execution fast: {addon_time:.2f}s", "SUCCESS")
            else:
                self.log(f"⚠️ Addon execution slow: {addon_time:.2f}s", "WARN")

        return True

    def test_streaming_readiness(self):
        """Test streaming functionality readiness"""
        self.log("Testing streaming readiness...")

        # Test ResolveURL functionality
        result = self.kodi_jsonrpc("Addons.GetAddonDetails", {
            "addonid": "script.module.resolveurl",
            "properties": ["enabled", "broken"]
        })

        if result and result["addon"]["enabled"] and not result["addon"]["broken"]:
            self.log("✅ ResolveURL module ready", "SUCCESS")
        else:
            self.log("❌ ResolveURL module issues", "ERROR")
            return False

        # Test network connectivity
        try:
            test_url = "http://httpbin.org/status/200"
            response = requests.get(test_url, timeout=5)
            if response.status_code == 200:
                self.log("✅ Network connectivity verified", "SUCCESS")
            else:
                self.log("⚠️ Network connectivity issues", "WARN")
        except:
            self.log("⚠️ Could not verify network connectivity", "WARN")

        return True

    def test_debloat_effectiveness(self):
        """Test Amazon debloating effectiveness"""
        self.log("Testing debloat effectiveness...")

        # Check for removed bloatware
        success, output = self.adb_command("shell pm list packages | grep amazon")
        if success:
            amazon_packages = output.split('\n') if output else []
            bloat_count = len([pkg for pkg in amazon_packages if any(bloat in pkg for bloat in [
                "dee.app", "speech.sim", "ags.app", "avod", "bueller", "hedwig", "precog"
            ])])

            self.results["performance_metrics"]["remaining_bloat_packages"] = bloat_count

            if bloat_count == 0:
                self.log("✅ Amazon bloatware successfully removed", "SUCCESS")
            elif bloat_count <= 3:
                self.log(f"⚠️ Some bloatware remains: {bloat_count} packages", "WARN")
            else:
                self.log(f"❌ Debloating incomplete: {bloat_count} bloat packages", "ERROR")
                return False

        # Check launcher
        success, output = self.adb_command("shell pm list packages | grep launcher")
        if success and "amazon.tv.launcher" in output:
            # Check if it's disabled
            success, status = self.adb_command("shell pm list packages -d | grep amazon.tv.launcher")
            if success and status:
                self.log("✅ Amazon launcher disabled", "SUCCESS")
            else:
                self.log("⚠️ Amazon launcher still active", "WARN")

        return True

    def generate_report(self):
        """Generate comprehensive validation report"""
        self.log("Generating validation report...")

        total_tests = self.results["tests_passed"] + self.results["tests_failed"]
        success_rate = (self.results["tests_passed"] / total_tests * 100) if total_tests > 0 else 0

        report = f"""
=========================================================================
FIRE TV CUBE GOLD BUILD VALIDATION REPORT
=========================================================================
Timestamp: {self.results['timestamp']}
Target: {self.fire_tv_ip}:{self.http_port}

SUMMARY
=======
Tests Passed: {self.results['tests_passed']}
Tests Failed: {self.results['tests_failed']}
Success Rate: {success_rate:.1f}%
Warnings: {len(self.results['warnings'])}

SYSTEM INFORMATION
=================="""

        for key, value in self.results["system_info"].items():
            report += f"\n{key}: {value}"

        report += f"""

PERFORMANCE METRICS
==================="""

        for key, value in self.results["performance_metrics"].items():
            if isinstance(value, float):
                report += f"\n{key}: {value:.2f}"
            else:
                report += f"\n{key}: {value}"

        if self.results["critical_failures"]:
            report += f"""

CRITICAL FAILURES
================="""
            for failure in self.results["critical_failures"]:
                report += f"\n❌ {failure}"

        if self.results["warnings"]:
            report += f"""

WARNINGS
========"""
            for warning in self.results["warnings"]:
                report += f"\n⚠️ {warning}"

        report += f"""

GOLD BUILD STATUS
================="""

        if success_rate >= 90:
            report += "\n🏆 GOLD BUILD VALIDATION PASSED!"
            report += "\n✅ System ready for production streaming"
        elif success_rate >= 75:
            report += "\n🥈 SILVER BUILD - Minor issues detected"
            report += "\n⚠️ System functional but not optimal"
        else:
            report += "\n❌ BUILD VALIDATION FAILED"
            report += "\n🚨 Critical issues require attention"

        report += f"""

RECOMMENDATIONS
==============="""

        if success_rate < 90:
            report += "\n• Review critical failures and resolve issues"
            report += "\n• Re-run optimization if necessary"

        if self.results["performance_metrics"].get("free_memory_mb", 1000) < 256:
            report += "\n• Consider reducing active addons for better performance"

        if self.results["performance_metrics"].get("api_response_time", 0) > 1.0:
            report += "\n• Network or system performance may need optimization"

        report += "\n\n========================================================================="

        return report

    def run_full_validation(self):
        """Execute complete validation suite"""
        self.log("=" * 70)
        self.log("FIRE TV CUBE GOLD BUILD VALIDATION")
        self.log("=" * 70)

        validation_tests = [
            ("System Connectivity", self.test_system_connectivity),
            ("System Information", self.test_system_information),
            ("Addon Configuration", self.test_addon_configuration),
            ("Launcher Configuration", self.test_launcher_configuration),
            ("Performance Benchmarks", self.test_performance_benchmarks),
            ("Streaming Readiness", self.test_streaming_readiness),
            ("Debloat Effectiveness", self.test_debloat_effectiveness),
        ]

        for test_name, test_func in validation_tests:
            self.log(f"\n[TEST] {test_name}...")
            try:
                test_func()
            except Exception as e:
                self.log(f"❌ Test {test_name} failed with exception: {e}", "ERROR")

        # Generate and display report
        report = self.generate_report()
        print(report)

        # Save report to file
        report_filename = f"M:\\validation_report_{int(time.time())}.txt"
        with open(report_filename, "w") as f:
            f.write(report)

        self.log(f"Validation report saved: {report_filename}")

        # Return success status
        total_tests = self.results["tests_passed"] + self.results["tests_failed"]
        success_rate = (self.results["tests_passed"] / total_tests * 100) if total_tests > 0 else 0
        return success_rate >= 90

if __name__ == "__main__":
    validator = GoldBuildValidator()
    success = validator.run_full_validation()

    sys.exit(0 if success else 1)