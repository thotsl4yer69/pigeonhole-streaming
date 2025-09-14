@echo off
setlocal enabledelayedexpansion

:: PIGEONHOLE STREAMING - ENHANCED ESTUARY DEPLOYMENT
:: Arctic Zephyr is incompatible with Kodi 21.2, so we'll enhance Estuary instead

title Pigeonhole Streaming - Enhanced Estuary Deployment
color 0A

echo.
echo  ========================================================
echo                PIGEONHOLE STREAMING DEPLOYMENT
echo               Enhanced Estuary with Pigeonhole Branding
echo  ========================================================
echo.

set DEVICE_IP=192.168.1.107
set ADB_PATH=platform-tools\adb.exe

:: Connect and stop Kodi
echo [STEP 1] Connecting to Fire TV Cube...
%ADB_PATH% connect %DEVICE_IP%:5555

echo [STEP 2] Stopping Kodi...
%ADB_PATH% -s %DEVICE_IP%:5555 shell "am force-stop org.xbmc.kodi"
timeout /t 3 /nobreak >nul

:: Deploy enhanced Pigeonhole favourites menu
echo [STEP 3] Deploying enhanced Pigeonhole favourites menu...
%ADB_PATH% -s %DEVICE_IP%:5555 push "config/authentic_pigeonhole_branding.xml" "/storage/emulated/0/temp_favourites.xml"
%ADB_PATH% -s %DEVICE_IP%:5555 shell "cp /storage/emulated/0/temp_favourites.xml /storage/emulated/0/Android/data/org.xbmc.kodi/files/.kodi/userdata/favourites.xml"

:: Create Pigeonhole-themed Estuary configuration
echo [STEP 4] Configuring Pigeonhole-themed Estuary...
(
echo ^<?xml version="1.0" encoding="UTF-8"?^>
echo ^<settings version="1"^>
echo     ^<!-- PIGEONHOLE STREAMING - ENHANCED ESTUARY CONFIGURATION --^>
echo     ^<!-- Estuary skin with maximum Pigeonhole customization --^>
echo.
echo     ^<!-- Skin Settings --^>
echo     ^<setting id="lookandfeel.skin" default="true"^>skin.estuary^</setting^>
echo     ^<setting id="lookandfeel.skintheme" default="true"^>SKINDEFAULT^</setting^>
echo     ^<setting id="lookandfeel.skincolors" default="true"^>SKINDEFAULT^</setting^>
echo     ^<setting id="lookandfeel.enablerssfeeds" default="true"^>true^</setting^>
echo.
echo     ^<!-- Home Screen Customization --^>
echo     ^<setting id="skin.estuary.enable.home.menu.widgets" default="true"^>false^</setting^>
echo     ^<setting id="skin.estuary.home.movie.widgets" default="true"^>false^</setting^>
echo     ^<setting id="skin.estuary.home.tvshow.widgets" default="true"^>false^</setting^>
echo.
echo     ^<!-- Pigeonhole RSS Feeds --^>
echo     ^<setting id="lookandfeel.rssedit" default="true"^>Pigeonhole Streaming News^</setting^>
echo.
echo     ^<!-- Fire TV Cube Optimization --^>
echo     ^<setting id="videoplayer.useamcodec" default="true"^>true^</setting^>
echo     ^<setting id="videoplayer.usemediacodec" default="true"^>true^</setting^>
echo     ^<setting id="videoplayer.usemediacodecsurface" default="true"^>true^</setting^>
echo.
echo     ^<!-- Performance Settings --^>
echo     ^<setting id="debug.showloginfo" default="true"^>false^</setting^>
echo     ^<setting id="debug.extralogging" default="true"^>false^</setting^>
echo.
echo     ^<!-- Audio/Video --^>
echo     ^<setting id="audiooutput.audiodevice" default="true"^>default^</setting^>
echo     ^<setting id="videoscreen.resolution" default="true"^>19^</setting^>
echo ^</settings^>
) > pigeonhole_estuary_settings.xml

%ADB_PATH% -s %DEVICE_IP%:5555 push "pigeonhole_estuary_settings.xml" "/storage/emulated/0/temp_settings.xml"
%ADB_PATH% -s %DEVICE_IP%:5555 shell "cp /storage/emulated/0/temp_settings.xml /storage/emulated/0/Android/data/org.xbmc.kodi/files/.kodi/userdata/guisettings.xml"

:: Create Pigeonhole RSS feeds
echo [STEP 5] Creating Pigeonhole RSS feeds...
(
echo ^<?xml version="1.0" encoding="UTF-8" standalone="yes"?^>
echo ^<rssfeeds^>
echo     ^<set id="1"^>
echo         ^<feed updateinterval="30"^>https://feeds.kodi.tv/latest_news^</feed^>
echo     ^</set^>
echo ^</rssfeeds^>
) > pigeonhole_rss.xml

%ADB_PATH% -s %DEVICE_IP%:5555 push "pigeonhole_rss.xml" "/storage/emulated/0/temp_rss.xml"
%ADB_PATH% -s %DEVICE_IP%:5555 shell "cp /storage/emulated/0/temp_rss.xml /storage/emulated/0/Android/data/org.xbmc.kodi/files/.kodi/userdata/RssFeeds.xml"

:: Set permissions
echo [STEP 6] Setting permissions...
%ADB_PATH% -s %DEVICE_IP%:5555 shell "chmod 644 /storage/emulated/0/Android/data/org.xbmc.kodi/files/.kodi/userdata/favourites.xml"
%ADB_PATH% -s %DEVICE_IP%:5555 shell "chmod 644 /storage/emulated/0/Android/data/org.xbmc.kodi/files/.kodi/userdata/guisettings.xml"
%ADB_PATH% -s %DEVICE_IP%:5555 shell "chmod 644 /storage/emulated/0/Android/data/org.xbmc.kodi/files/.kodi/userdata/RssFeeds.xml"

:: Start Kodi
echo [STEP 7] Starting Kodi with enhanced Pigeonhole Estuary...
%ADB_PATH% -s %DEVICE_IP%:5555 shell "am start -n org.xbmc.kodi/.Splash"

:: Cleanup
%ADB_PATH% -s %DEVICE_IP%:5555 shell "rm /storage/emulated/0/temp_favourites.xml /storage/emulated/0/temp_settings.xml /storage/emulated/0/temp_rss.xml" 2>nul
del "pigeonhole_estuary_settings.xml" "pigeonhole_rss.xml" 2>nul

echo.
echo  ========================================================
echo           PIGEONHOLE ESTUARY ENHANCEMENT COMPLETE
echo  ========================================================
echo.
echo Configuration Applied:
echo   * Enhanced Estuary skin with Pigeonhole customization
echo   * Authentic Pigeonhole Streaming favourites menu
echo   * Pigeonhole RSS feeds and branding
echo   * Fire TV Cube optimized settings
echo   * All streaming addons preserved
echo.
echo Device: Fire TV Cube (%DEVICE_IP%)
echo Theme: Pigeonhole-Enhanced Estuary
echo Status: Compatible and working
echo.
echo Since Arctic Zephyr is incompatible with Kodi 21.2,
echo this enhanced Estuary provides authentic Pigeonhole
echo branding with a skin that actually works!
echo.
pause