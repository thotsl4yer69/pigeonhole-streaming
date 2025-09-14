@echo off
echo =====================================
echo FIRE TV CUBE 3RD GEN RECONNAISSANCE
echo Target: 192.168.1.130:5555 (AFTGAZL)
echo =====================================

:: Establish ADB connection
echo [PHASE 1] Establishing ADB connection...
adb connect 192.168.1.130:5555
timeout /t 3

:: Critical System Information
echo [PHASE 2] Gathering critical system intelligence...
echo.
echo === FIRMWARE VERSION ===
adb shell getprop ro.build.version.release
adb shell getprop ro.build.version.sdk
adb shell getprop ro.build.display.id
adb shell getprop ro.build.fingerprint

echo.
echo === DEVICE SPECIFICATIONS ===
adb shell getprop ro.product.model
adb shell getprop ro.product.device
adb shell getprop ro.hardware
adb shell getprop ro.board.platform

echo.
echo === BOOTLOADER STATUS ===
adb shell getprop ro.boot.verifiedbootstate
adb shell getprop ro.boot.flash.locked
adb shell getprop ro.boot.veritymode
adb shell getprop ro.debuggable

echo.
echo === SECURITY PATCH LEVEL ===
adb shell getprop ro.build.version.security_patch
adb shell getprop ro.boot.warranty_bit
adb shell getprop ro.warranty_bit

echo.
echo === EXPLOIT ASSESSMENT DATA ===
adb shell getprop ro.build.version.incremental
adb shell getprop ro.build.date
adb shell getprop ro.build.tags
adb shell getprop ro.build.type

echo.
echo === KERNEL VERSION ===
adb shell cat /proc/version

echo.
echo === PARTITION LAYOUT ===
adb shell cat /proc/partitions

echo.
echo === MOUNT POINTS ===
adb shell mount | grep -E "(system|boot|recovery|data)"

echo.
echo === ROOT CHECK ===
adb shell su -c "id" 2>nul
if %errorlevel%==0 (
    echo [INFO] Device appears to have root access
) else (
    echo [INFO] Device does not have root access
)

echo.
echo === INSTALLED PACKAGES (Critical) ===
adb shell pm list packages | findstr -i "kodi\|amazon\|launcher\|root\|magisk\|supersu"

echo =====================================
echo RECONNAISSANCE COMPLETE
echo =====================================
pause