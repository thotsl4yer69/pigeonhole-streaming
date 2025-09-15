# FireCube Debloater and Privacy Toolkit

This toolkit helps you remove bloatware from your FireCube device and enhance privacy by blocking Amazon services.

## Files

1. `firecube_debloater.py` - Removes Amazon bloatware and optimizes the system
2. `post_debloat_checker.py` - Checks what packages remain after debloating
3. `network_blocker.py` - Blocks Amazon domains at the network level
4. `simple_kodi_optimizer.py` - Optimizes Kodi settings for better performance

## Requirements

- ADB (Android Debug Bridge) - included in platform-tools
- Python 3.x
- FireCube device connected to the same network
- USB debugging enabled on the FireCube (if using USB connection)

## Usage

### 1. Connect via Network (Recommended)

Make sure your FireCube is connected to the same network as your computer.

### 2. Run the Debloater

```bash
python firecube_debloater.py
```

This script will:
- Disable Amazon bloatware apps
- Block internet access for remaining Amazon services
- Optimize system settings for privacy

### 3. Check Results

```bash
python post_debloat_checker.py
```

This script will show you what packages remain after debloating.

### 4. Network-Level Blocking

```bash
python network_blocker.py
```

This script provides information on blocking Amazon domains at the network level.

## What Gets Removed

The debloater targets these types of Amazon services:
- Alexa and voice services
- Advertising and metrics collection
- Automatic updates and telemetry
- Shopping and marketplace apps
- Sync and cloud services
- Media and entertainment apps (except Kodi)
- Device management services

## What's Preserved

Essential system components are preserved:
- Android system packages
- Kodi media center
- Basic input and UI services
- Network and connectivity essentials

## Recommendations

1. **Before running**: Make sure you have a backup of your device
2. **After debloating**: Restart your device to apply all changes
3. **Enhanced privacy**: Set up Pi-hole or similar network-wide ad blocker
4. **VPN**: Consider installing a privacy-focused VPN
5. **WolfLauncher**: Install WolfLauncher for a better user interface

## Troubleshooting

If you encounter issues:

1. Make sure ADB is properly installed and accessible
2. Verify network connectivity to your FireCube
3. Check that USB debugging is enabled (if using USB)
4. Some packages may require root access to fully remove

## Disclaimer

This toolkit modifies your device software. While we've tested these scripts, we cannot guarantee they will work on all FireCube devices or that they won't cause issues. Use at your own risk.