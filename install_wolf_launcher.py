#!/usr/bin/env python3
"""
WolfLauncher Installation Script for Pigeonhole Entertainment Systems
"""

import subprocess
import os
import sys
import time

# Configuration
KODI_IP = "192.168.1.107"
ADB_PATH = "M:\\platform-tools\\adb.exe"  # Adjust path as needed
WOLF_APK_PATH = "M:\\apps\\wolf-launcher.apk"  # Path where APK should be

def check_adb():
    """Check if ADB is available"""
    try:
        result = subprocess.run([ADB_PATH, "version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("ADB is available")
            return True
        else:
            print("ADB not found or not working properly")
            return False
    except Exception as e:
        print(f"Error checking ADB: {e}")
        return False

def connect_to_device():
    """Connect to the Fire TV device"""
    try:
        # Connect via ADB
        result = subprocess.run([ADB_PATH, "connect", KODI_IP], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"Connected to device {KODI_IP}")
            return True
        else:
            print(f"Failed to connect to device: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error connecting to device: {e}")
        return False

def check_wolf_installed():
    """Check if WolfLauncher is already installed"""
    try:
        result = subprocess.run([ADB_PATH, "-s", KODI_IP, "shell", "pm", "list", "packages", "|", "grep", "wolf"], 
                              capture_output=True, text=True, timeout=10)
        if "xyz.wolf.launcher" in result.stdout:
            print("WolfLauncher is already installed")
            return True
        else:
            print("WolfLauncher not found")
            return False
    except Exception as e:
        print(f"Error checking WolfLauncher installation: {e}")
        return False

def download_wolf_launcher():
    """Download WolfLauncher APK (placeholder)"""
    print("Checking for WolfLauncher APK...")
    
    # In a real implementation, this would download the APK
    # For now, we'll check if it exists locally
    if os.path.exists(WOLF_APK_PATH):
        print(f"WolfLauncher APK found at {WOLF_APK_PATH}")
        return True
    else:
        print("WolfLauncher APK not found. Please download it manually:")
        print("1. Visit the WolfLauncher GitHub repository")
        print("2. Download the latest APK")
        print(f"3. Save it as {WOLF_APK_PATH}")
        return False

def install_wolf_launcher():
    """Install WolfLauncher on the device"""
    try:
        print("Installing WolfLauncher...")
        
        # Install the APK
        result = subprocess.run([ADB_PATH, "-s", KODI_IP, "install", WOLF_APK_PATH], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("WolfLauncher installed successfully")
            return True
        else:
            print(f"Failed to install WolfLauncher: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error installing WolfLauncher: {e}")
        return False

def set_wolf_as_home():
    """Set WolfLauncher as the default home launcher"""
    try:
        print("Setting WolfLauncher as default home launcher...")
        
        # Set as default launcher
        result = subprocess.run([ADB_PATH, "-s", KODI_IP, "shell", "su", "-c", 
                               "pm set-home-activity xyz.wolf.launcher/.MainActivity"], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("WolfLauncher set as default home launcher")
            return True
        else:
            print(f"Failed to set WolfLauncher as default: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error setting WolfLauncher as default: {e}")
        return False

def configure_wolf_launcher():
    """Configure WolfLauncher settings"""
    try:
        print("Configuring WolfLauncher...")
        
        # This would push configuration files
        # For now, we'll just show what would be done
        print("Would push WolfLauncher configuration files")
        print("Would set up Pigeonhole Kodi integration")
        print("Would configure app shortcuts and preferences")
        
        return True
    except Exception as e:
        print(f"Error configuring WolfLauncher: {e}")
        return False

def main():
    """Main installation function"""
    print("=== WolfLauncher Installation for Pigeonhole Entertainment Systems ===")
    print(f"Target device: {KODI_IP}")
    
    # Check prerequisites
    if not check_adb():
        print("Please ensure ADB is installed and accessible")
        return
    
    if not connect_to_device():
        print("Failed to connect to device")
        return
    
    # Check if already installed
    if check_wolf_installed():
        print("WolfLauncher is already installed. Skipping installation.")
        return
    
    # Download APK if needed
    if not download_wolf_launcher():
        print("Please download WolfLauncher APK and try again")
        return
    
    # Install WolfLauncher
    if not install_wolf_launcher():
        print("Failed to install WolfLauncher")
        return
    
    # Set as default launcher
    if not set_wolf_as_home():
        print("Failed to set WolfLauncher as default launcher")
        return
    
    # Configure settings
    if not configure_wolf_launcher():
        print("Failed to configure WolfLauncher")
        return
    
    print("\n=== WolfLauncher Installation Complete ===")
    print("Next steps:")
    print("1. Restart the device")
    print("2. WolfLauncher should start as the default launcher")
    print("3. Configure WolfLauncher settings as needed")
    print("4. Set up Pigeonhole Kodi within WolfLauncher")

if __name__ == "__main__":
    main()