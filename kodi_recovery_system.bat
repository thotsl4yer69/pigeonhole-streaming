@echo off
echo ================================================
echo KODI RECOVERY AND DIAGNOSTIC SYSTEM
echo Pigeonhole Streaming - Emergency Recovery Tools
echo ================================================

set FIRE_TV_IP=192.168.1.130
set ADB_PATH=M:\platform-tools\adb.exe
set KODI_PACKAGE=org.xbmc.kodi
set KODI_DATA_PATH=/sdcard/Android/data/%KODI_PACKAGE%/files/.kodi

:MAIN_MENU
echo.
echo SELECT RECOVERY OPTION:
echo [1] Quick Crash Recovery
echo [2] Full System Reset
echo [3] Addon Repair
echo [4] Performance Diagnostics
echo [5] Log Analysis
echo [6] Backup Current Setup
echo [7] Restore from Backup
echo [8] Exit
echo.
set /p choice="Enter choice (1-8): "

if "%choice%"=="1" goto CRASH_RECOVERY
if "%choice%"=="2" goto FULL_RESET
if "%choice%"=="3" goto ADDON_REPAIR
if "%choice%"=="4" goto PERFORMANCE_DIAG
if "%choice%"=="5" goto LOG_ANALYSIS
if "%choice%"=="6" goto BACKUP
if "%choice%"=="7" goto RESTORE
if "%choice%"=="8" goto EXIT
goto MAIN_MENU

:CRASH_RECOVERY
echo [CRASH RECOVERY] Performing emergency stabilization...
%ADB_PATH% connect %FIRE_TV_IP%:5555
%ADB_PATH% shell "am force-stop %KODI_PACKAGE%"
timeout /t 3
%ADB_PATH% shell "rm -f %KODI_DATA_PATH%/temp/kodi.log"
%ADB_PATH% shell "rm -rf %KODI_DATA_PATH%/Database/Textures*"
echo Restarting Kodi with crash protection...
%ADB_PATH% shell "am start -n %KODI_PACKAGE%/.Splash"
echo Recovery complete. Monitor for stability.
pause
goto MAIN_MENU

:FULL_RESET
echo [FULL RESET] Performing complete system reset...
%ADB_PATH% connect %FIRE_TV_IP%:5555
%ADB_PATH% shell "am force-stop %KODI_PACKAGE%"
%ADB_PATH% shell "pm clear %KODI_PACKAGE%"
echo System reset complete. Redeploy with stable script.
pause
goto MAIN_MENU

:ADDON_REPAIR
echo [ADDON REPAIR] Checking and repairing addons...
%ADB_PATH% connect %FIRE_TV_IP%:5555
%ADB_PATH% shell "chmod -R 755 %KODI_DATA_PATH%/addons/"
%ADB_PATH% shell "find %KODI_DATA_PATH%/addons/ -name '*.pyo' -delete"
%ADB_PATH% shell "find %KODI_DATA_PATH%/addons/ -name '*.pyc' -delete"
echo Addon repair complete.
pause
goto MAIN_MENU

:PERFORMANCE_DIAG
echo [PERFORMANCE DIAGNOSTICS] Running system analysis...
%ADB_PATH% connect %FIRE_TV_IP%:5555
echo Memory Usage:
%ADB_PATH% shell "free -m"
echo.
echo CPU Load:
%ADB_PATH% shell "top -n 1 | head -5"
echo.
echo Kodi Process:
%ADB_PATH% shell "ps | grep kodi"
echo.
echo Storage Usage:
%ADB_PATH% shell "df -h | grep sdcard"
pause
goto MAIN_MENU

:LOG_ANALYSIS
echo [LOG ANALYSIS] Extracting and analyzing logs...
%ADB_PATH% connect %FIRE_TV_IP%:5555
echo Pulling latest Kodi log...
%ADB_PATH% pull "%KODI_DATA_PATH%/temp/kodi.log" "M:\kodi_debug.log" 2>nul
if exist "M:\kodi_debug.log" (
    echo Log extracted to M:\kodi_debug.log
    echo Checking for crashes...
    findstr /i "crash\|error\|exception\|segv" "M:\kodi_debug.log" > "M:\error_summary.txt"
    if exist "M:\error_summary.txt" (
        echo Error summary created in M:\error_summary.txt
    )
) else (
    echo No log file found or extraction failed
)
pause
goto MAIN_MENU

:BACKUP
echo [BACKUP] Creating configuration backup...
%ADB_PATH% connect %FIRE_TV_IP%:5555
mkdir "M:\backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%" 2>nul
%ADB_PATH% pull "%KODI_DATA_PATH%/userdata/guisettings.xml" "M:\backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%\"
%ADB_PATH% pull "%KODI_DATA_PATH%/userdata/favourites.xml" "M:\backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%\"
%ADB_PATH% pull "%KODI_DATA_PATH%/userdata/advancedsettings.xml" "M:\backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%\"
echo Backup created in M:\backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%\
pause
goto MAIN_MENU

:RESTORE
echo [RESTORE] Restoring from backup...
echo Available backups:
dir "M:\backup_*" /b 2>nul
set /p backup_folder="Enter backup folder name: "
if exist "M:\%backup_folder%" (
    %ADB_PATH% connect %FIRE_TV_IP%:5555
    %ADB_PATH% push "M:\%backup_folder%\guisettings.xml" "%KODI_DATA_PATH%/userdata/"
    %ADB_PATH% push "M:\%backup_folder%\favourites.xml" "%KODI_DATA_PATH%/userdata/"
    %ADB_PATH% push "M:\%backup_folder%\advancedsettings.xml" "%KODI_DATA_PATH%/userdata/"
    echo Restore complete.
) else (
    echo Backup folder not found.
)
pause
goto MAIN_MENU

:EXIT
echo Exiting recovery system...
exit /b 0