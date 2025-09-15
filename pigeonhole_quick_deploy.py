import requests
import json
import time
from requests.auth import HTTPBasicAuth

def send_kodi_command(method, params=None):
    """Send command to Kodi via HTTP API"""
    url = "http://192.168.1.130:8080/jsonrpc"
    auth = HTTPBasicAuth("kodi", "0000")
    headers = {"Content-Type": "application/json"}

    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params or {},
        "id": 1
    }

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return None

def check_addon_status(addon_id):
    """Check if addon is installed and enabled"""
    params = {"addonid": addon_id, "properties": ["name", "version", "enabled"]}
    result = send_kodi_command("Addons.GetAddonDetails", params)
    return result

def enable_addon(addon_id):
    """Enable an addon"""
    params = {"addonid": addon_id, "enabled": True}
    result = send_kodi_command("Addons.SetAddonEnabled", params)
    return result

def install_addon(addon_id):
    """Install addon from repository"""
    params = {"addonid": addon_id}
    result = send_kodi_command("Addons.Install", params)
    return result

def apply_cache_settings():
    """Apply optimized cache settings"""
    print("Applying cache settings...")

    settings = {
        "network.buffermode": 1,
        "network.cachemembuffersize": 209715200,
        "network.readbufferfactor": 4.0
    }

    for setting, value in settings.items():
        params = {"setting": setting, "value": value}
        result = send_kodi_command("Settings.SetSettingValue", params)
        print(f"Set {setting}: {result}")
        time.sleep(1)

def main():
    print("PIGEONHOLE QUICK DEPLOYMENT")
    print("=" * 40)

    # Test connection
    print("Testing connection...")
    sys_result = send_kodi_command("System.GetProperties", {"properties": ["version"]})
    if not sys_result or "error" in sys_result:
        print("ERROR: Cannot connect to Kodi")
        return

    print("Connection OK!")

    # Apply cache settings
    apply_cache_settings()

    # Check and enable core addons
    core_addons = [
        "script.module.resolveurl",
        "plugin.video.thecrew",
        "plugin.video.fen.lite",
        "script.pigeonhole.config"
    ]

    print("\nChecking addons...")
    for addon in core_addons:
        status = check_addon_status(addon)
        if status and "result" in status:
            print(f"{addon}: FOUND - Enabling...")
            enable_result = enable_addon(addon)
        else:
            print(f"{addon}: NOT FOUND - Attempting install...")
            install_result = install_addon(addon)
            time.sleep(2)
            enable_result = enable_addon(addon)

    print("\nDeployment complete!")
    print("Check Kodi addons menu to verify installation")

if __name__ == "__main__":
    main()