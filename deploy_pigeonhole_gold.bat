@echo off
echo ================================================
echo PIGEONHOLE STREAMING - GOLD DEPLOYMENT SCRIPT
echo Fire TV Cube - Kodi v22 Alpha - Complete Setup
echo ================================================

set FIRE_TV_IP=192.168.1.130
set ADB_PATH=M:\platform-tools\adb.exe

echo [1/10] Connecting to Fire TV Cube...
%ADB_PATH% connect %FIRE_TV_IP%:5555

echo [2/10] Installing Kodi v22 Alpha ARM32...
%ADB_PATH% install "C:\Users\Jack\Downloads\kodi-22.0-Piers_alpha1-armeabi-v7a.apk"

echo [3/10] Deploying Arctic Zephyr Pigeonhole Skin...
%ADB_PATH% push "M:\arctic-zephyr-pigeonhole" "/sdcard/Android/data/org.xbmc.kodi/files/.kodi/addons/"

echo [4/10] Installing ResolveURL Module...
%ADB_PATH% push "M:\addons\script.module.resolveurl" "/sdcard/Android/data/org.xbmc.kodi/files/.kodi/addons/"

echo [5/10] Installing The Crew Streaming Addon...
%ADB_PATH% push "M:\addons\plugin.video.thecrew" "/sdcard/Android/data/org.xbmc.kodi/files/.kodi/addons/"

echo [6/10] Installing Mad Titan Sports...
%ADB_PATH% push "M:\addons\plugin.video.madtitansports" "/sdcard/Android/data/org.xbmc.kodi/files/.kodi/addons/"

echo [7/10] Installing FEN Lite Pigeonhole Edition...
%ADB_PATH% push "M:\addons\plugin.video.fen.lite" "/sdcard/Android/data/org.xbmc.kodi/files/.kodi/addons/"

echo [8/10] Installing Pigeonhole Configuration System...
%ADB_PATH% push "M:\addons\script.pigeonhole.config" "/sdcard/Android/data/org.xbmc.kodi/files/.kodi/addons/"

echo [9/10] Applying Pigeonhole Branding...
%ADB_PATH% push "M:\config\authentic_pigeonhole_branding.xml" "/sdcard/Android/data/org.xbmc.kodi/files/.kodi/userdata/favourites.xml"

echo [10/10] Starting Kodi with Gold Configuration...
%ADB_PATH% shell "am start -n org.xbmc.kodi/.Splash"

echo ================================================
echo PIGEONHOLE STREAMING GOLD SETUP COMPLETE!
echo 
echo Installed Components:
echo - Arctic Zephyr Pigeonhole Edition Skin
echo - The Crew Streaming Addon
echo - Mad Titan Sports Live Streaming  
echo - FEN Lite Pigeonhole Edition
echo - ResolveURL Support Module
echo - Pigeonhole Configuration System
echo - Professional Pigeonhole Branding
echo 
echo Ready for Real Debrid configuration!
echo ================================================
pause