#!/usr/bin/env python3
"""
Simple Kodi HTTP API Test - Windows Compatible
"""

import requests
import json
import base64
from datetime import datetime

def test_kodi_connection():
    """Test basic Kodi HTTP API connection"""
    
    # Connection details
    fire_tv_ip = "192.168.1.130"
    http_port = 8080
    username = "kodi"
    password = "0000"
    
    # Create auth header
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {encoded_credentials}"
    }
    
    base_url = f"http://{fire_tv_ip}:{http_port}/jsonrpc"
    
    print("KODI HTTP API CONNECTION TEST")
    print("=" * 40)
    print(f"Target: {fire_tv_ip}:{http_port}")
    print(f"Auth: {username}/***")
    print()
    
    try:
        # Test ping
        print("Testing connection...")
        ping_payload = {
            "jsonrpc": "2.0",
            "method": "JSONRPC.Ping",
            "id": 1
        }
        
        response = requests.post(base_url, json=ping_payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("result") == "pong":
                print("[OK] Connection successful - Kodi responding")
                
                # Get system info
                print("\nGetting system information...")
                system_payload = {
                    "jsonrpc": "2.0",
                    "method": "System.GetInfoLabels",
                    "params": {
                        "labels": [
                            "System.BuildVersion",
                            "System.FreeMemory",
                            "System.CPUUsage",
                            "System.Uptime"
                        ]
                    },
                    "id": 2
                }
                
                sys_response = requests.post(base_url, json=system_payload, headers=headers, timeout=10)
                if sys_response.status_code == 200:
                    sys_result = sys_response.json()
                    if "result" in sys_result:
                        info = sys_result["result"]
                        print(f"[OK] Kodi Version: {info.get('System.BuildVersion', 'Unknown')}")
                        print(f"[OK] Free Memory: {info.get('System.FreeMemory', 'Unknown')}")
                        print(f"[OK] CPU Usage: {info.get('System.CPUUsage', 'Unknown')}")
                        print(f"[OK] Uptime: {info.get('System.Uptime', 'Unknown')}")
                
                # Get addon list
                print("\nGetting addon information...")
                addon_payload = {
                    "jsonrpc": "2.0",
                    "method": "Addons.GetAddons",
                    "params": {
                        "properties": ["name", "version", "enabled", "broken"]
                    },
                    "id": 3
                }
                
                addon_response = requests.post(base_url, json=addon_payload, headers=headers, timeout=10)
                if addon_response.status_code == 200:
                    addon_result = addon_response.json()
                    if "result" in addon_result and "addons" in addon_result["result"]:
                        addons = addon_result["result"]["addons"]
                        print(f"[OK] Found {len(addons)} installed addons")
                        
                        # Check for our core addons
                        core_addons = [
                            "skin.arctic.zephyr.pigeonhole",
                            "script.module.resolveurl",
                            "plugin.video.thecrew",
                            "plugin.video.fen.lite",
                            "script.pigeonhole.config"
                        ]
                        
                        print("\nCore Pigeonhole addon status:")
                        found_addons = {}
                        for addon in addons:
                            found_addons[addon["addonid"]] = addon
                        
                        for core_addon in core_addons:
                            if core_addon in found_addons:
                                addon_info = found_addons[core_addon]
                                status = "[OK]" if addon_info["enabled"] and not addon_info["broken"] else "[ISSUE]"
                                print(f"  {status} {addon_info['name']} v{addon_info['version']}")
                            else:
                                print(f"  [MISSING] {core_addon}")
                
                # Test simple addon execution
                print("\nTesting addon execution...")
                exec_payload = {
                    "jsonrpc": "2.0", 
                    "method": "Addons.ExecuteAddon",
                    "params": {
                        "addonid": "script.pigeonhole.config",
                        "wait": False
                    },
                    "id": 4
                }
                
                exec_response = requests.post(base_url, json=exec_payload, headers=headers, timeout=10)
                if exec_response.status_code == 200:
                    exec_result = exec_response.json()
                    if "result" in exec_result:
                        print(f"[OK] Addon execution test: {exec_result['result']}")
                    else:
                        print(f"[ISSUE] Addon execution failed: {exec_result}")
                
                print("\nHTTP API test completed successfully!")
                return True
                
            else:
                print(f"[FAIL] Unexpected response: {result}")
                return False
        else:
            print(f"[FAIL] HTTP Error {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"[FAIL] Connection error: {e}")
        return False
    except Exception as e:
        print(f"[FAIL] Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_kodi_connection()
    print(f"\nTest result: {'PASSED' if success else 'FAILED'}")