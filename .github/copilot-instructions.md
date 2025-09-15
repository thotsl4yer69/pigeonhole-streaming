# Pigeonhole Streaming - GitHub Copilot Instructions

**ALWAYS follow these instructions first. Only search for additional context if the information here is incomplete or found to be in error.**

## Project Overview

Pigeonhole Streaming is an enterprise Fire TV/Android TV deployment framework that transforms Amazon Fire TV devices into custom-branded Kodi media centers. The system uses a Python backend with YAML-driven configuration to automate deployment, addon management, and remote control via HTTP API.

**Architecture**: 4-layer system - YAML configuration drives Python framework (device management, skin customization, ADB operations) that generates deployment scripts for Fire TV devices.

## Working Effectively

### Bootstrap and Dependencies

Install required dependencies:
```bash
pip3 install Pillow PyYAML requests
```

**NEVER CANCEL**: Installation typically takes 30-60 seconds. Set timeout to 120+ seconds.

### Core Validation (Always Run First)

Validate the project setup:
```bash
# Health check - takes ~0.1 seconds, NEVER CANCEL
python3 health_check.py

# Configuration validation - takes ~0.06 seconds  
python3 -c "import sys; sys.path.insert(0, './scripts'); from pigeonhole_config import get_config; config = get_config(); issues = config.validate_config(); print(f'Issues: {len(issues)}')"

# Core framework test - takes ~0.16 seconds
python3 -c "import sys; sys.path.insert(0, './scripts'); from pigeonhole_config import get_config; from pigeonhole_customizer import PigeonholeCustomizer; from pigeonhole_device_manager import create_device_manager; print('All systems operational')"
```

### Python Module Loading

**CRITICAL**: Use proper Python path for script imports:
```bash
# Correct way to import framework modules:
python3 -c "import sys; sys.path.insert(0, './scripts'); from pigeonhole_config import get_config"

# Or run from scripts directory:
cd scripts && python3 -c "from pigeonhole_config import get_config"

# With environment variable:
PYTHONPATH=./scripts:$PYTHONPATH python3 -c "from scripts.pigeonhole_config import get_config"
```

### No Traditional Build Process

This project does NOT have a traditional build process. Instead it has:
- **Configuration-driven deployment** using YAML files
- **Python framework validation** (very fast, <1 second)
- **ADB deployment scripts** for Fire TV devices
- **HTTP API validation** for remote testing

## Core Operations & Timing

### Configuration System (Instant - <0.1 seconds)
```bash
# Load and validate configuration
python3 -c "import sys; sys.path.insert(0, './scripts'); from pigeonhole_config import get_config; config = get_config(); print('Config loaded')"

# Validate configuration
python3 -c "import sys; sys.path.insert(0, './scripts'); from pigeonhole_config import get_config; config = get_config(); issues = config.validate_config(); print(f'Issues: {len(issues)}')"
```

### Health Check System (Fast - <0.1 seconds)
```bash
# Comprehensive project health check
python3 health_check.py
```

### Testing Framework (Fast for local tests)
```bash
# Test HTTP API connection (requires Fire TV device)
python3 test_kodi_http.py

# Test streaming functionality (requires Fire TV device)  
python3 test_streaming_functionality.py

# Basic addon validation
python3 addon_validation_system.py
```

**Note**: HTTP tests will fail without connected Fire TV device - this is normal.

## Validation Scenarios

### Always Test After Changes

1. **Configuration Validation**:
   ```bash
   python3 -c "import sys; sys.path.insert(0, './scripts'); from pigeonhole_config import get_config; config = get_config(); issues = config.validate_config(); print('Valid' if len(issues) == 0 else f'Issues: {issues}')"
   ```

2. **Module Import Test**:
   ```bash
   python3 -c "import sys; sys.path.insert(0, './scripts'); from pigeonhole_config import get_config; from pigeonhole_customizer import PigeonholeCustomizer; print('Imports successful')"
   ```

3. **Project Health Check**:
   ```bash
   python3 health_check.py
   ```

### Manual User Scenarios (For Interactive Testing)

**User Scenario 1**: New User Onboarding
```bash
# Run interactive setup guide
python3 start_here.py
# Test with input "n" to skip setup, verify tool loads correctly
```

**User Scenario 2**: Configuration Customization  
```bash
# Test customization system
python3 -c "import sys; sys.path.insert(0, './scripts'); from pigeonhole_customizer import PigeonholeCustomizer; c = PigeonholeCustomizer(); print('Customizer ready')"
```

**User Scenario 3**: Device Deployment (Fire TV Required)
```bash
# Note: Requires physical Fire TV device with ADB debugging enabled
# Test ADB availability: adb devices
# Main deployment: deploy_pigeonhole_stable_final.bat (Windows only)
```

## Linting and Code Quality

**No automated linting** - this project uses configuration-driven validation instead:

```bash
# Configuration validation (replaces traditional linting)
python3 -c "import sys; sys.path.insert(0, './scripts'); from pigeonhole_config import get_config; config = get_config(); issues = config.validate_config(); print('Valid' if len(issues) == 0 else issues)"

# Python syntax validation
python3 -m py_compile health_check.py
python3 -m py_compile scripts/pigeonhole_config.py
python3 -m py_compile scripts/pigeonhole_customizer.py
python3 -m py_compile scripts/pigeonhole_device_manager.py
```

## Working With Fire TV Devices

### ADB Requirements
- **ADB debugging must be enabled** on target Fire TV device
- **Same WiFi network** required for deployment
- **Default Fire TV IP**: 192.168.1.130 (configurable)

### Testing Without Hardware
```bash
# These work without Fire TV device:
python3 health_check.py
python3 start_here.py
python3 -c "import sys; sys.path.insert(0, './scripts'); from pigeonhole_config import get_config; print('Config works')"

# These require Fire TV device (will show connection errors otherwise):
python3 test_kodi_http.py
python3 test_streaming_functionality.py
```

## Key Project Components

### Essential Files
- `config/pigeonhole_config.yaml` - Master configuration (YAML-driven)
- `scripts/pigeonhole_config.py` - Configuration framework  
- `scripts/pigeonhole_customizer.py` - Branding/theme customization
- `scripts/pigeonhole_device_manager.py` - ADB/device management
- `deploy_pigeonhole_stable_final.bat` - Main deployment script (Windows)
- `health_check.py` - Project validation tool
- `start_here.py` - Beginner guidance tool

### Directory Structure
```
/scripts/          - Python automation framework  
/config/           - YAML configuration files
/addons/           - Kodi addons and plugins
/documentation/    - Setup guides and documentation
/.github/          - GitHub workflows (Gemini AI automation)
```

## Common Tasks

### Adding New Features
1. **Always modify `config/pigeonhole_config.yaml` first** (configuration-driven approach)
2. **Extend existing Python classes** in `/scripts/` (don't create new scripts)
3. **Use device manager for ADB operations** (connection pooling built-in)
4. **Validate changes**: Run health check + configuration validation

### Deployment Testing
1. **Configuration validation**: `python3 health_check.py`
2. **Module loading test**: Test all framework imports
3. **If Fire TV available**: Test HTTP API connectivity
4. **Manual validation**: Run `python3 start_here.py` to test user experience

### Troubleshooting
```bash
# Module import issues - use correct Python path:
export PYTHONPATH="./scripts:$PYTHONPATH"

# Configuration issues - check YAML syntax:
python3 -c "import yaml; yaml.safe_load(open('config/pigeonhole_config.yaml'))"

# Dependencies missing:
pip3 install Pillow PyYAML requests
```

## CRITICAL: Working Methods vs Failed Methods

### ✅ Always Use These (Validated Working)
- `python3 health_check.py` - Project validation
- YAML configuration modifications in `config/`
- Python framework classes with proper module paths
- Direct validation commands shown above

### ❌ Never Use These (Known to Fail) 
- Traditional build tools (make, npm, etc.) - **Not applicable**
- ZIP extraction operations - **Not supported on Android target**
- Complex XML manipulation - **Kodi-specific requirements**
- Deployment without ADB debugging enabled - **Will fail**

## Timeout Guidelines

**NEVER CANCEL** any of these operations:
- **Dependency installation**: 30-120 seconds (normal for pip install Pillow)
- **Python validation**: <1 second (always fast)
- **Health check**: <1 second (always fast)
- **Configuration loading**: <0.1 seconds (always instant)

**Set minimum timeouts**:
- Build commands: 120+ seconds (for dependency installation)
- Test commands: 60+ seconds (though most are instant)
- Health checks: 30+ seconds (though typically <1 second)

## Expected Error Conditions

**Normal/Expected Errors** (not failures):
- HTTP connection timeouts when Fire TV device not connected
- ADB "device not found" when no Fire TV connected  
- Config file warnings when using defaults (M:/pigeonhole_config.yaml not found)

**Actual Failures**:
- Python import errors (missing dependencies)
- YAML syntax errors in configuration files
- Missing essential project files