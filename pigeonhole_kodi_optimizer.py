#!/usr/bin/env python3
"""
Comprehensive Kodi Optimization Script for Fire TV Cube - Pigeonhole Entertainment Systems
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

def optimize_video_settings():
    """Optimize video settings for Fire TV Cube"""
    print("Optimizing video settings...")
    
    # Enable hardware acceleration
    settings = [
        {"setting": "videoplayer.usemediacodec", "value": True},
        {"setting": "videoplayer.usemediacodecsurface", "value": True},
        {"setting": "videoplayer.usedxva2", "value": True},
        {"setting": "videoplayer.rendermethod", "value": 0},  # Auto
    ]
    
    for setting in settings:
        try:
            kodi_rpc("Settings.SetSettingValue", setting)
            print(f"Set {setting['setting']} to {setting['value']}")
        except Exception as e:
            print(f"Failed to set {setting['setting']}: {e}")

def optimize_network_settings():
    """Optimize network settings for streaming"""
    print("Optimizing network settings...")
    
    # Network optimization settings
    settings = [
        {"setting": "network.disableipv6", "value": True},
        {"setting": "network.curlretries", "value": 2},
        {"setting": "network.httpmaxreadrate", "value": 4096},
    ]
    
    for setting in settings:
        try:
            kodi_rpc("Settings.SetSettingValue", setting)
            print(f"Set {setting['setting']} to {setting['value']}")
        except Exception as e:
            print(f"Failed to set {setting['setting']}: {e}")

def optimize_audio_settings():
    """Optimize audio settings"""
    print("Optimizing audio settings...")
    
    # Audio optimization settings
    settings = [
        {"setting": "audiooutput.dontnormalizelevels", "value": True},
        {"setting": "audiooutput.guisoundmode", "value": 1},  # Only when playback stops
    ]
    
    for setting in settings:
        try:
            kodi_rpc("Settings.SetSettingValue", setting)
            print(f"Set {setting['setting']} to {setting['value']}")
        except Exception as e:
            print(f"Failed to set {setting['setting']}: {e}")

def disable_unnecessary_services():
    """Disable unnecessary services to free up resources"""
    print("Disabling unnecessary services...")
    
    # Disable resource-heavy services
    settings = [
        {"setting": "services.airplay", "value": False},
        {"setting": "services.upnp", "value": False},
        {"setting": "services.plex", "value": False},
        {"setting": "services.zeroconf", "value": False},
    ]
    
    for setting in settings:
        try:
            kodi_rpc("Settings.SetSettingValue", setting)
            print(f"Disabled {setting['setting']}")
        except Exception as e:
            print(f"Failed to disable {setting['setting']}: {e}")

def optimize_skin_settings():
    """Optimize skin settings for performance"""
    print("Optimizing skin settings...")
    
    # Check current skin
    try:
        result = kodi_rpc("Settings.GetSettingValue", {"setting": "lookandfeel.skin"})
        current_skin = result.get("result", {}).get("value", "")
        print(f"Current skin: {current_skin}")
        
        # For Arctic Zephyr Mod, disable some animations
        if "arctic" in current_skin.lower():
            print("Arctic Zephyr detected - applying optimizations")
            # These would be skin-specific settings
    except Exception as e:
        print(f"Error checking skin: {e}")

def clean_addon_cache():
    """Clean addon cache and temporary files"""
    print("Cleaning addon cache...")
    
    try:
        # This would normally trigger cache cleaning
        # For now, we'll just log what would be done
        print("Would execute: Clear cache for all addons")
        print("Would execute: Clear temporary files")
        print("Would execute: Clear thumbnails cache")
    except Exception as e:
        print(f"Error cleaning cache: {e}")

def update_addon_repositories():
    """Update addon repositories"""
    print("Updating addon repositories...")
    
    try:
        # Trigger repository updates
        kodi_rpc("Addons.ExecuteAddon", {"addonid": "repository.xbmc.org"})
        print("Triggered official repository update")
        time.sleep(2)
        
        # Check for any Pigeonhole repositories
        addons = kodi_rpc("Addons.GetAddons", {"type": "xbmc.addon.repository"})
        if addons and "result" in addons:
            for addon in addons["result"].get("addons", []):
                addonid = addon["addonid"]
                if "pigeonhole" in addonid.lower() or "funstersplace" in addonid.lower():
                    kodi_rpc("Addons.ExecuteAddon", {"addonid": addonid})
                    print(f"Triggered update for {addonid}")
    except Exception as e:
        print(f"Error updating repositories: {e}")

def main():
    """Main optimization function"""
    print("=== Pigeonhole Entertainment Systems - Kodi Fire TV Cube Optimizer ===")
    print(f"Target device: {KODI_IP}:{KODI_PORT}")
    
    # Check connection
    try:
        result = kodi_rpc("JSONRPC.Ping")
        if result and result.get("result") == "pong":
            print("Successfully connected to Kodi device")
        else:
            print("Failed to connect to Kodi device")
            return
    except Exception as e:
        print(f"Connection error: {e}")
        return
    
    # Perform optimizations
    optimize_video_settings()
    optimize_network_settings()
    optimize_audio_settings()
    disable_unnecessary_services()
    optimize_skin_settings()
    clean_addon_cache()
    update_addon_repositories()
    
    print("\n=== Optimization Complete ===")
    print("Recommendations:")
    print("1. Restart Kodi to apply all changes")
    print("2. Consider upgrading to Kodi v22 Alpha for latest features")
    print("3. Install WolfLauncher for enhanced Fire TV experience")
    print("4. Review addon performance and disable any unused plugins")

if __name__ == "__main__":
    main()