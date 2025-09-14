# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Pigeonhole Streaming** - Enterprise Kodi deployment framework with Python backend and YAML-driven configuration for Android TV devices (Fire TV Cube/Stick, NVIDIA Shield, etc.).

**Key Architecture**: 4-layer system - YAML configuration drives Python framework (device management, skin customization, ADB operations) that generates deployment scripts.

## Essential Commands

### Primary Deployment
```bash
# Main deployment to Fire TV Cube (production ready)
./deploy_pigeonhole_final.bat

# Manual deployment steps
adb connect 192.168.1.107:5555
adb shell "am force-stop org.xbmc.kodi"
adb push config/authentic_pigeonhole_branding.xml /storage/emulated/0/Android/data/org.xbmc.kodi/files/.kodi/userdata/favourites.xml
adb shell "am start -n org.xbmc.kodi/.Splash"
```

### Python Framework Usage
```bash
# Configuration validation (run before deployment)
python -c "from scripts.pigeonhole_config import get_config; print(get_config().validate_config())"

# Device discovery
python scripts/pigeonhole_device_manager.py

# Custom skin generation
python scripts/pigeonhole_customizer.py
```

## Critical Architecture Knowledge

### Configuration System
- **Master config**: `config/pigeonhole_config.yaml` - ALL settings controlled here
- **Deployment profiles**: corporate, home, hotel, retail (different security/feature sets)
- **Device profiles**: Fire TV Cube/Stick, NVIDIA Shield (different performance settings)
- Always validate config before deployment: `get_config().validate_config()`

### Python Framework Structure
```python
# Use existing framework instead of creating new scripts:
from scripts.pigeonhole_config import get_config
from scripts.pigeonhole_device_manager import create_device_manager

# Configuration-driven approach:
config = get_config()
device_profile = config.get_device_profile('corporate')
```

### ADB Management
- Framework has connection pooling and device discovery
- Use context managers: `with device_manager.adb.device_connection(ip)`
- Device classification automatic (Fire TV Cube vs Stick vs Shield)

## What Actually Works vs. What Fails

### ✅ Working Methods (Use These)
- `deploy_pigeonhole_final.bat` - Context7-validated, production tested
- Direct ADB file push operations 
- YAML configuration modifications
- Python framework classes with proper error handling

### ❌ Failed Methods (Don't Repeat)
- ZIP extraction on Android (`unzip` not available)
- Python scripts with PIL dependencies (library missing)
- Complex XML manipulation (Kodi rejects)
- "Corporate" branding (wrong - use "Pigeonhole Streaming by MZ1312")

## Authentic Branding Requirements
- **Name**: "PIGEONHOLE STREAMING" by MZ1312 (never "corporate")
- **Colors**: Deep blue (#4A5A7A) with dove imagery 🕊️
- **Tagline**: "ALL YOUR ENTERTAINMENT. ONE DEVICE"

## Development Patterns

### Adding New Features
1. Modify `config/pigeonhole_config.yaml` first (configuration-driven)
2. Extend existing Python classes, don't create new scripts
3. Use device manager for all ADB operations
4. Follow established error handling patterns

### Key File Paths
- **Kodi userdata**: `/storage/emulated/0/Android/data/org.xbmc.kodi/files/.kodi/userdata/`
- **Critical files**: `favourites.xml`, `guisettings.xml`, `advancedsettings.xml`
- **ADB tools**: `platform-tools/adb.exe`

## Dependencies
- Python 3.7+ with `pyyaml`, `pillow`, `requests`
- ADB debugging enabled on target devices
- Same network subnet for deployment

---

**Core Principle**: Configuration-driven enterprise framework. Modify YAML config, use existing Python classes, avoid ad-hoc scripts.