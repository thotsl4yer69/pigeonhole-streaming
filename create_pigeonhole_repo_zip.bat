@echo off
REM Create Proper Pigeonhole Streaming Repository ZIP for Installation
REM This creates a properly structured repository ZIP file for Kodi installation

echo === Creating Pigeonhole Streaming Repository ZIP ===
echo.

REM Create temporary directory for repository packaging
mkdir M:\temp_repo_packaging
mkdir M:\temp_repo_packaging\repository.pigeonhole.streaming

REM Copy repository files
xcopy /E /I M:\pigeonhole-streaming\repository.pigeonhole.streaming M:\temp_repo_packaging\repository.pigeonhole.streaming

REM Create addons.xml file if it doesn't exist
if not exist M:\temp_repo_packaging\repository.pigeonhole.streaming\addons.xml (
    echo ^<?xml version="1.0" encoding="UTF-8" standalone="yes"?^> > M:\temp_repo_packaging\repository.pigeonhole.streaming\addons.xml
    echo ^<addons^> >> M:\temp_repo_packaging\repository.pigeonhole.streaming\addons.xml
    echo ^</addons^> >> M:\temp_repo_packaging\repository.pigeonhole.streaming\addons.xml
)

REM Create MD5 checksum for addons.xml
if exist M:\temp_repo_packaging\repository.pigeonhole.streaming\addons.xml (
    certutil -hashfile M:\temp_repo_packaging\repository.pigeonhole.streaming\addons.xml MD5 | findstr /V "hash" | findstr /V "CertUtil" > M:\temp_repo_packaging\repository.pigeonhole.streaming\addons.xml.md5
)

REM Create the ZIP file
cd /d M:\temp_repo_packaging
tar -a -c -f M:\pigeonhole-streaming-repository.zip repository.pigeonhole.streaming

REM Clean up temporary files
rmdir /S /Q M:\temp_repo_packaging

echo Repository ZIP created: M:\pigeonhole-streaming-repository.zip
echo.

echo === Installation Instructions ===
echo 1. Transfer M:\pigeonhole-streaming-repository.zip to your FireCube device
echo 2. In Kodi, go to Settings ^> Add-ons ^> Install from zip file
echo 3. Navigate to where you saved the ZIP file
echo 4. Select pigeonhole-streaming-repository.zip to install
echo 5. After installation, go to Install from repository
echo 6. Select Pigeonhole Streaming Repository
echo 7. Install addons from there
echo.

pause