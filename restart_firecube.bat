@echo off
REM FireCube Restart Script
REM Restarts the FireCube device to apply all changes

echo === FireCube Restart ===
echo This script will restart your FireCube device
echo to apply all debloating changes.
echo.

REM Connect to device
echo Connecting to FireCube device...
M:\platform-tools\adb.exe connect 192.168.1.107:5555
echo.

echo Restarting FireCube device...
M:\platform-tools\adb.exe -s 192.168.1.107:5555 shell reboot
echo.

echo Device restart initiated.
echo Please wait for the device to fully restart.
echo This may take a few minutes.
echo.

echo === Post-Restart Checklist ===
echo After the device restarts:
echo 1. Verify that Kodi is working properly
echo 2. Check that disabled Amazon services remain disabled
echo 3. Install WolfLauncher if desired
echo 4. Set up a VPN for additional privacy
echo.

pause