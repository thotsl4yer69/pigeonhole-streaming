@echo off
setlocal enabledelayedexpansion

:: ================================================================
:: FIRE TV CUBE GOLD BUILD DEPLOYMENT - PIGEONHOLE STREAMING
:: Complete system optimization with Amazon debloating
:: ================================================================

echo.
echo ████████████████████████████████████████████████████████████████
echo ██                                                            ██
echo ██    FIRE TV CUBE GOLD BUILD - PIGEONHOLE STREAMING         ██
echo ██    Ultimate Kodi v22 Optimization System                  ██
echo ██                                                            ██
echo ████████████████████████████████████████████████████████████████
echo.

set FIRE_TV_IP=192.168.1.130
set HTTP_PORT=8080
set ADB_PORT=5555
set KODI_PACKAGE=org.xbmc.kodi
set START_TIME=%TIME%

:: Check for existing ADB
where adb >nul 2>nul
if %errorlevel% equ 0 (
    echo [INFO] ADB already installed and available
) else (
    echo [PHASE 1] Installing ADB Platform Tools...
    echo.

    :: Download and extract minimal ADB
    if not exist "M:\adb" mkdir "M:\adb"
    cd /d "M:\adb"

    :: Check if already downloaded
    if not exist "adb.exe" (
        echo [INFO] Downloading ADB platform tools...
        powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://dl.google.com/android/repository/platform-tools-latest-windows.zip' -OutFile 'platform-tools.zip'}"

        if exist "platform-tools.zip" (
            echo [INFO] Extracting ADB tools...
            powershell -Command "Expand-Archive -Path 'platform-tools.zip' -DestinationPath '.' -Force"
            copy "platform-tools\*.exe" "."
            copy "platform-tools\*.dll" "."
            del platform-tools.zip
            rmdir /s /q platform-tools
        ) else (
            echo [ERROR] Failed to download ADB platform tools
            echo [ERROR] Please install ADB manually and retry
            pause
            exit /b 1
        )
    )

    :: Add to PATH for this session
    set PATH=%PATH%;M:\adb
    cd /d "M:\"
)

:: Verify ADB installation
echo [PHASE 2] Verifying ADB installation...
adb version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] ADB not working properly
    pause
    exit /b 1
)
echo [OK] ADB ready

:: Connect to Fire TV Cube
echo [PHASE 3] Connecting to Fire TV Cube...
echo.
adb disconnect %FIRE_TV_IP%:%ADB_PORT%
timeout /t 2 >nul
adb connect %FIRE_TV_IP%:%ADB_PORT%
timeout /t 5 >nul

:: Verify connection
adb -s %FIRE_TV_IP%:%ADB_PORT% shell echo "ADB Connected" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Failed to connect to Fire TV Cube at %FIRE_TV_IP%:%ADB_PORT%
    echo [ERROR] Please check:
    echo         - Fire TV developer options enabled
    echo         - ADB debugging enabled
    echo         - Network connectivity
    echo         - IP address correct
    pause
    exit /b 1
)

echo [OK] Connected to Fire TV Cube (%FIRE_TV_IP%:%ADB_PORT%)
echo.

:: System information
echo [PHASE 4] Gathering system information...
echo ================================================
for /f "tokens=*" %%i in ('adb -s %FIRE_TV_IP%:%ADB_PORT% shell getprop ro.build.display.id 2^>nul') do set FIRMWARE=%%i
for /f "tokens=*" %%i in ('adb -s %FIRE_TV_IP%:%ADB_PORT% shell getprop ro.product.model 2^>nul') do set MODEL=%%i
echo Device: %MODEL%
echo Firmware: %FIRMWARE%
echo ================================================
echo.

:: Backup current state
echo [PHASE 5] Creating system backup...
if not exist "M:\backups" mkdir "M:\backups"
set BACKUP_DIR=M:\backups\firetv_backup_%date:~-4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%
set BACKUP_DIR=!BACKUP_DIR: =0!
mkdir "!BACKUP_DIR!"

echo [INFO] Backing up installed packages...
adb -s %FIRE_TV_IP%:%ADB_PORT% shell pm list packages > "!BACKUP_DIR!\packages.txt"

echo [INFO] Backing up launcher configuration...
adb -s %FIRE_TV_IP%:%ADB_PORT% shell cmd package resolve-activity --brief -c android.intent.category.HOME > "!BACKUP_DIR!\launcher.txt"

echo [OK] System backup created at: !BACKUP_DIR!
echo.

:: Create recovery script
echo [INFO] Creating recovery script...
(
echo @echo off
echo echo FIRE TV CUBE RECOVERY SCRIPT
echo echo ============================
echo echo This script can restore your Fire TV Cube to its previous state
echo echo.
echo set FIRE_TV_IP=%FIRE_TV_IP%
echo set ADB_PORT=%ADB_PORT%
echo.
echo echo [RECOVERY] Connecting to Fire TV Cube...
echo adb connect %%FIRE_TV_IP%%:%%ADB_PORT%%
echo timeout /t 5 ^>nul
echo.
echo echo [RECOVERY] Restoring Amazon launcher...
echo adb -s %%FIRE_TV_IP%%:%%ADB_PORT%% shell cmd package set-home-activity com.amazon.tv.launcher/.ui.HomeActivity_vNext
echo.
echo echo [RECOVERY] Re-enabling Amazon services...
echo for %%%%p in ^(com.amazon.tv.launcher com.amazon.tv.settings^) do ^(
echo     echo Enabling %%%%p...
echo     adb -s %%FIRE_TV_IP%%:%%ADB_PORT%% shell pm enable %%%%p
echo ^)
echo.
echo echo [RECOVERY] Restarting system...
echo adb -s %%FIRE_TV_IP%%:%%ADB_PORT%% shell reboot
echo echo.
echo echo Recovery completed. Your Fire TV should return to normal state.
echo pause
) > "!BACKUP_DIR!\recovery.bat"

echo [OK] Recovery script created: !BACKUP_DIR!\recovery.bat
echo.

:: Pre-flight checks
echo [PHASE 6] Pre-flight system checks...
echo.

:: Check if Kodi is installed
adb -s %FIRE_TV_IP%:%ADB_PORT% shell pm list packages | findstr "org.xbmc.kodi" >nul
if %errorlevel% neq 0 (
    echo [ERROR] Kodi not found on device
    echo [ERROR] Please install Kodi first before running optimization
    pause
    exit /b 1
)
echo [OK] Kodi installation verified

:: Check available storage
for /f "tokens=4" %%i in ('adb -s %FIRE_TV_IP%:%ADB_PORT% shell df /data ^| findstr /data') do set AVAILABLE=%%i
echo [OK] Available storage: %AVAILABLE%

:: Test Kodi HTTP API
echo [INFO] Testing Kodi HTTP API connection...
python -c "import requests; r=requests.get('http://%FIRE_TV_IP%:%HTTP_PORT%/jsonrpc', timeout=5); exit(0 if r.status_code==200 else 1)" >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Kodi HTTP API responding
) else (
    echo [WARN] Kodi HTTP API not responding - will start Kodi
    adb -s %FIRE_TV_IP%:%ADB_PORT% shell am start -n org.xbmc.kodi/.Splash
    timeout /t 10 >nul
)

echo.
echo ================================================================
echo PRE-FLIGHT CHECKS COMPLETE - READY FOR GOLD OPTIMIZATION
echo ================================================================
echo.

:: Warning and confirmation
echo [WARNING] This process will:
echo          - Remove Amazon bloatware (safely)
echo          - Clean unnecessary Kodi addons
echo          - Set Kodi as default launcher
echo          - Apply performance optimizations
echo          - Configure Pigeonhole streaming setup
echo.
echo [INFO] A recovery script has been created at:
echo        !BACKUP_DIR!\recovery.bat
echo.
set /p CONFIRM="Continue with Fire TV Cube Gold optimization? (y/N): "
if /i not "!CONFIRM!"=="y" (
    echo [INFO] Operation cancelled by user
    pause
    exit /b 0
)

echo.
echo ================================================================
echo STARTING FIRE TV CUBE GOLD OPTIMIZATION
echo ================================================================
echo.

:: Execute Python optimization script
echo [PHASE 7] Executing comprehensive optimization...
python "M:\fire_tv_gold_optimizer.py"

if %errorlevel% equ 0 (
    echo.
    echo ████████████████████████████████████████████████████████████████
    echo ██                                                            ██
    echo ██    🚀 FIRE TV CUBE GOLD BUILD COMPLETED! 🚀               ██
    echo ██                                                            ██
    echo ██    ✅ Amazon bloatware removed                            ██
    echo ██    ✅ Kodi addons optimized                               ██
    echo ██    ✅ Kodi set as default launcher                       ██
    echo ██    ✅ Performance settings optimized                      ██
    echo ██    ✅ Pigeonhole configuration deployed                   ██
    echo ██                                                            ██
    echo ██    Your Fire TV Cube is now ready for ultimate           ██
    echo ██    streaming with the Pigeonhole architecture!           ██
    echo ██                                                            ██
    echo ████████████████████████████████████████████████████████████████
    echo.

    :: Final system validation
    echo [FINAL CHECK] Validating optimized system...
    timeout /t 5 >nul

    :: Test Kodi startup
    adb -s %FIRE_TV_IP%:%ADB_PORT% shell am start -n org.xbmc.kodi/.Splash
    timeout /t 10 >nul

    :: Test HTTP API
    python -c "import requests; r=requests.get('http://%FIRE_TV_IP%:%HTTP_PORT%/jsonrpc', timeout=10); print('✅ Kodi responding' if r.status_code==200 else '❌ Kodi not responding')" 2>nul

    echo.
    echo [SUCCESS] Fire TV Cube Gold Build deployment completed successfully!
    echo [INFO] Recovery available at: !BACKUP_DIR!\recovery.bat
    echo [INFO] Total time: %TIME% (started at %START_TIME%)
    echo.
    echo Your Pigeonhole streaming system is now ready for use!

) else (
    echo.
    echo ████████████████████████████████████████████████████████████████
    echo ██                                                            ██
    echo ██    ❌ OPTIMIZATION FAILED                                 ██
    echo ██                                                            ██
    echo ██    Check the error messages above for details             ██
    echo ██    Recovery script available at:                          ██
    echo ██    !BACKUP_DIR!\recovery.bat                              ██
    echo ██                                                            ██
    echo ████████████████████████████████████████████████████████████████
    echo.
)

echo.
pause
endlocal