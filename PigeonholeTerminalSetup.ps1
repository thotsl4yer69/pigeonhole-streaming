# Pigeonhole Streaming Terminal Setup
# Professional development environment for Fire TV deployment

# Set console title and colors
$Host.UI.RawUI.WindowTitle = "Pigeonhole Streaming - MZ1312 Development Environment"

# Clear and show banner
Clear-Host
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "        PIGEONHOLE STREAMING TERMINAL SETUP" -ForegroundColor Yellow
Write-Host "            MZ1312 Development Environment" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

# Environment Variables
$env:PIGEONHOLE_HOME = "M:\"
$env:PIGEONHOLE_ADB = "M:\platform-tools\adb.exe"
$env:FIRE_TV_CUBE = "192.168.1.107:5555"
$env:PIGEONHOLE_CONFIG = "M:\config"

# Pigeonhole Streaming Functions
function Show-PigeonholeStatus {
    Write-Host "🔧 PIGEONHOLE STREAMING STATUS" -ForegroundColor Yellow
    Write-Host "--------------------------------" -ForegroundColor Cyan
    Write-Host "Home Directory: $env:PIGEONHOLE_HOME" -ForegroundColor Green
    Write-Host "ADB Path: $env:PIGEONHOLE_ADB" -ForegroundColor Green
    Write-Host "Fire TV Cube: $env:FIRE_TV_CUBE" -ForegroundColor Green
    Write-Host "Config Path: $env:PIGEONHOLE_CONFIG" -ForegroundColor Green
    Write-Host ""
    
    # Check ADB connectivity
    Write-Host "🎯 Device Connectivity:" -ForegroundColor Yellow
    try {
        $devices = & "$env:PIGEONHOLE_ADB" devices
        if ($devices -match $env:FIRE_TV_CUBE) {
            Write-Host "✅ Fire TV Cube Connected" -ForegroundColor Green
        } else {
            Write-Host "❌ Fire TV Cube Disconnected" -ForegroundColor Red
            Write-Host "Run: Connect-FireTV to establish connection" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "❌ ADB Not Available" -ForegroundColor Red
    }
    Write-Host ""
}

function Connect-FireTV {
    param(
        [string]$DeviceIP = $env:FIRE_TV_CUBE
    )
    
    Write-Host "🔌 Connecting to Fire TV: $DeviceIP" -ForegroundColor Yellow
    & "$env:PIGEONHOLE_ADB" connect $DeviceIP
    
    Start-Sleep -Seconds 2
    $devices = & "$env:PIGEONHOLE_ADB" devices
    if ($devices -match $DeviceIP) {
        Write-Host "✅ Connection Successful!" -ForegroundColor Green
    } else {
        Write-Host "❌ Connection Failed!" -ForegroundColor Red
    }
}

function Deploy-Pigeonhole {
    param(
        [switch]$Final,
        [switch]$Fleet,
        [string]$Target = $env:FIRE_TV_CUBE
    )
    
    Write-Host "🚀 Starting Pigeonhole Deployment" -ForegroundColor Yellow
    
    if ($Final) {
        Write-Host "📦 Using Final Deployment Script" -ForegroundColor Cyan
        & "M:\deploy_pigeonhole_final.bat"
    } elseif ($Fleet) {
        Write-Host "🌐 Using Fleet Deployment Script" -ForegroundColor Cyan
        bash "M:\pigeonhole-fleet-deploy.sh"
    } else {
        Write-Host "🎯 Quick Deployment to $Target" -ForegroundColor Cyan
        Connect-FireTV $Target
        & "$env:PIGEONHOLE_ADB" -s $Target shell "am force-stop org.xbmc.kodi"
        & "$env:PIGEONHOLE_ADB" -s $Target shell "am start -n org.xbmc.kodi/.Splash"
        Write-Host "✅ Kodi Restarted" -ForegroundColor Green
    }
}

function Get-FireTVInfo {
    param(
        [string]$DeviceIP = $env:FIRE_TV_CUBE
    )
    
    Write-Host "📱 Fire TV Device Information" -ForegroundColor Yellow
    Write-Host "-----------------------------" -ForegroundColor Cyan
    
    try {
        $model = & "$env:PIGEONHOLE_ADB" -s $DeviceIP shell "getprop ro.product.model"
        $serial = & "$env:PIGEONHOLE_ADB" -s $DeviceIP shell "getprop ro.serialno"
        $version = & "$env:PIGEONHOLE_ADB" -s $DeviceIP shell "getprop ro.build.version.release"
        
        Write-Host "Model: $model" -ForegroundColor Green
        Write-Host "Serial: $serial" -ForegroundColor Green
        Write-Host "Android Version: $version" -ForegroundColor Green
        
        # Check Kodi status
        $kodi = & "$env:PIGEONHOLE_ADB" -s $DeviceIP shell "pm list packages | grep kodi"
        if ($kodi) {
            Write-Host "✅ Kodi Installed" -ForegroundColor Green
        } else {
            Write-Host "❌ Kodi Not Found" -ForegroundColor Red
        }
        
    } catch {
        Write-Host "❌ Cannot retrieve device info - check connection" -ForegroundColor Red
    }
}

function Show-PigeonholeCommands {
    Write-Host "🎯 PIGEONHOLE STREAMING COMMANDS" -ForegroundColor Yellow
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Connection and Status:" -ForegroundColor Green
    Write-Host "  Show-PigeonholeStatus    - Display environment status"
    Write-Host "  Connect-FireTV          - Connect to Fire TV Cube"
    Write-Host "  Get-FireTVInfo          - Show device information"
    Write-Host ""
    Write-Host "Deployment:" -ForegroundColor Green
    Write-Host "  Deploy-Pigeonhole       - Quick deployment"
    Write-Host "  Deploy-Pigeonhole -Final - Full deployment script"
    Write-Host "  Deploy-Pigeonhole -Fleet - Fleet deployment"
    Write-Host ""
    Write-Host "Aliases:" -ForegroundColor Green
    Write-Host "  phs     - Show-PigeonholeStatus"
    Write-Host "  phc     - Connect-FireTV"
    Write-Host "  phd     - Deploy-Pigeonhole"
    Write-Host "  phi     - Get-FireTVInfo"
    Write-Host ""
}

# Create Aliases
Set-Alias -Name phs -Value Show-PigeonholeStatus
Set-Alias -Name phc -Value Connect-FireTV
Set-Alias -Name phd -Value Deploy-Pigeonhole
Set-Alias -Name phi -Value Get-FireTVInfo

# Navigation Shortcuts
function Set-PigeonholeLocation { Set-Location "M:\" }
function Set-RepoLocation { Set-Location "M:\pigeonhole-repo" }
Set-Alias -Name ph -Value Set-PigeonholeLocation
Set-Alias -Name repo -Value Set-RepoLocation

# Startup Actions
Show-PigeonholeCommands
Show-PigeonholeStatus

Write-Host "🎉 Pigeonhole Streaming Terminal Ready!" -ForegroundColor Green
Write-Host "Type Show-PigeonholeCommands for help" -ForegroundColor Yellow
Write-Host ""