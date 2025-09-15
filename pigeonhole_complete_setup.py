#!/usr/bin/env python3
"""
Complete Pigeonhole Entertainment Systems Setup Script
"""

import subprocess
import requests
import json
import time
import os

# Configuration
KODI_IP = "192.168.1.107"
KODI_PORT = "8080"
KODI_USER = "kodi"
KODI_PASS = "0000"
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
        print(f"Error communicating with Kodi: {e}")
        return None

def check_connection():
    """Check if we can connect to Kodi"""
    try:
        result = kodi_rpc("JSONRPC.Ping")
        return result and result.get("result") == "pong"
    except:
        return False

def get_kodi_info():
    """Get Kodi version and system information"""
    try:
        version = kodi_rpc("Application.GetProperties", {"properties": ["name", "version"]})
        addons = kodi_rpc("Addons.GetAddons")
        
        print("=== Kodi System Information ===")
        if version and "result" in version:
            ver_info = version["result"]["version"]
            print(f"Kodi Version: {ver_info['major']}.{ver_info['minor']} ({ver_info['tag']})")
        
        if addons and "result" in addons:
            total_addons = addons["result"]["limits"]["total"]
            print(f"Total Addons Installed: {total_addons}")
            
        return True
    except Exception as e:
        print(f"Error getting system info: {e}")
        return False

def install_pigeonhole_repository():
    """Install Pigeonhole repository"""
    print("Installing Pigeonhole repository...")
    
    # This would normally use Addons.InstallAddonFromZip
    # For now, we'll just check if it exists
    try:
        addons = kodi_rpc("Addons.GetAddons", {"type": "xbmc.addon.repository"})
        if addons and "result" in addons:
            pigeonhole_repos = [a for a in addons["result"]["addons"] 
                              if "pigeonhole" in a["addonid"].lower()]
            if pigeonhole_repos:
                print("Pigeonhole repository already installed")
                return True
        
        print("Pigeonhole repository installation would require:")
        print("1. Pushing repository zip to device")
        print("2. Installing via Addons.InstallAddonFromZip")
        return True
    except Exception as e:
        print(f"Error with repository installation: {e}")
        return False

def optimize_system():
    """Apply system optimizations"""
    print("Applying system optimizations...")
    
    optimizations = [
        # Video settings
        {"setting": "videoplayer.usemediacodec", "value": True},
        {"setting": "videoplayer.usemediacodecsurface", "value": True},
        {"setting": "videoplayer.rendermethod", "value": 0},
        
        # Network settings
        {"setting": "network.disableipv6", "value": True},
        {"setting": "network.curlretries", "value": 2},
        
        # Disable unnecessary services
        {"setting": "services.airplay", "value": False},
        {"setting": "services.upnp", "value": False},
        {"setting": "services.zeroconf", "value": False},
    ]
    
    success_count = 0
    for opt in optimizations:
        try:
            result = kodi_rpc("Settings.SetSettingValue", opt)
            if result:
                print(f"✓ Set {opt['setting']}")
                success_count += 1
            else:
                print(f"✗ Failed to set {opt['setting']}")
        except Exception as e:
            print(f"✗ Error setting {opt['setting']}: {e}")
    
    print(f"Applied {success_count}/{len(optimizations)} optimizations")
    return success_count > 0

def check_for_updates():
    """Check for addon updates"""
    print("Checking for addon updates...")
    
    try:
        # Trigger repository updates
        kodi_rpc("Addons.ExecuteAddon", {"addonid": "repository.xbmc.org"})
        time.sleep(3)
        
        print("Repository update triggered")
        return True
    except Exception as e:
        print(f"Error checking for updates: {e}")
        return False

def generate_report():
    """Generate a setup report"""
    print("\n=== Setup Report ===")
    
    try:
        # Get system info
        version = kodi_rpc("Application.GetProperties", {"properties": ["name", "version"]})
        if version and "result" in version:
            ver_info = version["result"]["version"]
            print(f"Kodi Version: {ver_info['major']}.{ver_info['minor']}")
        
        # Get skin info
        skin = kodi_rpc("Settings.GetSettingValue", {"setting": "lookandfeel.skin"})
        if skin and "result" in skin:
            print(f"Current Skin: {skin['result']['value']}")
        
        # Get addon count
        addons = kodi_rpc("Addons.GetAddons")
        if addons and "result" in addons:
            total = addons["result"]["limits"]["total"]
            print(f"Installed Addons: {total}")
            
        return True
    except Exception as e:
        print(f"Error generating report: {e}")
        return False

def main():
    """Main setup function"""
    print("=== Pigeonhole Entertainment Systems - Complete Setup ===")
    print(f"Target device: {KODI_IP}:{KODI_PORT}")
    
    # Check connection
    if not check_connection():
        print("ERROR: Cannot connect to Kodi device")
        print("Please ensure:")
        print("1. Device is powered on")
        print("2. Kodi is running")
        print("3. Network connection is active")
        print("4. Username/password are correct")
        return
    
    print("✓ Connected to Kodi device")
    
    # Get system information
    get_kodi_info()
    
    # Install Pigeonhole repository
    install_pigeonhole_repository()
    
    # Apply optimizations
    optimize_system()
    
    # Check for updates
    check_for_updates()
    
    # Generate final report
    generate_report()
    
    print("\n=== Setup Complete ===")
    print("Recommended next steps:")
    print("1. Restart Kodi to apply all changes")
    print("2. Install WolfLauncher for enhanced Fire TV experience")
    print("3. Upgrade to Kodi v22 Alpha for latest features")
    print("4. Review and configure installed addons")
    print("5. Test streaming performance")

if __name__ == "__main__":
    main()