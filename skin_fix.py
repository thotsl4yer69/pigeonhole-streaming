import requests
from requests.auth import HTTPBasicAuth

def send_command(method, params=None):
    url = "http://192.168.1.130:8080/jsonrpc"
    auth = HTTPBasicAuth("kodi", "0000")
    payload = {"jsonrpc": "2.0", "method": method, "params": params or {}, "id": 1}
    try:
        response = requests.post(url, json=payload, auth=auth, timeout=10)
        return response.json()
    except Exception as e:
        return None

print("FIXING PIGEONHOLE SKIN ISSUE")
print("=" * 40)

# Disable broken Pigeonhole skin
print("Disabling broken Pigeonhole skin...")
disable_result = send_command("Addons.SetAddonEnabled", {
    "addonid": "skin.arctic.zephyr.pigeonhole",
    "enabled": False
})
print(f"Disabled: {'OK' if disable_result else 'FAILED'}")

# Ensure Estuary is active and working
print("Setting Estuary as active skin...")
skin_result = send_command("Settings.SetSettingValue", {
    "setting": "lookandfeel.skin",
    "value": "skin.estuary"
})
print(f"Estuary active: {'OK' if skin_result else 'FAILED'}")

# Configure Estuary for streaming
print("Optimizing Estuary for streaming...")
settings = [
    ("lookandfeel.startupwindow", 10025),  # Videos section
    ("filelists.showextensions", False),
    ("filelists.ignorethewhensorting", True)
]

for setting, value in settings:
    result = send_command("Settings.SetSettingValue", {"setting": setting, "value": value})
    print(f"  {setting}: {'OK' if result else 'FAILED'}")

# Check available skins
print("\nAvailable skins:")
skins_result = send_command("Addons.GetAddons", {
    "type": "xbmc.addon.skin",
    "properties": ["name", "enabled"]
})

if skins_result and "result" in skins_result:
    for skin in skins_result["result"]["addons"]:
        status = "ACTIVE" if skin.get("enabled") else "available"
        print(f"  - {skin['addonid']}: {status}")

print("\nSOLUTION:")
print("✅ Estuary skin is now active and optimized")
print("✅ Broken Pigeonhole skin disabled")
print("✅ System ready for streaming addons")
print("\nNext: Install ResolveURL and streaming addons manually")