#!/usr/bin/env python3
"""
Simple Kodi v22 Checker
"""

import requests
import json
import subprocess
import os

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

def check_version():
    """Check current Kodi version"""
    print("Checking Kodi version...")
    
    version = kodi_rpc("Application.GetProperties", {"properties": ["version"]})
    if version:
        ver = version["result"]["version"]
        major = ver['major']
        minor = ver['minor']
        print(f"Current version: {major}.{minor}")
        return major, minor
    return None, None

def main():
    """Main function to check if upgrade to v22 is needed"""
    print("Kodi v22 Upgrade Checker")
    print("=" * 30)
    
    # Test connection
    result = kodi_rpc("JSONRPC.Ping")
    if result and result.get("result") == "pong":
        print("✓ Connected to Kodi device")
    else:
        print("✗ Failed to connect to Kodi")
        return
    
    # Check version
    major, minor = check_version()
    
    if major is not None:
        if major >= 22:
            print("Kodi is already v22 or newer")
        else:
            print("Kodi version is older than v22")
            print("To upgrade to v22:")
            print("1. Download Kodi v22 APK for ARM64")
            print("2. Install via ADB: adb install kodi-22.X.X-arm64.apk")
            print("3. Or install v22 repositories and update addons")

if __name__ == "__main__":
    main()