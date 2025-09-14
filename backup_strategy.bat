@echo off
setlocal enabledelayedexpansion

echo ========================================
echo FIRE TV CUBE COMPREHENSIVE BACKUP
echo Target: 192.168.1.107:5555 (AFTGAZL)
echo ========================================

:: Create backup directory with timestamp
for /f "tokens=1-3 delims=/ " %%a in ('date /t') do set mydate=%%c-%%a-%%b
for /f "tokens=1-2 delims=: " %%a in ('time /t') do set mytime=%%a-%%b
set timestamp=%mydate%_%mytime%
set backup_dir=M:\FireTV_Backup_%timestamp%
mkdir "%backup_dir%"

echo [INFO] Backup directory: %backup_dir%

:: Establish connection
echo [PHASE 1] Establishing ADB connection...
adb connect 192.168.1.107:5555
timeout /t 3

:: System Configuration Backup
echo [PHASE 2] Backing up system configuration...
mkdir "%backup_dir%\system_config"

echo   - Build properties
adb shell getprop > "%backup_dir%\system_config\build_props.txt"

echo   - Package list
adb shell pm list packages -f > "%backup_dir%\system_config\packages.txt"

echo   - Settings database
adb shell settings list system > "%backup_dir%\system_config\settings_system.txt"
adb shell settings list secure > "%backup_dir%\system_config\settings_secure.txt"
adb shell settings list global > "%backup_dir%\system_config\settings_global.txt"

:: Kodi Configuration Backup (CRITICAL)
echo [PHASE 3] Backing up Kodi configuration...
mkdir "%backup_dir%\kodi_config"

echo   - Kodi userdata directory
adb pull /sdcard/Android/data/org.xbmc.kodi/files/.kodi/userdata "%backup_dir%\kodi_config\userdata"

echo   - Kodi addons
adb pull /sdcard/Android/data/org.xbmc.kodi/files/.kodi/addons "%backup_dir%\kodi_config\addons"

echo   - Kodi addon_data (settings)
adb pull /sdcard/Android/data/org.xbmc.kodi/files/.kodi/userdata/addon_data "%backup_dir%\kodi_config\addon_data"

echo   - Pigeonhole branding assets
adb pull /sdcard/Android/data/org.xbmc.kodi/files/.kodi/userdata/addon_data/skin.confluence/backgrounds "%backup_dir%\kodi_config\pigeonhole_assets" 2>nul
adb pull /sdcard/Android/data/org.xbmc.kodi/files/.kodi/media "%backup_dir%\kodi_config\media_assets" 2>nul

:: VPN Configuration Backup
echo [PHASE 4] Backing up VPN configuration...
mkdir "%backup_dir%\vpn_config"

echo   - Surfshark app data
adb pull /sdcard/Android/data/com.surfshark.vpnclient.android "%backup_dir%\vpn_config\surfshark" 2>nul

echo   - OpenVPN profiles (if any)
adb pull /sdcard/openvpn "%backup_dir%\vpn_config\openvpn" 2>nul

:: Application APKs (Critical Apps)
echo [PHASE 5] Backing up critical application APKs...
mkdir "%backup_dir%\apks"

echo   - Kodi APK
for /f "tokens=2 delims=:" %%a in ('adb shell pm path org.xbmc.kodi') do (
    adb pull %%a "%backup_dir%\apks\kodi.apk"
)

echo   - Surfshark VPN APK
for /f "tokens=2 delims=:" %%a in ('adb shell pm path com.surfshark.vpnclient.android') do (
    adb pull %%a "%backup_dir%\apks\surfshark.apk"
) 2>nul

:: System Partition Images (Advanced)
echo [PHASE 6] Attempting system partition backup...
mkdir "%backup_dir%\partitions"

echo   - Boot partition
adb shell "su -c 'dd if=/dev/block/boot of=/sdcard/boot.img'" 2>nul
adb pull /sdcard/boot.img "%backup_dir%\partitions\boot.img" 2>nul
adb shell rm /sdcard/boot.img 2>nul

echo   - Recovery partition
adb shell "su -c 'dd if=/dev/block/recovery of=/sdcard/recovery.img'" 2>nul
adb pull /sdcard/recovery.img "%backup_dir%\partitions\recovery.img" 2>nul
adb shell rm /sdcard/recovery.img 2>nul

:: Full device info dump
echo [PHASE 7] Creating device information dump...
adb shell dumpsys > "%backup_dir%\system_config\dumpsys_full.txt"

:: Create restoration script
echo [PHASE 8] Creating restoration script...
(
echo @echo off
echo echo FIRE TV CUBE RESTORATION SCRIPT
echo echo Generated: %date% %time%
echo echo.
echo echo WARNING: Only use this script on the SAME device model
echo echo Target: Fire TV Cube 3rd Gen ^(AFTGAZL^)
echo echo.
echo pause
echo.
echo adb connect 192.168.1.107:5555
echo timeout /t 3
echo.
echo echo Restoring Kodi configuration...
echo adb push "userdata" /sdcard/Android/data/org.xbmc.kodi/files/.kodi/userdata
echo adb push "addons" /sdcard/Android/data/org.xbmc.kodi/files/.kodi/addons
echo adb push "addon_data" /sdcard/Android/data/org.xbmc.kodi/files/.kodi/userdata/addon_data
echo.
echo echo Installing critical APKs...
echo adb install -r kodi.apk
echo adb install -r surfshark.apk
echo.
echo echo Restoration complete
echo pause
) > "%backup_dir%\RESTORE.bat"

echo ========================================
echo BACKUP COMPLETE
echo Location: %backup_dir%
echo ========================================
echo.
echo CRITICAL FILES BACKED UP:
echo - Kodi configuration and addons
echo - VPN settings
echo - System configuration
echo - Application APKs
echo - Partition images ^(if root available^)
echo.
echo Use RESTORE.bat to restore configuration
echo ========================================
pause