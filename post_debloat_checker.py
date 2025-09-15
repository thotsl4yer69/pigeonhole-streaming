#!/usr/bin/env python3
"""
FireCube Post-Debloat Checker
Checks what packages remain after debloating
"""

import subprocess

# Device IP
DEVICE_IP = "192.168.1.107"

def run_adb_command(command):
    """Run an ADB command and return the output"""
    try:
        full_command = f"M:\\platform-tools\\adb.exe -s {DEVICE_IP} {command}"
        result = subprocess.run(full_command, shell=True, capture_output=True, text=True, timeout=30)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)

def connect_device():
    """Connect to the FireCube device"""
    print("Connecting to FireCube device...")
    code, stdout, stderr = run_adb_command("connect")
    if code == 0:
        print("✓ Connected successfully")
        return True
    else:
        print(f"✗ Connection failed: {stderr}")
        return False

def list_installed_packages():
    """List all installed packages"""
    print("Getting list of installed packages...")
    code, stdout, stderr = run_adb_command("shell pm list packages")
    if code == 0:
        packages = [line.replace("package:", "").strip() for line in stdout.split("\n") if line.startswith("package:")]
        return packages
    else:
        print(f"Error getting package list: {stderr}")
        return []

def main():
    """Main function to check post-debloat status"""
    print("=== FireCube Post-Debloat Checker ===\n")
    
    # Connect to device
    if not connect_device():
        return
    
    # Get list of packages
    packages = list_installed_packages()
    
    if not packages:
        print("No packages found")
        return
    
    print(f"Total packages installed: {len(packages)}\n")
    
    # Separate Amazon and non-Amazon packages
    amazon_packages = [pkg for pkg in packages if "amazon" in pkg.lower()]
    kodi_packages = [pkg for pkg in packages if "kodi" in pkg.lower() or "xbmc" in pkg.lower()]
    android_packages = [pkg for pkg in packages if pkg.startswith("com.android.")]
    other_packages = [pkg for pkg in packages if pkg not in amazon_packages and pkg not in kodi_packages and pkg not in android_packages]
    
    print("=== Amazon Packages ({} remaining) ===".format(len(amazon_packages)))
    for pkg in sorted(amazon_packages):
        print(f"  {pkg}")
    
    print("\n=== Kodi Packages ({} found) ===".format(len(kodi_packages)))
    for pkg in sorted(kodi_packages):
        print(f"  {pkg}")
    
    print("\n=== Essential Android Packages ({} found) ===".format(len(android_packages)))
    for pkg in sorted(android_packages):
        print(f"  {pkg}")
    
    print("\n=== Other Packages ({} found) ===".format(len(other_packages)))
    for pkg in sorted(other_packages):
        print(f"  {pkg}")
    
    print("\n=== Summary ===")
    print(f"Amazon packages: {len(amazon_packages)}")
    print(f"Kodi packages: {len(kodi_packages)}")
    print(f"Android system packages: {len(android_packages)}")
    print(f"Other packages: {len(other_packages)}")
    print(f"Total: {len(packages)}")

if __name__ == "__main__":
    main()