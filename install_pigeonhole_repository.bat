@echo off
REM Install Pigeonhole Streaming Repository on FireCube
REM This script installs the Pigeonhole Streaming repository on a FireCube device

echo === Pigeonhole Streaming Repository Installer ===
echo.

REM Connect to device
echo Connecting to FireCube device...
M:\platform-tools\adb.exe connect 192.168.1.107:5555
echo.

REM Push repository files to device
echo Pushing repository files to device...
M:\platform-tools\adb.exe -s 192.168.1.107:5555 push M:\pigeonhole-streaming\repository.pigeonhole.streaming /storage/emulated/0/Download/repository.pigeonhole.streaming
if %errorlevel% neq 0 (
    echo ERROR: Failed to push repository files to device
    pause
    exit /b 1
)
echo [OK] Repository files pushed to device
echo.

REM Push addon files to device
echo Pushing addon files to device...
M:\platform-tools\adb.exe -s 192.168.1.107:5555 push M:\pigeonhole-streaming\addons /storage/emulated/0/Download/addons
if %errorlevel% neq 0 (
    echo ERROR: Failed to push addon files to device
    pause
    exit /b 1
)
echo [OK] Addon files pushed to device
echo.

REM Install repository in Kodi
echo Installing repository in Kodi...
echo NOTE: This requires Kodi to be running with web server enabled
echo If this fails, please start Kodi manually and try again
echo.

REM Try to install via JSON-RPC API
curl -u kodi:0000 -H "Content-Type: application/json" -X POST -d "{\"jsonrpc\":\"2.0\",\"method\":\"Addons.InstallAddonFromZip\",\"params\":{\"path\":\"/storage/emulated/0/Download/repository.pigeonhole.streaming\"},\"id\":1}" http://192.168.1.107:8080/jsonrpc >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Failed to install repository via JSON-RPC API
    echo Will try alternative method...
    
    REM Alternative method: Copy to Kodi addons directory
    echo Copying repository to Kodi addons directory...
    M:\platform-tools\adb.exe -s 192.168.1.107:5555 shell cp -r /storage/emulated/0/Download/repository.pigeonhole.streaming /storage/emulated/0/Android/data/org.xbmc.kodi/files/.kodi/addons/
    if %errorlevel% neq 0 (
        echo ERROR: Failed to copy repository to Kodi addons directory
        pause
        exit /b 1
    )
    echo [OK] Repository copied to Kodi addons directory
) else (
    echo [OK] Repository installed via JSON-RPC API
)

echo.
echo === Installation Complete ===
echo.
echo Next steps:
echo 1. Open Kodi on your FireCube device
echo 2. Go to Settings ^> Add-ons ^> Install from repository
echo 3. Select "Pigeonhole Streaming Repository"
echo 4. Browse and install addons from the repository
echo.
echo For manual installation:
echo 1. In Kodi, go to Settings ^> Add-ons ^> Install from zip file
echo 2. Navigate to the Download folder
echo 3. Select the repository.pigeonhole.streaming folder
echo 4. Select addon.xml to install the repository
echo.
pause