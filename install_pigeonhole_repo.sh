#!/bin/bash
# Pigeonhole Repository Installation Script

# Copy repository to Kodi addons directory
cp -r /storage/emulated/0/kodi/addons/repository.pigeonhole.streaming /storage/emulated/0/Android/data/org.xbmc.kodi/files/.kodi/addons/

# Copy addons to Kodi addons directory
cp -r /storage/emulated/0/kodi/addons/plugin.video.* /storage/emulated/0/Android/data/org.xbmc.kodi/files/.kodi/addons/

# Update Kodi addons
am force-stop org.xbmc.kodi
sleep 5
am start org.xbmc.kodi/.Splash

echo "Pigeonhole Repository installation completed. Please restart Kodi to see the changes."