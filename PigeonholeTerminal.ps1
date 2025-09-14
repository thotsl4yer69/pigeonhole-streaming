# Pigeonhole Streaming Terminal - Simple Version
Clear-Host

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "        PIGEONHOLE STREAMING TERMINAL" -ForegroundColor Yellow  
Write-Host "            MZ1312 Development Environment" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

# Set environment variables
$env:PIGEONHOLE_ADB = "M:\platform-tools\adb.exe"
$env:FIRE_TV_CUBE = "192.168.1.107:5555"

# Function to show status
function Show-Status {
    Write-Host "🔧 PIGEONHOLE STATUS" -ForegroundColor Yellow
    Write-Host "-------------------" -ForegroundColor Cyan
    Write-Host "ADB Path: $env:PIGEONHOLE_ADB" -ForegroundColor Green
    Write-Host "Fire TV: $env:FIRE_TV_CUBE" -ForegroundColor Green
    Write-Host ""
    
    if (Test-Path $env:PIGEONHOLE_ADB) {
        Write-Host "✅ ADB Available" -ForegroundColor Green
    } else {
        Write-Host "❌ ADB Not Found" -ForegroundColor Red
    }
    Write-Host ""
}

# Function to connect Fire TV
function Connect-Device {
    Write-Host "🔌 Connecting to Fire TV..." -ForegroundColor Yellow
    & $env:PIGEONHOLE_ADB connect $env:FIRE_TV_CUBE
    Write-Host ""
}

# Function to deploy Pigeonhole
function Deploy-Final {
    Write-Host "🚀 Starting Final Deployment..." -ForegroundColor Yellow
    & "M:\deploy_pigeonhole_final.bat"
}

# Set aliases
Set-Alias status Show-Status
Set-Alias connect Connect-Device  
Set-Alias deploy Deploy-Final

# Show available commands
Write-Host "Available Commands:" -ForegroundColor Green
Write-Host "  status   - Show system status" -ForegroundColor Cyan
Write-Host "  connect  - Connect to Fire TV" -ForegroundColor Cyan
Write-Host "  deploy   - Run final deployment" -ForegroundColor Cyan
Write-Host ""

# Show initial status
Show-Status