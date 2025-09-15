@echo off
REM FireCube Debloater Script
REM Removes Amazon bloatware and optimizes the system

echo === FireCube Debloater ===
echo This script will remove Amazon bloatware and optimize your device
echo WARNING: This will remove many Amazon services. Proceed with caution!
echo.

REM Connect to device
echo Connecting to FireCube device...
M:\platform-tools\adb.exe connect 192.168.1.107:5555
echo.

REM Confirm with user
set /p confirm=Do you want to proceed with debloating? (yes/no): 
if /i "%confirm%" neq "yes" if /i "%confirm%" neq "y" (
    echo Debloating cancelled
    pause
    exit /b
)

echo.
echo Starting debloating process...

REM Disable Amazon bloatware
echo.
echo 1. Disabling Amazon bloatware...

REM Alexa and voice services
M:\platform-tools\adb.exe -s 192.168.1.107:5555 shell pm disable-user --user 0 com.amazon.alexamediaplayer.runtime.ftv
echo [OK] Disabled Alexa Media Player

M:\platform-tools\adb.exe -s 192.168.1.107:5555 shell pm disable-user --user 0 com.amazon.alexa.datastore.app
echo [OK] Disabled Alexa Data Store

M:\platform-tools\adb.exe -s 192.168.1.107:5555 shell pm disable-user --user 0 com.amazon.tv.alexaalerts
echo [OK] Disabled Alexa Alerts

M:\platform-tools\adb.exe -s 192.168.1.107:5555 shell pm disable-user --user 0 com.amazon.tv.alexanotifications
echo [OK] Disabled Alexa Notifications

REM Advertising and metrics
M:\platform-tools\adb.exe -s 192.168.1.107:5555 shell pm disable-user --user 0 com.amazon.client.metrics
echo [OK] Disabled Client Metrics

M:\platform-tools\adb.exe -s 192.168.1.107:5555 shell pm disable-user --user 0 com.amazon.client.metrics.api
echo [OK] Disabled Client Metrics API

M:\platform-tools\adb.exe -s 192.168.1.107:5555 shell pm disable-user --user 0 com.amazon.tv.fw.metrics
echo [OK] Disabled Fire TV Metrics

M:\platform-tools\adb.exe -s 192.168.1.107:5555 shell pm disable-user --user 0 com.amazon.wirelessmetrics.service
echo [OK] Disabled Wireless Metrics

REM Shopping and marketplace
M:\platform-tools\adb.exe -s 192.168.1.107:5555 shell pm disable-user --user 0 com.amazon.venezia
echo [OK] Disabled Amazon Appstore

M:\platform-tools\adb.exe -s 192.168.1.107:5555 shell pm disable-user --user 0 com.amazon.shoptv.firetv.client
echo [OK] Disabled Shop TV Client

M:\platform-tools\adb.exe -s 192.168.1.107:5555 shell pm disable-user --user 0 com.amazon.shoptv.client
echo [OK] Disabled Shop TV

REM Updates and sync
M:\platform-tools\adb.exe -s 192.168.1.107:5555 shell pm disable-user --user 0 com.amazon.device.software.ota
echo [OK] Disabled OTA Updates

M:\platform-tools\adb.exe -s 192.168.1.107:5555 shell pm disable-user --user 0 com.amazon.device.sync
echo [OK] Disabled Device Sync

M:\platform-tools\adb.exe -s 192.168.1.107:5555 shell pm disable-user --user 0 com.amazon.sync.service
echo [OK] Disabled Sync Service

REM Media services
M:\platform-tools\adb.exe -s 192.168.1.107:5555 shell pm disable-user --user 0 com.amazon.avod
echo [OK] Disabled Amazon Video

M:\platform-tools\adb.exe -s 192.168.1.107:5555 shell pm disable-user --user 0 com.amazon.imdb.tv.android.app
echo [OK] Disabled IMDb TV

M:\platform-tools\adb.exe -s 192.168.1.107:5555 shell pm disable-user --user 0 com.amazon.minitv.android.app
echo [OK] Disabled Mini TV

REM Device management
M:\platform-tools\adb.exe -s 192.168.1.107:5555 shell pm disable-user --user 0 com.amazon.tv.parentalcontrols
echo [OK] Disabled Parental Controls

M:\platform-tools\adb.exe -s 192.168.1.107:5555 shell pm disable-user --user 0 com.amazon.tv.devicecontrolsettings
echo [OK] Disabled Device Control Settings

M:\platform-tools\adb.exe -s 192.168.1.107:5555 shell pm disable-user --user 0 com.amazon.tv.settings.v2
echo [OK] Disabled TV Settings V2

REM Other services
M:\platform-tools\adb.exe -s 192.168.1.107:5555 shell pm disable-user --user 0 com.amazon.ftv.screensaver
echo [OK] Disabled Screensaver

M:\platform-tools\adb.exe -s 192.168.1.107:5555 shell pm disable-user --user 0 com.amazon.notification
echo [OK] Disabled Notifications

M:\platform-tools\adb.exe -s 192.168.1.107:5555 shell pm disable-user --user 0 com.amazon.tv.website_launcher
echo [OK] Disabled Website Launcher

echo.
echo 2. Blocking internet access for remaining Amazon services...

REM Block internet access for key Amazon services
M:\platform-tools\adb.exe -s 192.168.1.107:5555 shell pm restrict-background com.amazon.device.software.ota
echo [OK] Restricted OTA Updates

M:\platform-tools\adb.exe -s 192.168.1.107:5555 shell pm restrict-background com.amazon.client.metrics
echo [OK] Restricted Metrics

M:\platform-tools\adb.exe -s 192.168.1.107:5555 shell pm restrict-background com.amazon.venezia
echo [OK] Restricted Appstore

echo.
echo === Debloating Complete ===
echo.
echo Recommendations:
echo 1. Restart your FireCube device
echo 2. Check that Kodi is still working properly
echo 3. Install WolfLauncher for a better interface
echo 4. Consider installing a VPN for privacy
echo.
pause