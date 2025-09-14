#!/usr/bin/env python3
"""
Test Pigeonhole Streaming Functionality via HTTP API
"""

import requests
import json
import base64
import time

class StreamingTester:
    def __init__(self):
        self.fire_tv_ip = "192.168.1.130"
        self.http_port = 8080
        self.username = "kodi"
        self.password = "0000"
        
        # Create auth header
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_credentials}"
        }
        
        self.base_url = f"http://{self.fire_tv_ip}:{self.http_port}/jsonrpc"
        
        # Streaming addons to test
        self.streaming_addons = [
            {
                "id": "plugin.video.thecrew",
                "name": "The Crew",
                "description": "Movies and TV Shows"
            },
            {
                "id": "plugin.video.fen.lite", 
                "name": "FEN Lite",
                "description": "Pigeonhole Edition Streaming"
            },
            {
                "id": "plugin.video.madtitansports",
                "name": "Mad Titan Sports",
                "description": "Live Sports Streaming"
            },
            {
                "id": "script.pigeonhole.config",
                "name": "Pigeonhole Config",
                "description": "Configuration System"
            }
        ]

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
                return response.json()
            else:
                print(f"HTTP Error {response.status_code}: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}")
            return None

    def test_addon_launch(self, addon_info):
        """Test launching a specific addon"""
        addon_id = addon_info["id"]
        addon_name = addon_info["name"]
        
        print(f"Testing {addon_name} ({addon_id})...")
        
        test_result = {
            "addon_id": addon_id,
            "addon_name": addon_name,
            "launch_success": False,
            "response_time": None,
            "error": None,
            "ui_navigation": False
        }
        
        try:
            # Record start time
            start_time = time.time()
            
            # Try to launch addon
            launch_response = self.send_rpc_request("Addons.ExecuteAddon", {
                "addonid": addon_id,
                "wait": False
            })
            
            response_time = time.time() - start_time
            test_result["response_time"] = round(response_time, 2)
            
            if launch_response:
                if "result" in launch_response:
                    if launch_response["result"] == "OK":
                        print(f"  [OK] Launch successful ({response_time:.2f}s)")
                        test_result["launch_success"] = True
                        
                        # Wait a moment for UI to load
                        time.sleep(3)
                        
                        # Test if we can get current window info (indicates UI loaded)
                        window_response = self.send_rpc_request("GUI.GetInfoLabels", {
                            "labels": ["System.CurrentWindow"]
                        })
                        
                        if window_response and "result" in window_response:
                            current_window = window_response["result"].get("System.CurrentWindow", "")
                            print(f"  [OK] UI loaded - Current window: {current_window}")
                            test_result["ui_navigation"] = True
                        
                        # Navigate back to home
                        self.send_rpc_request("Input.Home")
                        
                    else:
                        print(f"  [ISSUE] Launch failed: {launch_response['result']}")
                        test_result["error"] = str(launch_response["result"])
                else:
                    # Check for error
                    if "error" in launch_response:
                        error_msg = launch_response["error"].get("message", "Unknown error")
                        print(f"  [ISSUE] Error: {error_msg}")
                        test_result["error"] = error_msg
                    else:
                        print(f"  [ISSUE] Unexpected response: {launch_response}")
                        test_result["error"] = "Unexpected response"
            else:
                print(f"  [FAIL] No response from Kodi")
                test_result["error"] = "No response"
                
        except Exception as e:
            print(f"  [FAIL] Exception: {e}")
            test_result["error"] = str(e)
        
        return test_result

    def test_gui_navigation(self):
        """Test basic GUI navigation"""
        print("Testing GUI navigation...")
        
        nav_tests = [
            {
                "action": "Input.Home",
                "description": "Navigate to Home"
            },
            {
                "action": "Input.Info", 
                "description": "Show info dialog"
            },
            {
                "action": "Input.Back",
                "description": "Go back"
            }
        ]
        
        nav_success = 0
        for test in nav_tests:
            response = self.send_rpc_request(test["action"])
            if response and "result" in response and response["result"] == "OK":
                print(f"  [OK] {test['description']}")
                nav_success += 1
                time.sleep(1)  # Brief pause between navigation actions
            else:
                print(f"  [ISSUE] {test['description']} failed")
        
        print(f"GUI navigation: {nav_success}/{len(nav_tests)} actions successful")
        return nav_success > 0

    def check_system_performance(self):
        """Check system performance during testing"""
        print("Checking system performance...")
        
        response = self.send_rpc_request("System.GetInfoLabels", {
            "labels": [
                "System.FreeMemory",
                "System.UsedMemory", 
                "System.CPUUsage",
                "System.KernelVersion",
                "Network.IPAddress"
            ]
        })
        
        if response and "result" in response:
            info = response["result"]
            print(f"  Free Memory: {info.get('System.FreeMemory', 'Unknown')}")
            print(f"  Used Memory: {info.get('System.UsedMemory', 'Unknown')}")
            print(f"  CPU Usage: {info.get('System.CPUUsage', 'Unknown')}")
            print(f"  Network: {info.get('Network.IPAddress', 'Unknown')}")
            return True
        else:
            print("  [ISSUE] Could not get performance metrics")
            return False

    def test_favorites_menu(self):
        """Test Pigeonhole favorites menu"""
        print("Testing Pigeonhole favorites menu...")
        
        # Try to activate favorites window
        response = self.send_rpc_request("GUI.ActivateWindow", {
            "window": "favourites"
        })
        
        if response and "result" in response and response["result"] == "OK":
            print("  [OK] Favorites window activated")
            time.sleep(2)
            
            # Get favorites list
            fav_response = self.send_rpc_request("Favourites.GetFavourites", {
                "properties": ["window", "path"]
            })
            
            if fav_response and "result" in fav_response:
                favs = fav_response["result"].get("favourites", [])
                print(f"  [OK] Found {len(favs)} favorites")
                
                # Look for Pigeonhole entries
                pigeonhole_favs = [f for f in favs if "pigeonhole" in f.get("title", "").lower()]
                print(f"  [INFO] Pigeonhole favorites: {len(pigeonhole_favs)}")
                
                return True
            else:
                print("  [ISSUE] Could not get favorites list")
                return False
        else:
            print("  [ISSUE] Could not activate favorites window")
            return False

    def run_streaming_tests(self):
        """Run comprehensive streaming functionality tests"""
        print("PIGEONHOLE STREAMING FUNCTIONALITY TEST")
        print("=" * 45)
        
        # Test connection first
        ping_response = self.send_rpc_request("JSONRPC.Ping")
        if not ping_response or ping_response.get("result") != "pong":
            print("[FAIL] Cannot connect to Kodi HTTP API")
            return False
        
        print("[OK] Connected to Kodi HTTP API")
        
        # Check system performance
        perf_ok = self.check_system_performance()
        
        # Test GUI navigation
        nav_ok = self.test_gui_navigation()
        
        # Test favorites menu
        fav_ok = self.test_favorites_menu()
        
        # Test each streaming addon
        addon_results = []
        successful_launches = 0
        
        print(f"\nTesting {len(self.streaming_addons)} streaming addons...")
        for addon_info in self.streaming_addons:
            result = self.test_addon_launch(addon_info)
            addon_results.append(result)
            
            if result["launch_success"]:
                successful_launches += 1
            
            # Brief pause between addon tests
            time.sleep(2)
        
        # Final assessment
        print(f"\nSTREAMING TEST RESULTS:")
        print(f"  System Performance: {'OK' if perf_ok else 'ISSUE'}")
        print(f"  GUI Navigation: {'OK' if nav_ok else 'ISSUE'}")
        print(f"  Favorites Menu: {'OK' if fav_ok else 'ISSUE'}")
        print(f"  Addon Launches: {successful_launches}/{len(self.streaming_addons)} successful")
        
        print(f"\nDetailed Addon Results:")
        for result in addon_results:
            status = "[OK]" if result["launch_success"] else "[ISSUE]"
            time_info = f" ({result['response_time']}s)" if result["response_time"] else ""
            error_info = f" - {result['error']}" if result["error"] else ""
            print(f"  {status} {result['addon_name']}{time_info}{error_info}")
        
        # Overall success criteria
        overall_success = (
            perf_ok and 
            nav_ok and 
            successful_launches >= len(self.streaming_addons) // 2  # At least half working
        )
        
        if overall_success:
            print(f"\n[SUCCESS] Streaming functionality test PASSED!")
            print("Pigeonhole Gold Version is ready for streaming!")
        else:
            print(f"\n[WARNING] Streaming functionality test completed with issues.")
            print("Some components may need attention.")
        
        return overall_success

def main():
    """Main execution function"""
    tester = StreamingTester()
    
    success = tester.run_streaming_tests()
    
    if success:
        print("\nStreaming functionality validation completed successfully!")
    else:
        print("\nStreaming functionality validation completed with issues.")
        print("Review the detailed results above.")

if __name__ == "__main__":
    main()