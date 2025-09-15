@echo off
REM Verify Pigeonhole Streaming Installation
REM This script checks if the Pigeonhole Streaming repository and addons are properly installed

echo === Pigeonhole Streaming Installation Verification ===
echo.

REM Connect to device
echo Connecting to FireCube device...
M:\platform-tools\adb.exe connect 192.168.1.107:5555
echo.

REM Check if repository is installed
echo Checking if Pigeonhole Streaming Repository is installed...
M:\platform-tools\adb.exe -s 192.168.1.107:5555 shell ls /storage/emulated/0/Android/data/org.xbmc.kodi/files/.kodi/addons/repository.pigeonhole.streaming/addon.xml >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Pigeonhole Streaming Repository is not installed
    pause
    exit /b 1
)
echo [OK] Pigeonhole Streaming Repository is installed

REM Check if addons are installed
echo Checking if Pigeonhole addons are installed...
M:\platform-tools\adb.exe -s 192.168.1.107:5555 shell ls /storage/emulated/0/Android/data/org.xbmc.kodi/files/.kodi/addons/plugin.video.fen.lite/addon.xml >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Pigeonhole addons are not installed
    pause
    exit /b 1
)
echo [OK] Pigeonhole addons are installed

REM Check if Kodi is running
echo Checking if Kodi is running...
M:\platform-tools\adb.exe -s 192.168.1.107:5555 shell ps | findstr -i kodi >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Kodi is not currently running
    echo Please start Kodi manually to use the installed addons
) else (
    echo [OK] Kodi is running
)

echo.
echo === Verification Complete ===
echo.
echo Summary:
echo - Pigeonhole Streaming Repository: Installed
echo - Pigeonhole Addons: Installed
echo.
echo You can now use the Pigeonhole Streaming repository in Kodi.
echo.
pause