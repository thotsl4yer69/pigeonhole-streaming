@echo off
REM Kodi v22 Alpha Deployment Script for Pigeonhole Entertainment Systems
REM This script automates the process of upgrading to Kodi v22 Alpha

echo === Pigeonhole Entertainment Systems - Kodi v22 Alpha Deployment ===
echo Target device: 192.168.1.107

REM Check if ADB is available
where adb >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: ADB not found in PATH
    echo Please ensure Android SDK platform-tools are installed and in PATH
    pause
    exit /b 1
)

echo ✓ ADB is available

REM Connect to device
echo Connecting to device...
adb connect 192.168.1.107
if %errorlevel% neq 0 (
    echo ERROR: Failed to connect to device
    pause
    exit /b 1
)

echo ✓ Connected to device

REM Check if device is connected
adb devices | findstr "192.168.1.107" >nul
if %errorlevel% neq 0 (
    echo ERROR: Device not found in connected devices list
    pause
    exit /b 1
)

echo ✓ Device is connected

REM Check current Kodi version
echo Checking current Kodi version...
adb -s 192.168.1.107 shell dumpsys package org.xbmc.kodi | findstr "versionName"
if %errorlevel% neq 0 (
    echo WARNING: Could not determine current Kodi version
)

REM Check if Kodi v22 APK exists
if not exist "M:\kodi-22.0-alpha1-arm64.apk" (
    echo WARNING: Kodi v22 APK not found
    echo Please download the Kodi v22 Alpha APK and place it in the M:\ directory
    echo Filename should be: kodi-22.0-alpha1-arm64.apk
    echo.
    echo Alternatively, you can:
    echo 1. Install v22 repositories only
    echo 2. Update existing addons to v22-compatible versions
    echo.
    set /p choice="Continue with repository-only upgrade? (Y/N): "
    if /i "%choice%" neq "Y" (
        echo Deployment cancelled
        pause
        exit /b 1
    )
    goto repository_upgrade
)

REM Install Kodi v22 APK
echo Installing Kodi v22 Alpha...
adb -s 192.168.1.107 install -r "M:\kodi-22.0-alpha1-arm64.apk"
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Kodi v22 APK
    pause
    exit /b 1
)

echo ✓ Kodi v22 Alpha installed successfully

:repository_upgrade
REM Push v22 repository files
echo Pushing v22 repository files to device...
if exist "M:\repo-v22.zip" (
    adb -s 192.168.1.107 push "M:\repo-v22.zip" /storage/emulated/0/Download/
    if %errorlevel% equ 0 (
        echo ✓ Pushed repo-v22.zip to device
    ) else (
        echo WARNING: Failed to push repo-v22.zip
    )
)

if exist "M:\repo-v22-fixed.zip" (
    adb -s 192.168.1.107 push "M:\repo-v22-fixed.zip" /storage/emulated/0/Download/
    if %errorlevel% equ 0 (
        echo ✓ Pushed repo-v22-fixed.zip to device
    ) else (
        echo WARNING: Failed to push repo-v22-fixed.zip
    )
)

REM Instructions for completing the upgrade
echo.
echo === Kodi v22 Alpha Deployment - Next Steps ===
echo 1. Open Kodi on your Fire TV Cube
echo 2. Go to Settings ^> Add-ons ^> Install from zip file
echo 3. Navigate to Download folder and select repo-v22-fixed.zip
echo 4. After installation, go to Install from repository
echo 5. Select the v22 repository
echo 6. Update your addons to v22-compatible versions
echo 7. Restart Kodi to complete the upgrade

echo.
echo === Optional: Additional v22 Repositories ===
echo You can also install these repositories for more addons:
echo - repository.pigeonhole.streaming-FIXED.zip
echo - repository.tikipeter.zip
echo - repository.nixgates.zip

echo.
echo Deployment script completed successfully!
pause