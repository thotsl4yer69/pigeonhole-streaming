@echo off
REM FireCube Post-Debloat Checker
REM Checks what packages remain after debloating

echo === FireCube Post-Debloat Checker ===
echo.

REM Connect to device
echo Connecting to FireCube device...
M:\platform-tools\adb.exe connect 192.168.1.107:5555
echo.

echo Getting list of installed packages...
M:\platform-tools\adb.exe -s 192.168.1.107:5555 shell pm list packages > installed_packages.txt
echo.

echo Analyzing packages...

echo ==================== Amazon Packages ==================== 
findstr /i "amazon" installed_packages.txt

echo.
echo ==================== Kodi Packages ==================== 
findstr /i "kodi" installed_packages.txt
findstr /i "xbmc" installed_packages.txt

echo.
echo ==================== Android System Packages ==================== 
findstr /i "com.android" installed_packages.txt

echo.
echo ==================== Other Packages ==================== 
echo Other packages can be found in installed_packages.txt

echo.
echo === Summary ===
echo Amazon packages remaining:
find /c /i "package:" installed_packages.txt | find /c "amazon"
echo Kodi packages:
find /c /i "kodi" installed_packages.txt
find /c /i "xbmc" installed_packages.txt
echo Android system packages:
find /c /i "com.android" installed_packages.txt

echo.
echo Detailed list saved to installed_packages.txt
echo.
pause