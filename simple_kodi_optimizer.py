#!/usr/bin/env python3
"""
Simple Kodi Optimizer for FireCube Device
"""

import requests
import json

# Device configuration
KODI_IP = "192.168.1.107"
KODI_PORT = "8080"
KODI_USER = "kodi"
KODI_PASS = "0000"

# Kodi JSON-RPC endpoint
KODI_URL = f"http://{KODI_IP}:{KODI_PORT}/jsonrpc"

def kodi_rpc(method, params=None):
    """Send a JSON-RPC request to Kodi"""
    headers = {'Content-Type': 'application/json'}
    data = {
        "jsonrpc": "2.0",
        "method": method,
        "id": 1
    }
    if params:
        data["params"] = params
    
    try:
        response = requests.post(
            KODI_URL,
            auth=(KODI_USER, KODI_PASS),
            headers=headers,
            json=data,
            timeout=10
        )
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    """Main function to optimize Kodi settings"""
    print("Connecting to Kodi device...")
    
    # Test connection
    result = kodi_rpc("JSONRPC.Ping")
    if result and result.get("result") == "pong":
        print("✓ Connected successfully")
    else:
        print("✗ Failed to connect")
        return
    
    # Get current version
    version = kodi_rpc("Application.GetProperties", {"properties": ["version"]})
    if version:
        ver = version["result"]["version"]
        print(f"Current version: {ver['major']}.{ver['minor']}")
    
    # Optimize video settings for FireCube
    print("Optimizing video settings...")
    kodi_rpc("Settings.SetSettingValue", {"setting": "videoplayer.usemediacodec", "value": True})
    kodi_rpc("Settings.SetSettingValue", {"setting": "videoplayer.usemediacodecsurface", "value": True})
    kodi_rpc("Settings.SetSettingValue", {"setting": "videoplayer.rendermethod", "value": 0})
    
    # Optimize network settings
    print("Optimizing network settings...")
    kodi_rpc("Settings.SetSettingValue", {"setting": "network.disableipv6", "value": True})
    kodi_rpc("Settings.SetSettingValue", {"setting": "network.curlretries", "value": 2})
    
    # Disable unnecessary services
    print("Disabling unnecessary services...")
    kodi_rpc("Settings.SetSettingValue", {"setting": "services.airplay", "value": False})
    kodi_rpc("Settings.SetSettingValue", {"setting": "services.upnp", "value": False})
    
    print("Optimization complete! Please restart Kodi to apply all changes.")

if __name__ == "__main__":
    main()