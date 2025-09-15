import requests
import json
import time
from requests.auth import HTTPBasicAuth

def send_command(method, params=None):
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
        response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth, timeout=15)
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return None

def install_from_repository(addon_id):
    """Try to install addon from available repositories"""
    print(f"Installing {addon_id}...")

    # Try to install from official repository
    params = {"addonid": addon_id}
    result = send_command("Addons.Install", params)

    if result and "result" in result:
        print(f"  {addon_id}: Installation started")
        return True
    else:
        print(f"  {addon_id}: Installation failed - {result}")
        return False

def refresh_repositories():
    """Refresh addon repositories"""
    print("Refreshing repositories...")
    result = send_command("Addons.GetAddons", {"type": "kodi.addon.repository"})

    if result and "result" in result:
        repos = result["result"].get("addons", [])
        print(f"Found {len(repos)} repositories")

        # Try to update repositories
        for repo in repos:
            repo_id = repo["addonid"]
            update_result = send_command("Addons.Install", {"addonid": repo_id})
            print(f"  Updated {repo_id}: {'OK' if update_result else 'FAILED'}")
            time.sleep(2)

    time.sleep(5)  # Wait for repo refresh

def main():
    print("CORE ADDON INSTALLER")
    print("=" * 40)

    # First, refresh repositories
    refresh_repositories()

    # Core addons to install
    core_addons = [
        "script.module.resolveurl",
        "plugin.video.youtube",  # Test addon
        "plugin.video.vimeo",    # Another test addon
    ]

    print("\nInstalling core addons...")
    for addon in core_addons:
        success = install_from_repository(addon)
        time.sleep(3)  # Wait between installations

    # Check what got installed
    print("\nChecking installation status...")
    time.sleep(5)  # Wait for installations to complete

    for addon in core_addons:
        details = send_command("Addons.GetAddonDetails", {
            "addonid": addon,
            "properties": ["enabled", "version", "installed"]
        })

        if details and "result" in details:
            addon_data = details["result"]["addon"]
            status = f"v{addon_data.get('version', '?')} - {'Enabled' if addon_data.get('enabled') else 'Disabled'}"
            print(f"  {addon}: {status}")
        else:
            print(f"  {addon}: NOT FOUND")

    print("\nInstallation complete!")
    print("NOTE: Some addons may need to be installed manually from Kodi's addon browser")

if __name__ == "__main__":
    main()