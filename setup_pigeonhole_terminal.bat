@echo off
title Pigeonhole Streaming Terminal Setup
color 0A

echo.
echo  ========================================================
echo              PIGEONHOLE STREAMING TERMINAL
echo                    Quick Setup Utility
echo  ========================================================
echo.

:: Set environment variables
set PIGEONHOLE_HOME=M:\
set PIGEONHOLE_ADB=M:\platform-tools\adb.exe
set FIRE_TV_CUBE=192.168.1.107:5555

echo [STEP 1] Configuring environment variables...
setx PIGEONHOLE_HOME "M:\" >nul
setx PIGEONHOLE_ADB "M:\platform-tools\adb.exe" >nul
setx FIRE_TV_CUBE "192.168.1.107:5555" >nul
echo   - Environment variables set

echo [STEP 2] Validating ADB installation...
if exist "M:\platform-tools\adb.exe" (
    echo   - ADB found: M:\platform-tools\adb.exe
    M:\platform-tools\adb.exe version
) else (
    echo   - ERROR: ADB not found in platform-tools
    echo   - Please ensure platform-tools directory contains adb.exe
    pause
    exit /b 1
)

echo [STEP 3] Testing device connectivity...
echo   - Attempting to connect to Fire TV Cube...
M:\platform-tools\adb.exe connect %FIRE_TV_CUBE%
timeout /t 2 /nobreak >nul

M:\platform-tools\adb.exe devices | findstr %FIRE_TV_CUBE% >nul
if errorlevel 1 (
    echo   - WARNING: Fire TV Cube not connected
    echo   - Device may be offline or IP incorrect
) else (
    echo   - SUCCESS: Fire TV Cube connected
)

echo [STEP 4] Launching enhanced PowerShell environment...
echo   - Loading Pigeonhole terminal setup...
powershell -NoExit -ExecutionPolicy Bypass -File "M:\PigeonholeTerminalSetup.ps1"

echo.
echo Terminal setup complete!
pause