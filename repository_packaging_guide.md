# Fire TV Cube Repository Packaging Guide

## Critical Compatibility Requirements

### Kodi 21.1 ARM32 Specifications
- **Platform**: Android 9 (API 28)
- **Architecture**: ARM32 (armeabi-v7a)
- **Minimum addon API**: 12.0.0
- **Maximum zip size**: 50MB (Fire TV limit)

### Required Repository Structure
```
repository.pigeonhole.streaming/
├── addon.xml              # Primary addon definition
├── addons.xml             # Repository catalog
├── addons.xml.md5         # Integrity checksum
├── changelog.txt          # Version history
├── icon.png              # 512x512 repository icon
├── fanart.jpg            # 1920x1080 background
└── README.txt            # Installation instructions
```

### Fire TV Restrictions
1. **Memory constraints**: Max 150MB addon cache
2. **Network timeouts**: 10-second download limit
3. **Storage limitations**: /sdcard/Android/data/ only
4. **ARM32 binary compatibility**: No x86 libraries
5. **Amazon appstore compliance**: No sideload detection

### Packaging Commands
```bash
# Create properly formatted zip
cd repository.pigeonhole.streaming/
zip -r ../repository.pigeonhole.streaming-1.0.0.zip . -x "*.DS_Store" "*.git*"

# Verify zip integrity
unzip -t repository.pigeonhole.streaming-1.0.0.zip

# Check file permissions
zipinfo repository.pigeonhole.streaming-1.0.0.zip
```

### Installation Methods

#### Method 1: Local Network (Recommended)
1. Copy zip to Fire TV via ADB
2. Use ES File Explorer to navigate
3. Install via Kodi > Settings > Add-ons > Install from zip

#### Method 2: HTTP Server
1. Host on local HTTP server (port 8080)
2. Access via Fire TV browser
3. Download and install manually

#### Method 3: Cloud Storage
1. Upload to GitHub releases
2. Use direct download link
3. Install via network location

### Troubleshooting Crashes

**Immediate Fixes**:
- Ensure addon.xml UTF-8 encoding
- Verify all required XML elements present
- Check zip file integrity
- Validate MD5 checksums match

**Common Issues**:
- Missing `<requires>` section → parser crash
- Invalid version numbers → dependency failure
- Missing platform tags → compatibility crash
- Oversized icons → memory crash

### Testing Procedure
1. Test on Android emulator first
2. Validate with Kodi addon checker
3. Install on Fire TV development device
4. Monitor Kodi logs for errors
5. Test repository functionality

### Performance Optimization
- Compress images to <100KB each
- Minimize XML whitespace
- Use CDN for remote hosting
- Implement proper caching headers
- Monitor download speeds on Fire TV WiFi