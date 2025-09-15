# Pigeonhole Streaming System

A comprehensive streaming media solution for Fire TV devices with Kodi integration, featuring automated deployment, fleet management, and optimized configurations.

## 🎯 Overview

Pigeonhole Streaming is an advanced streaming media architecture designed for Fire TV devices. It provides automated deployment scripts, custom Kodi configurations, addon management, and fleet-wide monitoring capabilities.

## ✨ Key Features

- **Automated Deployment**: One-click deployment scripts for Fire TV devices
- **Fleet Management**: Monitor and manage multiple Fire TV devices
- **Custom Kodi Integration**: Optimized Kodi configurations with Arctic Zephyr theme
- **Addon Management**: Automated addon installation and validation
- **HTTP Control**: Remote control via HTTP API
- **Real Debrid Integration**: Premium streaming service integration
- **Recovery Systems**: Automated backup and recovery mechanisms

## 🚀 Quick Start (For Beginners!)

### 🆕 **NEW USERS - START HERE:**
```bash
python3 start_here.py
```
This interactive tool will guide you through everything step-by-step!

### 📚 **Or Follow These Simple Steps:**

#### Step 1: Get Your Fire TV Ready
1. **Enable Developer Options**: Settings → My Fire TV → About → Click your Fire TV name 7 times
2. **Enable ADB Debugging**: Settings → My Fire TV → Developer Options → Turn ON "ADB debugging"
3. **Find your Fire TV IP**: Settings → My Fire TV → About → Network

#### Step 2: Quick Health Check
```bash
python3 health_check.py
```
This checks if everything is ready to go!

#### Step 3: Connect and Deploy
```bash
adb connect YOUR_FIRE_TV_IP:5555
deploy_pigeonhole_stable_final.bat
```

#### Step 4: Customize (Optional)
```bash
python3 easy_customize.py
```
Change colors, name, and apps without coding!

## 🎯 Beginner-Friendly Tools

We've created special tools to help you understand and use your project:

- **🆕 `start_here.py`** - Interactive guide for complete beginners
- **🔍 `health_check.py`** - Check what's working and what needs attention  
- **🎨 `easy_customize.py`** - Change colors and branding without coding
- **📚 `BEGINNER_GUIDE.md`** - Complete step-by-step tutorial
- **❓ `WHAT_DOES_THIS_DO.md`** - Explains what each file does

### Getting Help
- **Never used this before?** → Run `python3 start_here.py`
- **Something not working?** → Run `python3 health_check.py`
- **Want to customize?** → Run `python3 easy_customize.py`
- **Need to understand files?** → Read `WHAT_DOES_THIS_DO.md`

## 🔧 Configuration

### Core Components
- **Kodi 21.1**: Latest stable Kodi installation
- **Arctic Zephyr Theme**: Custom Pigeonhole branding
- **Addon Repository**: Curated addon collection
- **HTTP Remote Control**: Web-based device management

### Key Scripts
- `deploy_pigeonhole_stable_final.bat` - Main deployment script
- `kodi_http_controller.py` - HTTP API controller
- `enable_pigeonhole_addons.py` - Addon activation system
- `test_streaming_functionality.py` - System validation

## 📊 Fleet Management

Monitor multiple devices with:
- `fleet-monitoring.py` - Real-time fleet status
- `fleet-config.yaml` - Device configuration management
- `ansible-firetv-fleet.yml` - Ansible automation playbook

## 🛠️ Development

### Testing
```bash
python test_kodi_http.py
python test_streaming_functionality.py
```

### Validation
```bash
python addon_validation_system.py
```

## 📝 Documentation

- `PIGEONHOLE_GOLD_SETUP_GUIDE.md` - Complete setup guide
- `PIGEONHOLE_PROJECT_STRUCTURE.md` - Project architecture
- `HTTP_FIRST_APPROACH.md` - HTTP control documentation

## 🤝 Contributing

This project is designed for streaming media enthusiasts and Fire TV device management. Contributions welcome for:
- Device compatibility improvements
- Deployment automation enhancements
- Monitoring and alerting features
- Documentation updates

## ⚖️ Legal Notice

This project is for educational and personal use. Users are responsible for compliance with local laws and terms of service for streaming platforms and content providers.

## 🔧 Support

For issues and questions:
1. Check the documentation in `/documentation`
2. Review setup guides
3. Validate your Fire TV device configuration
4. Ensure network connectivity

---

**Built for streamlined Fire TV device management and optimized media streaming experiences.**