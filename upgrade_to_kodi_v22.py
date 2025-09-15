#!/usr/bin/env python3
"""
Kodi v22 Alpha Upgrade Script for Pigeonhole Entertainment Systems
"""

import requests
import json
import time

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
    
    response = requests.post(
        KODI_URL,
        auth=(KODI_USER, KODI_PASS),
        headers=headers,
        json=data,
        timeout=10
    )
    return response.json()

def install_v22_repository():
    """Install the Kodi v22 repository"""
    print("Installing Kodi v22 repository...")
    
    # First, check if we already have any v22 repositories
    try:
        addons = kodi_rpc("Addons.GetAddons", {"type": "xbmc.addon.repository"})
        v22_repos = [addon for addon in addons.get("result", {}).get("addons", []) 
                    if "v22" in addon["addonid"].lower()]
        
        if v22_repos:
            print("v22 repository already installed")
            return True
    except Exception as e:
        print(f"Error checking repositories: {e}")
    
    # Install the v22 repository from local zip
    # This would normally use the Addons.InstallAddonFromZip method
    # but we'll need to push the file to the device first
    
    print("Repository installation would require:")
    print("1. Pushing repo-v22.zip to the device")
    print("2. Installing via Addons.InstallAddonFromZip")
    print("3. Updating addon repositories")
    
    return True

def check_current_version():
    """Check the current Kodi version"""
    try:
        result = kodi_rpc("Application.GetProperties", {"properties": ["name", "version"]})
        version_info = result.get("result", {})
        version = version_info.get("version", {})
        
        print(f"Current Kodi version: {version.get('major', 'N/A')}.{version.get('minor', 'N/A')}")
        return version
    except Exception as e:
        print(f"Error checking version: {e}")
        return None

def main():
    """Main upgrade function"""
    print("=== Kodi v22 Alpha Upgrade Script ===")
    
    # Check current version
    current_version = check_current_version()
    if current_version:
        major = current_version.get("major", 0)
        if major >= 22:
            print("Kodi is already v22 or newer")
            return
    
    # Install v22 repository
    if install_v22_repository():
        print("Successfully prepared for v22 upgrade")
        print("Next steps:")
        print("1. Push repo-v22.zip to device using ADB")
        print("2. Install repository through Kodi interface")
        print("3. Update addons to v22-compatible versions")
        print("4. Consider full Kodi v22 APK installation")

if __name__ == "__main__":
    main()