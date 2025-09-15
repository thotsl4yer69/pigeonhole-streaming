@echo off
REM Start Simple HTTP Server for Pigeonhole Streaming Repository
REM This will serve the repository files on port 8000

echo === Starting HTTP Server for Pigeonhole Streaming Repository ===
echo Serving files from: M:\pigeonhole-streaming
echo Access URL: http://192.168.1.116:8000
echo To stop the server, press Ctrl+C
echo.

cd /d M:\pigeonhole-streaming
python -m http.server 8000

echo Server stopped.
pause