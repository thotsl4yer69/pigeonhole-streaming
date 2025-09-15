# Pigeonhole Entertainment Systems

## Working Directory

This is the primary working directory (`M:\\`) for Pigeonhole Entertainment Systems, a company specializing in customized streaming solutions using Amazon Fire TV devices with Kodi media center software.

## Project Overview

This directory contains all the tools, configurations, and deployment systems for creating and managing fleets of customized streaming devices with enhanced capabilities beyond standard Fire TV offerings.

## 🚀 Quick Start (For Beginners!)

### 🆕 **NEW USERS - START HERE:**
```bash
python configure_pigeonhole_http.py
```
This HTTP-based tool will guide you through everything step-by-step with 100% reliability!

### 📚 **Or Follow These Simple Steps:**

#### Step 1: Get Your Fire TV Ready
1. **Enable Developer Options**: Settings → My Fire TV → About → Click your Fire TV name 7 times
2. **Enable ADB Debugging**: Settings → My Fire TV → Developer Options → Turn ON "ADB debugging"
3. **Enable HTTP Remote Control**: Settings → Services → Control → Allow remote control via HTTP
4. **Find your Fire TV IP**: Settings → My Fire TV → About → Network

#### Step 2: Quick Health Check
```bash
python test_http_simple.py
```
This checks if HTTP connection is working!

#### Step 3: Deploy via HTTP (Recommended)
```bash
python configure_pigeonhole_http.py
```

#### Step 4: Alternative ADB Deployment
```bash
adb connect YOUR_FIRE_TV_IP:5555
deploy_pigeonhole_gold_complete.bat
```

## Key Components

- **HTTP Deployment**: Modern, reliable deployment via Kodi HTTP API
- **Fire TV Optimization**: Hardware-specific performance tuning
- **Kodi builds**: Custom Kodi configurations and installations
- **Streaming Setup**: Complete streaming addon deployment
- **Deployment tools**: Applications and scripts for device management
- **Addon repositories**: Third-party Kodi addons and plugin configurations

## 🎯 Beginner-Friendly Tools

We've created special tools to help you understand and use your project:

- **🆕 `configure_pigeonhole_http.py`** - HTTP-based setup (100% reliable)
- **🔍 `test_http_simple.py`** - Check HTTP connection status
- **🎨 `skin_fix.py`** - Fix skin issues and optimize interface
- **📚 `PIGEONHOLE_FINAL_STATUS.md`** - Complete implementation guide
- **❓ `STREAMING_SOLUTION_COMPLETE.md`** - What's working and how to use it

## Specialized Agents

This project uses several specialized agents for different aspects of the business:

1. **pigeonhole-streaming-architect**: Fire TV hardware optimization and streaming setup
2. **kodi-expert**: Kodi performance tuning and addon management
3. **project-orchestrator**: Large-scale deployment coordination
4. **frontend**: User interface and experience optimization

## Documentation

- **PIGEONHOLE_FINAL_STATUS.md** - Current implementation status and next steps
- **FIRE_TV_CUBE_GOLD_BUILD_COMPLETE.md** - Gold build achievement guide
- **STREAMING_SOLUTION_COMPLETE.md** - Complete streaming setup guide
- **HTTP_FIRST_APPROACH.md** - Proven reliable deployment methodology

### Getting Help
- **Never used this before?** → Run `python configure_pigeonhole_http.py`
- **Something not working?** → Run `python test_http_simple.py`
- **Want to fix skin issues?** → Run `python skin_fix.py`
- **Need status update?** → Read `PIGEONHOLE_FINAL_STATUS.md`

## Getting Started

For new team members or collaborators, review the documentation files and consult with the appropriate specialized agent based on the task at hand.