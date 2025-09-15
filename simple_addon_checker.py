#!/usr/bin/env python3
"""
Simple Addon Checker for Kodi
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
    """Main function to check installed addons"""
    print("Connecting to Kodi device...")
    
    # Test connection
    result = kodi_rpc("JSONRPC.Ping")
    if result and result.get("result") == "pong":
        print("✓ Connected successfully")
    else:
        print("✗ Failed to connect")
        return
    
    # Get all addons
    print("\nInstalled Addons:")
    print("-" * 50)
    
    addons = kodi_rpc("Addons.GetAddons")
    if addons and "result" in addons:
        for addon in addons["result"]["addons"]:
            print(f"{addon['addonid']}")
    
    # Get only video addons
    print("\n\nVideo Addons:")
    print("-" * 50)
    
    video_addons = kodi_rpc("Addons.GetAddons", {"type": "xbmc.python.pluginsource"})
    if video_addons and "result" in video_addons:
        for addon in video_addons["result"]["addons"]:
            print(f"{addon['addonid']}")

if __name__ == "__main__":
    main()