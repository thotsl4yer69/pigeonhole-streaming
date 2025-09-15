# Simple Kodi Optimization Tools

This directory contains simple scripts to optimize your Kodi setup on FireCube devices.

## Files

1. `simple_kodi_optimizer.py` - Optimizes video, network, and service settings
2. `simple_addon_checker.py` - Lists installed addons
3. `simple_kodi_v22_checker.py` - Checks if Kodi v22 upgrade is needed
4. `simple_optimized_settings.xml` - XML settings file with optimizations

## Usage

1. Make sure your FireCube device is on the same network
2. Ensure Kodi is running with web server enabled
3. Default credentials are kodi/0000
4. Run the Python scripts:
   ```
   python simple_kodi_optimizer.py
   python simple_addon_checker.py
   python simple_kodi_v22_checker.py
   ```

## Settings Applied

The optimizer script applies these settings:

### Video
- Enables MediaCodec hardware acceleration
- Enables MediaCodecSurface rendering
- Sets render method to auto

### Network
- Disables IPv6
- Sets CURL retries to 2
- Sets HTTP max read rate to 4096

### Services
- Disables AirPlay
- Disables UPnP
- Disables Zeroconf

## Manual Settings Installation

To manually apply the optimized settings:

1. Open Kodi
2. Go to Settings > System > Import/Export
3. Select "Import all settings from a file"
4. Choose the `simple_optimized_settings.xml` file

## Upgrade to Kodi v22

To upgrade to Kodi v22:

1. Download the Kodi v22 APK for ARM64
2. Connect via ADB: `adb connect 192.168.1.107`
3. Install: `adb install kodi-22.X.X-arm64.apk`
4. Restart Kodi