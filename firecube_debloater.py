#!/usr/bin/env python3
"""
FireCube Debloater Script
Removes Amazon bloatware and optimizes the system
"""

import subprocess
import time

# Device IP and port
DEVICE_IP = "192.168.1.107:5555"

# Amazon packages to remove/disable
AMAZON_BLOATWARE = [
    "com.amazon.alexamediaplayer.runtime.ftv",
    "com.amazon.spiderpork",
    "com.amazon.tv.turnstile",
    "com.amazon.ssmsys",
    "com.amazon.tigris",
    "com.amazon.tv.acr",
    "com.amazon.whisperplay.contracts",
    "com.amazon.device.rdmapplication",
    "com.amazon.venezia",
    "com.amazon.dcp.contracts.library",
    "com.amazon.ftv.xpicker",
    "com.amazon.hybridadidservice",
    "com.amazon.livedeviceservice",
    "com.amazon.vizzini",
    "com.amazon.tv.devicecontrolsettings",
    "com.amazon.connectivitycontroller",
    "com.amazon.bueller.photos",
    "com.ivona.orchestrator",
    "com.amazon.device.sync",
    "com.amazon.tv.sysappsinternal.resources",
    "com.amazon.shoptv.firetv.client",
    "com.amazon.dpcclient",
    "com.amazon.tv.parentalcontrols",
    "com.amazon.ftv.screensaver",
    "com.amazon.notification",
    "com.amazon.tv.ooberesource",
    "com.amazon.dp.logger",
    "com.amazon.ods.kindleconnect",
    "com.amazon.alexa.datastore.app",
    "com.amazon.alta.h2clientservice",
    "com.amazon.tv.intentsupport",
    "com.amazon.sharingservice.android.client.proxy",
    "com.amazon.android.marketplace",
    "com.amazon.android.devicemodelinfo.resources",
    "com.amazon.prism.android.service",
    "com.amazon.spotify.mediabrowserservice",
    "com.amazon.tifobserver",
    "com.amazon.dialservice",
    "com.amazon.avsyncslider",
    "com.amazon.client.metrics.api",
    "com.amazon.storage.manager",
    "com.amazon.ale",
    "com.amazon.cpl",
    "com.amazon.dcp",
    "com.amazon.imp",
    "com.amazon.ssm",
    "com.amazon.neodelegate",
    "com.amazon.tv.easyupgrade",
    "com.amazon.comms.knightmessaging",
    "com.amazon.fireinputdevices",
    "com.amazon.tv.settings.v2",
    "com.amazon.csm.htmlruntime",
    "com.amazon.tv.csapp",
    "com.amazon.diode",
    "com.amazon.logan",
    "com.amazon.tahoe",
    "com.amazon.tcomm",
    "com.amazon.ftvads.deeplinking",
    "com.amazon.tv.legalresources",
    "com.amazon.comms.starktachyon",
    "com.amazon.naatyam",
    "com.amazon.stillwatching.activity",
    "com.amazon.a4b.mcc",
    "com.amazon.sneakpeek",
    "com.amazon.tv.avrcpclient",
    "com.amazon.storm.lightning.tutorial",
    "com.amazon.identity.auth.device.authorization",
    "com.amazon.wirelessmetrics.service",
    "com.amazon.kindleautomatictimezone",
    "com.amazon.uxcontrollerservice",
    "com.fireos.arcus.proxy",
    "com.amazon.tv.fw.metrics",
    "com.amazon.whasettings",
    "com.amazon.tv.alexanotifications",
    "com.amazon.device.sale.service",
    "com.amazon.cardinal",
    "com.amazon.dummy.contacts",
    "com.amazon.accessoryconfigservice",
    "com.amazon.device.blepa",
    "com.amazon.tcomm.client",
    "com.amazon.tv.website_launcher",
    "com.amazon.tv.forcedotaupdater.v2",
    "com.amazon.client.metrics",
    "com.amazon.device.settings.sdk.internal.library",
    "com.amazon.tv.localgallery",
    "com.amazon.autopairservice",
    "com.amazon.minitv.android.app",
    "com.amazon.device.details",
    "com.amazon.imdb.tv.android.app",
    "com.amazon.tmm.tutorial",
    "com.amazon.wha.mediabrowserservice",
    "com.amazon.device.software.ota",
    "com.amazon.d3",
    "com.amazon.tv.developer.dataservice",
    "com.amazon.wifilocker",
    "com.amazon.avls.experience",
    "com.amazon.audiohome",
    "com.amazon.dummy.calendar",
    "com.amazon.dcp.contracts.framework.library",
    "com.amazon.whisperlink.core.android",
    "com.amazon.device.messaging.sdk.internal.library",
    "com.amazon.tv.devicecontrol",
    "com.amazon.systemnotices",
    "com.amazon.tv.ottssocompanionapp",
    "com.amazon.tv.oobe",
    "com.amazon.aiondec",
    "com.amznfuse.operatorredirection",
    "com.amazon.neopactservice",
    "com.amazon.sync.provider.ipc",
    "com.amazon.tv.legal.notices",
    "com.amazon.tv.settings.core",
    "com.amazon.firebat",
    "com.amazon.dummy.alarmclock",
    "com.amazon.kso.blackbird",
    "com.amazon.providers.contentsupport",
    "com.amazon.firetvledservice",
    "com.amazon.awvflingreceiver",
    "com.amazon.hearingaid",
    "com.amazon.device.crashmanager",
    "com.amazon.whisperjoin.middleware.np",
    "com.amazon.application.compatibility.enforcer",
    "com.amazon.whisperplay.service.install",
    "com.ivona.tts.oem",
    "com.amazon.tv.launcher",
    "com.amazon.uxnotification",
    "com.amazon.cast.sink",
    "com.amazon.tv.inputpreference.service",
    "com.amazon.shoptv.client",
    "com.amazon.device.software.ota.override",
    "com.amazon.franktvinput",
    "com.amazon.assetsync.service",
    "com.amazon.aria",
    "com.amazon.avod",
    "com.amazon.whad",
    "com.amazon.tcomm.jackson",
    "com.fireos.sdk.ftve.addp",
    "com.amazon.communication.discovery",
    "com.amazon.alexa.externalmediaplayer.fireos",
    "com.amazon.privacypassservice",
    "com.amazon.ssdpservice",
    "com.amazon.gamehub",
    "com.amazon.device.settings",
    "com.amazon.cloud9",
    "com.amazon.tv.livetv",
    "com.amazon.device.sync.sdk.internal",
    "com.amazon.connectivitydiag",
    "com.amazon.device.lowstoragemanager",
    "com.amazon.perfcollection",
    "com.amazon.providers.tv",
    "com.amazon.webview.chromium",
    "com.amazon.bueller.music",
    "com.amazon.hedwig",
    "com.amazon.fireos.cirruscloud",
    "com.amazon.vizzini.ftvcds",
    "com.amazon.dummy.music",
    "com.amazon.device.bluetoothpa",
    "com.amazon.application.compatibility.enforcer.sdk.library"
]

# Packages to keep (essential system packages)
ESSENTIAL_PACKAGES = [
    "android",
    "com.android.settings",
    "com.android.systemui",
    "com.android.bluetooth",
    "com.android.providers.contacts",
    "com.android.providers.settings",
    "com.android.providers.media",
    "com.android.providers.downloads",
    "com.android.providers.calendar",
    "com.android.documentsui",
    "com.android.externalstorage",
    "com.android.htmlviewer",
    "com.android.certinstaller",
    "com.android.packageinstaller",
    "com.android.shell",
    "com.android.keychain",
    "com.android.location.fused",
    "org.xbmc.kodi"
]

def run_adb_command(command):
    """Run an ADB command and return the output"""
    try:
        full_command = f"M:\\\\platform-tools\\\\adb.exe {command}"
        result = subprocess.run(full_command, shell=True, capture_output=True, text=True, timeout=30)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)

def connect_device():
    """Connect to the FireCube device"""
    print("Connecting to FireCube device...")
    code, stdout, stderr = run_adb_command(f"connect {DEVICE_IP}")
    if code == 0:
        print("[OK] Connected successfully")
        return True
    else:
        print(f"[ERROR] Connection failed: {stderr}")
        return False

def disable_package(package):
    """Disable a package"""
    code, stdout, stderr = run_adb_command(f"-s {DEVICE_IP} shell pm disable-user --user 0 {package}")
    if code == 0:
        print(f"[OK] Disabled {package}")
        return True
    else:
        print(f"[ERROR] Failed to disable {package}: {stderr}")
        return False

def uninstall_package(package):
    """Uninstall a package"""
    code, stdout, stderr = run_adb_command(f"-s {DEVICE_IP} shell pm uninstall --user 0 {package}")
    if code == 0:
        print(f"[OK] Uninstalled {package}")
        return True
    else:
        print(f"[ERROR] Failed to uninstall {package}: {stderr}")
        return False

def block_internet_access(package):
    """Block internet access for a package"""
    code, stdout, stderr = run_adb_command(f"-s {DEVICE_IP} shell pm restrict-background {package}")
    if code == 0:
        print(f"[OK] Restricted background data for {package}")
        return True
    else:
        print(f"[ERROR] Failed to restrict background data for {package}: {stderr}")
        return False

def main():
    """Main debloating function"""
    print("=== FireCube Debloater ===")
    print("This script will remove Amazon bloatware and optimize your device")
    print("WARNING: This will remove many Amazon services. Proceed with caution!")
    print()
    
    # Connect to device
    if not connect_device():
        return
    
    # Confirm with user
    confirm = input("Do you want to proceed with debloating? (yes/no): ")
    if confirm.lower() not in ["yes", "y"]:
        print("Debloating cancelled")
        return
    
    print("\\nStarting debloating process...")
    
    # Disable Amazon bloatware
    print("\\n1. Disabling Amazon bloatware...")
    disabled_count = 0
    for package in AMAZON_BLOATWARE:
        if disable_package(package):
            disabled_count += 1
        time.sleep(0.1)  # Small delay to avoid overwhelming the device
    
    # Block internet access for remaining Amazon packages
    print("\\n2. Blocking internet access for Amazon services...")
    blocked_count = 0
    
    # Get list of all installed packages
    code, stdout, stderr = run_adb_command(f"-s {DEVICE_IP} shell pm list packages")
    if code == 0:
        all_packages = [line.replace("package:", "").strip() for line in stdout.split("\\n") if line.startswith("package:")]
        
        # Filter for Amazon packages that weren't in our main list
        amazon_packages = [pkg for pkg in all_packages if "amazon" in pkg.lower() and pkg not in AMAZON_BLOATWARE and pkg not in ESSENTIAL_PACKAGES]
        
        for package in amazon_packages:
            if block_internet_access(package):
                blocked_count += 1
            time.sleep(0.1)
    
    # Optimize system settings
    print("\\n3. Optimizing system settings...")
    
    # Disable OTA updates
    run_adb_command(f"-s {DEVICE_IP} shell pm disable-user --user 0 com.amazon.device.software.ota")
    
    # Disable metrics collection
    run_adb_command(f"-s {DEVICE_IP} shell pm disable-user --user 0 com.amazon.client.metrics")
    run_adb_command(f"-s {DEVICE_IP} shell pm disable-user --user 0 com.amazon.client.metrics.api")
    
    # Disable advertising ID
    run_adb_command(f"-s {DEVICE_IP} shell pm disable-user --user 0 com.amazon.advertisingidsettings")
    
    # Disable telemetry
    run_adb_command(f"-s {DEVICE_IP} shell pm disable-user --user 0 com.amazon.tv.fw.metrics")
    
    # Disable sync services
    run_adb_command(f"-s {DEVICE_IP} shell pm disable-user --user 0 com.amazon.device.sync")
    run_adb_command(f"-s {DEVICE_IP} shell pm disable-user --user 0 com.amazon.sync.service")
    
    print("\\n=== Debloating Complete ===")
    print(f"Disabled packages: {disabled_count}")
    print(f"Blocked internet access for packages: {blocked_count}")
    print("\\nRecommendations:")
    print("1. Restart your FireCube device")
    print("2. Check that Kodi is still working properly")
    print("3. Install WolfLauncher for a better interface")
    print("4. Consider installing a VPN for privacy")

if __name__ == "__main__":
    main()