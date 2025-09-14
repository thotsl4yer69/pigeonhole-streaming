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

## 🚀 Quick Start

### Prerequisites
- ADB (Android Debug Bridge) access to Fire TV devices
- Python 3.7+ for automation scripts
- Network access to target Fire TV devices

### Basic Setup

1. **Enable Developer Options** on your Fire TV device
2. **Enable ADB Debugging** in Developer Options
3. **Connect to your Fire TV**:
   ```bash
   adb connect YOUR_FIRE_TV_IP:5555
   ```
4. **Run deployment script**:
   ```batch
   deploy_pigeonhole_stable_final.bat
   ```

## 📁 Project Structure

- `deploy_*.bat` - Deployment scripts for various configurations
- `kodi_*.py` - Python automation and control scripts
- `config/` - Configuration files and settings
- `addons/` - Kodi addon packages
- `scripts/` - Utility and maintenance scripts
- `documentation/` - Setup guides and technical documentation

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