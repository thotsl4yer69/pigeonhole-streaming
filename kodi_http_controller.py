#!/usr/bin/env python3
"""
Pigeonhole Streaming - Kodi HTTP Remote Controller
Real-time testing and optimization via HTTP API
"""

import requests
import json
import time
from datetime import datetime
import base64

class KodiHTTPController:
    def __init__(self):
        self.fire_tv_ip = "192.168.1.130"
        self.http_port = 8080
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
        
        self.test_results = {
            "timestamp": datetime.now().isoformat(),
            "connection_status": False,
            "system_info": {},
            "addon_validation": [],
            "streaming_tests": [],
            "performance_metrics": {},
            "recommendations": []
        }

    def send_rpc_request(self, method, params=None, timeout=10):
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
                return response.json()
            else:
                print(f"HTTP Error {response.status_code}: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}")
            return None

    def test_connection(self):
        """Test HTTP API connection"""
        print("Testing Kodi HTTP API connection...")
        
        response = self.send_rpc_request("JSONRPC.Ping")
        if response and response.get("result") == "pong":
            print("[OK] HTTP API connection successful")
            self.test_results["connection_status"] = True
            return True
        else:
            print("[FAIL] HTTP API connection failed")
            return False

    def get_system_info(self):
        """Get comprehensive system information"""
        print("Gathering system information...")
        
        # Get system info
        system_response = self.send_rpc_request("System.GetInfoLabels", {
            "labels": [
                "System.BuildVersion",
                "System.OSVersionInfo", 
                "System.KernelVersion",
                "System.Uptime",
                "System.TotalUptime",
                "System.FreeMemory",
                "System.UsedMemory",
                "System.CPUUsage",
                "System.CoreTemperature"
            ]
        })
        
        if system_response and "result" in system_response:
            self.test_results["system_info"] = system_response["result"]
            
            # Parse key metrics
            build_version = system_response["result"].get("System.BuildVersion", "Unknown")
            free_memory = system_response["result"].get("System.FreeMemory", "Unknown")
            cpu_usage = system_response["result"].get("System.CPUUsage", "Unknown")
            uptime = system_response["result"].get("System.Uptime", "Unknown")
            
            print(f"[OK] Kodi Version: {build_version}")
            print(f"[OK] Free Memory: {free_memory}")
            print(f"[OK] CPU Usage: {cpu_usage}")
            print(f"[OK] Uptime: {uptime}")
            
            return True
        
        print("[FAIL] Failed to get system information")
        return False

    def validate_installed_addons(self):
        """Validate all installed addons via HTTP API"""
        print("Validating installed addons...")
        
        # Get all installed addons
        addons_response = self.send_rpc_request("Addons.GetAddons", {
            "properties": ["name", "version", "summary", "enabled", "broken"]
        })
        
        if not addons_response or "result" not in addons_response:
            print("✗ Failed to get addon list")
            return False
        
        addons = addons_response["result"].get("addons", [])
        print(f"Found {len(addons)} installed addons")
        
        # Validate our core Pigeonhole addons
        core_addons = [
            "skin.arctic.zephyr.pigeonhole",
            "script.module.resolveurl", 
            "plugin.video.thecrew",
            "plugin.video.madtitansports",
            "plugin.video.fen.lite",
            "script.pigeonhole.config"
        ]
        
        addon_status = {}
        for addon in addons:
            addon_id = addon["addonid"]
            addon_status[addon_id] = {
                "name": addon.get("name", "Unknown"),
                "version": addon.get("version", "Unknown"),
                "enabled": addon.get("enabled", False),
                "broken": addon.get("broken", False),
                "is_core": addon_id in core_addons
            }
            
            # Print status for core addons
            if addon_id in core_addons:
                status = "✓" if addon["enabled"] and not addon["broken"] else "✗"
                print(f"  {status} {addon['name']} v{addon['version']}")
        
        # Check if all core addons are present and working
        core_addon_status = []
        for core_addon in core_addons:
            if core_addon in addon_status:
                addon_info = addon_status[core_addon]
                core_addon_status.append({
                    "addon_id": core_addon,
                    "present": True,
                    "enabled": addon_info["enabled"],
                    "working": not addon_info["broken"],
                    "version": addon_info["version"]
                })
            else:
                core_addon_status.append({
                    "addon_id": core_addon,
                    "present": False,
                    "enabled": False,
                    "working": False,
                    "version": "Not installed"
                })
                print(f"  ✗ {core_addon} - NOT FOUND")
        
        self.test_results["addon_validation"] = core_addon_status
        
        # Summary
        working_core = sum(1 for addon in core_addon_status if addon["present"] and addon["enabled"] and addon["working"])
        print(f"Core addon status: {working_core}/{len(core_addons)} working properly")
        
        return working_core == len(core_addons)

    def test_skin_activation(self):
        """Test Arctic Zephyr Pigeonhole skin activation"""
        print("Testing skin activation...")
        
        # Get current skin
        skin_response = self.send_rpc_request("Settings.GetSettingValue", {
            "setting": "lookandfeel.skin"
        })
        
        if skin_response and "result" in skin_response:
            current_skin = skin_response["result"]["value"]
            print(f"Current skin: {current_skin}")
            
            if "pigeonhole" in current_skin.lower():
                print("✓ Pigeonhole skin is active")
                return True
            else:
                print("⚠ Attempting to activate Pigeonhole skin...")
                # Attempt to set skin
                set_response = self.send_rpc_request("Settings.SetSettingValue", {
                    "setting": "lookandfeel.skin",
                    "value": "skin.arctic.zephyr.pigeonhole"
                })
                if set_response and "result" in set_response:
                    print("✓ Pigeonhole skin activated")
                    return True
                else:
                    print("✗ Failed to activate Pigeonhole skin")
                    return False
        
        print("✗ Failed to get skin information")
        return False

    def test_streaming_addons(self):
        """Test streaming addon functionality"""
        print("Testing streaming addon functionality...")
        
        streaming_tests = []
        
        # Test The Crew addon
        crew_test = self.test_addon_launch("plugin.video.thecrew", "The Crew")
        streaming_tests.append(crew_test)
        
        # Test FEN Lite addon  
        fen_test = self.test_addon_launch("plugin.video.fen.lite", "FEN Lite")
        streaming_tests.append(fen_test)
        
        # Test Mad Titan Sports
        sports_test = self.test_addon_launch("plugin.video.madtitansports", "Mad Titan Sports")
        streaming_tests.append(sports_test)
        
        self.test_results["streaming_tests"] = streaming_tests
        
        working_addons = sum(1 for test in streaming_tests if test["launch_success"])
        print(f"Streaming addon test: {working_addons}/{len(streaming_tests)} addons launched successfully")
        
        return working_addons > 0

    def test_addon_launch(self, addon_id, addon_name):
        """Test individual addon launch"""
        print(f"  Testing {addon_name}...")
        
        test_result = {
            "addon_id": addon_id,
            "addon_name": addon_name,
            "launch_success": False,
            "response_time": None,
            "error": None
        }
        
        try:
            start_time = time.time()
            
            # Execute addon
            launch_response = self.send_rpc_request("Addons.ExecuteAddon", {
                "addonid": addon_id,
                "wait": False
            })
            
            response_time = time.time() - start_time
            test_result["response_time"] = round(response_time, 2)
            
            if launch_response and "result" in launch_response:
                if launch_response["result"] == "OK":
                    print(f"    ✓ {addon_name} launched successfully ({response_time:.2f}s)")
                    test_result["launch_success"] = True
                else:
                    print(f"    ✗ {addon_name} launch failed: {launch_response}")
                    test_result["error"] = str(launch_response)
            else:
                print(f"    ✗ {addon_name} no response or error")
                test_result["error"] = "No response from addon"
                
            # Wait briefly before next test
            time.sleep(2)
            
        except Exception as e:
            test_result["error"] = str(e)
            print(f"    ✗ {addon_name} exception: {e}")
        
        return test_result

    def get_performance_metrics(self):
        """Get detailed performance metrics"""
        print("Collecting performance metrics...")
        
        # Get various performance indicators
        perf_labels = [
            "System.FreeMemory",
            "System.UsedMemory", 
            "System.CPUUsage",
            "Network.IPAddress",
            "System.Uptime",
            "System.IdleTime"
        ]
        
        perf_response = self.send_rpc_request("System.GetInfoLabels", {
            "labels": perf_labels
        })
        
        if perf_response and "result" in perf_response:
            self.test_results["performance_metrics"] = perf_response["result"]
            
            # Parse and display key metrics
            free_mem = perf_response["result"].get("System.FreeMemory", "Unknown")
            used_mem = perf_response["result"].get("System.UsedMemory", "Unknown") 
            cpu_usage = perf_response["result"].get("System.CPUUsage", "Unknown")
            uptime = perf_response["result"].get("System.Uptime", "Unknown")
            
            print(f"  Free Memory: {free_mem}")
            print(f"  Used Memory: {used_mem}")
            print(f"  CPU Usage: {cpu_usage}")
            print(f"  System Uptime: {uptime}")
            
            return True
        
        print("✗ Failed to get performance metrics")
        return False

    def configure_advanced_settings(self):
        """Configure advanced settings via HTTP API"""
        print("Optimizing advanced settings...")
        
        # Key settings to optimize
        settings_to_optimize = [
            {
                "setting": "network.cachemembuffersize", 
                "value": 20971520,  # 20MB
                "description": "Network cache buffer"
            },
            {
                "setting": "videoplayer.usemediacodec",
                "value": 2,  # Force enable
                "description": "MediaCodec acceleration"
            },
            {
                "setting": "debug.showloginfo",
                "value": False,
                "description": "Disable debug overlay"
            }
        ]
        
        optimized_count = 0
        for setting_config in settings_to_optimize:
            response = self.send_rpc_request("Settings.SetSettingValue", {
                "setting": setting_config["setting"],
                "value": setting_config["value"]
            })
            
            if response and "result" in response and response["result"] is True:
                print(f"  ✓ {setting_config['description']}: Optimized")
                optimized_count += 1
            else:
                print(f"  ✗ {setting_config['description']}: Failed to optimize")
        
        print(f"Advanced settings: {optimized_count}/{len(settings_to_optimize)} optimized")
        return optimized_count > 0

    def generate_comprehensive_report(self):
        """Generate comprehensive assessment report"""
        print("\nGenerating comprehensive assessment report...")
        
        # Calculate overall health scores
        addon_health = 0
        if self.test_results["addon_validation"]:
            working_addons = sum(1 for addon in self.test_results["addon_validation"] 
                               if addon["present"] and addon["enabled"] and addon["working"])
            total_addons = len(self.test_results["addon_validation"])
            addon_health = (working_addons / total_addons) * 100 if total_addons > 0 else 0
        
        streaming_health = 0
        if self.test_results["streaming_tests"]:
            working_streams = sum(1 for test in self.test_results["streaming_tests"] 
                                if test["launch_success"])
            total_streams = len(self.test_results["streaming_tests"])
            streaming_health = (working_streams / total_streams) * 100 if total_streams > 0 else 0
        
        # Overall system health
        system_health = (addon_health + streaming_health) / 2
        
        # Generate recommendations
        recommendations = []
        
        if system_health < 80:
            recommendations.append({
                "priority": "HIGH",
                "category": "System Health",
                "issue": f"Overall system health is {system_health:.1f}%",
                "action": "Review addon configurations and run diagnostics"
            })
        
        if addon_health < 100:
            broken_addons = [addon["addon_id"] for addon in self.test_results["addon_validation"]
                           if not (addon["present"] and addon["enabled"] and addon["working"])]
            recommendations.append({
                "priority": "MEDIUM", 
                "category": "Addon Issues",
                "issue": f"Broken addons: {', '.join(broken_addons)}",
                "action": "Reinstall or repair broken addons"
            })
        
        if streaming_health < 100:
            failed_streams = [test["addon_name"] for test in self.test_results["streaming_tests"]
                            if not test["launch_success"]]
            recommendations.append({
                "priority": "MEDIUM",
                "category": "Streaming Issues", 
                "issue": f"Failed streaming addons: {', '.join(failed_streams)}",
                "action": "Check Real Debrid configuration and addon settings"
            })
        
        self.test_results["recommendations"] = recommendations
        self.test_results["health_scores"] = {
            "addon_health": addon_health,
            "streaming_health": streaming_health,
            "system_health": system_health
        }

    def save_assessment_report(self):
        """Save complete assessment report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"M:\\pigeonhole_gold_assessment_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.test_results, f, indent=2)
            print(f"Assessment report saved to: {filename}")
            return filename
        except Exception as e:
            print(f"Failed to save assessment report: {e}")
            return None

    def print_assessment_summary(self):
        """Print comprehensive assessment summary"""
        print("\n" + "="*80)
        print("PIGEONHOLE STREAMING GOLD VERSION - ASSESSMENT SUMMARY")
        print("="*80)
        
        # Connection status
        connection = "✓ CONNECTED" if self.test_results["connection_status"] else "✗ FAILED"
        print(f"HTTP API Connection: {connection}")
        
        # System information
        if self.test_results["system_info"]:
            build = self.test_results["system_info"].get("System.BuildVersion", "Unknown")
            memory = self.test_results["system_info"].get("System.FreeMemory", "Unknown")
            cpu = self.test_results["system_info"].get("System.CPUUsage", "Unknown")
            print(f"Kodi Version: {build}")
            print(f"Free Memory: {memory}")
            print(f"CPU Usage: {cpu}")
        
        # Health scores
        if "health_scores" in self.test_results:
            scores = self.test_results["health_scores"]
            print(f"\nSYSTEM HEALTH SCORES:")
            print(f"  Addon Health: {scores['addon_health']:.1f}%")
            print(f"  Streaming Health: {scores['streaming_health']:.1f}%") 
            print(f"  Overall Health: {scores['system_health']:.1f}%")
        
        # Addon validation results
        if self.test_results["addon_validation"]:
            print(f"\nCORE ADDON STATUS:")
            for addon in self.test_results["addon_validation"]:
                status = "✓" if addon["present"] and addon["enabled"] and addon["working"] else "✗"
                print(f"  {status} {addon['addon_id']} v{addon['version']}")
        
        # Streaming test results
        if self.test_results["streaming_tests"]:
            print(f"\nSTREAMING ADDON TESTS:")
            for test in self.test_results["streaming_tests"]:
                status = "✓" if test["launch_success"] else "✗"
                time_info = f" ({test['response_time']}s)" if test["response_time"] else ""
                print(f"  {status} {test['addon_name']}{time_info}")
        
        # Recommendations
        if self.test_results["recommendations"]:
            print(f"\nRECOMMENDATIONS:")
            for rec in self.test_results["recommendations"]:
                print(f"  {rec['priority']}: {rec['issue']}")
                print(f"    → {rec['action']}")
        
        # Final assessment
        if "health_scores" in self.test_results:
            health = self.test_results["health_scores"]["system_health"]
            if health >= 90:
                status = "🟢 EXCELLENT - Production Ready"
            elif health >= 80:
                status = "🟡 GOOD - Minor Issues"
            elif health >= 60:
                status = "🟠 FAIR - Needs Attention"
            else:
                status = "🔴 POOR - Requires Immediate Fix"
            
            print(f"\nFINAL ASSESSMENT: {status}")
        
        print("="*80)

    def run_comprehensive_assessment(self):
        """Run complete assessment of Pigeonhole Gold Version"""
        print("Starting comprehensive Kodi assessment...")
        print("Target: Fire TV Cube at 192.168.1.130:8080")
        print("="*60)
        
        # Test connection
        if not self.test_connection():
            print("Cannot proceed without HTTP API connection")
            return False
        
        # Gather system info
        self.get_system_info()
        
        # Validate addons
        self.validate_installed_addons()
        
        # Test skin
        self.test_skin_activation()
        
        # Test streaming functionality
        self.test_streaming_addons()
        
        # Get performance metrics
        self.get_performance_metrics()
        
        # Configure optimizations
        self.configure_advanced_settings()
        
        # Generate assessment
        self.generate_comprehensive_report()
        
        # Save and display results
        report_file = self.save_assessment_report()
        self.print_assessment_summary()
        
        return True

def main():
    """Main execution function"""
    controller = KodiHTTPController()
    
    if controller.run_comprehensive_assessment():
        print("\nComprehensive assessment completed successfully!")
        print("Review the generated report for detailed analysis and recommendations.")
    else:
        print("\nAssessment failed. Check connection and try again.")

if __name__ == "__main__":
    main()