#!/bin/bash
# Pigeonhole Fleet Deployment Script
# Fire TV Mass Rooting and Configuration System
# Author: Pigeonhole Streaming Architect

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/fleet-config.yaml"
LOG_FILE="${SCRIPT_DIR}/logs/deployment-$(date +%Y%m%d-%H%M%S).log"
BACKUP_DIR="${SCRIPT_DIR}/backups"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${1}" | tee -a "${LOG_FILE}"
}

error() {
    log "${RED}[ERROR]${NC} ${1}"
    exit 1
}

success() {
    log "${GREEN}[SUCCESS]${NC} ${1}"
}

warning() {
    log "${YELLOW}[WARNING]${NC} ${1}"
}

info() {
    log "${BLUE}[INFO]${NC} ${1}"
}

# Check prerequisites
check_prerequisites() {
    info "Checking deployment prerequisites..."
    
    # Check for required tools
    local required_tools=("adb" "fastboot" "python3" "ansible" "curl" "unzip")
    for tool in "${required_tools[@]}"; do
        if ! command -v "$tool" &> /dev/null; then
            error "Required tool '$tool' not found. Please install it first."
        fi
    done
    
    # Check ADB server
    if ! adb start-server &> /dev/null; then
        error "Failed to start ADB server"
    fi
    
    # Check for Surfshark VPN connection
    if ! curl -s --max-time 5 https://my-ip.io/ip | grep -q "Surfshark"; then
        warning "Surfshark VPN not detected. Deployment may be blocked."
    fi
    
    success "Prerequisites check completed"
}

# Device discovery
discover_devices() {
    info "Discovering Fire TV devices on network..."
    
    # ADB device discovery
    adb devices -l | grep -E "(AFTMM|AFTBK|AFTKA|AFTGAZL)" > "${SCRIPT_DIR}/discovered_devices.txt" || true
    
    # Network discovery for Fire TV devices
    nmap -sn 192.168.1.0/24 | grep -B2 -A2 "amazon" >> "${SCRIPT_DIR}/discovered_devices.txt" || true
    
    local device_count=$(wc -l < "${SCRIPT_DIR}/discovered_devices.txt")
    info "Discovered ${device_count} Fire TV devices"
}

# Pre-root backup
create_backup() {
    local device_ip="$1"
    local device_serial="$2"
    
    info "Creating backup for device ${device_serial}..."
    
    local backup_path="${BACKUP_DIR}/${device_serial}-$(date +%Y%m%d-%H%M%S)"
    mkdir -p "$backup_path"
    
    # Backup critical partitions
    adb -s "$device_ip" shell "su -c 'dd if=/dev/block/platform/soc/d0074000.emmc/by-name/boot of=/sdcard/boot.img'"
    adb -s "$device_ip" pull /sdcard/boot.img "$backup_path/"
    
    adb -s "$device_ip" shell "su -c 'dd if=/dev/block/platform/soc/d0074000.emmc/by-name/recovery of=/sdcard/recovery.img'"
    adb -s "$device_ip" pull /sdcard/recovery.img "$backup_path/"
    
    # Backup system configuration
    adb -s "$device_ip" shell pm list packages > "$backup_path/installed_packages.txt"
    adb -s "$device_ip" shell dumpsys > "$backup_path/system_dump.txt"
    
    success "Backup completed for ${device_serial}"
}

# Root device using multiple methods
root_device() {
    local device_ip="$1"
    local device_serial="$2"
    
    info "Starting root process for device ${device_serial}..."
    
    # Method 1: Check if already rooted
    if adb -s "$device_ip" shell "su -c 'id'" &> /dev/null; then
        success "Device ${device_serial} already rooted"
        return 0
    fi
    
    # Method 2: Magisk via custom recovery
    if root_via_magisk "$device_ip" "$device_serial"; then
        return 0
    fi
    
    # Method 3: KingRoot method
    if root_via_kingroot "$device_ip" "$device_serial"; then
        return 0
    fi
    
    # Method 4: Exploit-based rooting
    if root_via_exploit "$device_ip" "$device_serial"; then
        return 0
    fi
    
    error "Failed to root device ${device_serial}"
}

# Magisk rooting method
root_via_magisk() {
    local device_ip="$1"
    local device_serial="$2"
    
    info "Attempting Magisk root for ${device_serial}..."
    
    # Install TWRP recovery
    adb -s "$device_ip" reboot bootloader
    sleep 10
    
    fastboot -s "$device_serial" flash recovery "${SCRIPT_DIR}/tools/twrp-firetv.img"
    fastboot -s "$device_serial" reboot recovery
    sleep 15
    
    # Install Magisk via TWRP
    adb -s "$device_ip" push "${SCRIPT_DIR}/tools/Magisk-v25.2.zip" /tmp/
    adb -s "$device_ip" shell 'echo "install /tmp/Magisk-v25.2.zip" > /tmp/adb-command'
    adb -s "$device_ip" shell 'twrp install /tmp/Magisk-v25.2.zip'
    
    adb -s "$device_ip" reboot
    sleep 30
    
    # Verify root
    if adb -s "$device_ip" shell "su -c 'id'" &> /dev/null; then
        success "Magisk root successful for ${device_serial}"
        return 0
    fi
    
    return 1
}

# KingRoot method
root_via_kingroot() {
    local device_ip="$1"
    local device_serial="$2"
    
    info "Attempting KingRoot method for ${device_serial}..."
    
    # Install KingRoot APK
    adb -s "$device_ip" install "${SCRIPT_DIR}/tools/kingroot.apk"
    
    # Launch KingRoot and attempt automated root
    adb -s "$device_ip" shell am start -n com.kingroot.kinguser/.activitys.SlashActivity
    
    # Wait for rooting process (this requires manual intervention)
    warning "Manual intervention required: Tap 'Root' button in KingRoot app"
    read -p "Press Enter after rooting is complete..."
    
    # Migrate to Magisk
    if adb -s "$device_ip" shell "su -c 'id'" &> /dev/null; then
        migrate_to_magisk "$device_ip" "$device_serial"
        return 0
    fi
    
    return 1
}

# Exploit-based rooting
root_via_exploit() {
    local device_ip="$1"
    local device_serial="$2"
    
    info "Attempting exploit-based root for ${device_serial}..."
    
    # Push exploit binary
    adb -s "$device_ip" push "${SCRIPT_DIR}/tools/mtk-su" /data/local/tmp/
    adb -s "$device_ip" shell chmod 755 /data/local/tmp/mtk-su
    
    # Execute exploit
    adb -s "$device_ip" shell /data/local/tmp/mtk-su
    
    # Install su binary
    if adb -s "$device_ip" shell "ls /system/xbin/su" &> /dev/null; then
        success "Exploit root successful for ${device_serial}"
        return 0
    fi
    
    return 1
}

# Install custom ROM
install_custom_rom() {
    local device_ip="$1"
    local device_serial="$2"
    
    info "Installing Pigeonhole custom ROM on ${device_serial}..."
    
    # Boot to recovery
    adb -s "$device_ip" reboot recovery
    sleep 15
    
    # Wipe system
    adb -s "$device_ip" shell 'twrp wipe system'
    adb -s "$device_ip" shell 'twrp wipe data'
    adb -s "$device_ip" shell 'twrp wipe cache'
    
    # Install custom ROM
    adb -s "$device_ip" push "${SCRIPT_DIR}/roms/pigeonhole-lineageos-firetv.zip" /tmp/
    adb -s "$device_ip" shell 'twrp install /tmp/pigeonhole-lineageos-firetv.zip'
    
    # Install GApps (minimal)
    adb -s "$device_ip" push "${SCRIPT_DIR}/roms/gapps-nano.zip" /tmp/
    adb -s "$device_ip" shell 'twrp install /tmp/gapps-nano.zip'
    
    # Install Magisk
    adb -s "$device_ip" push "${SCRIPT_DIR}/tools/Magisk-v25.2.zip" /tmp/
    adb -s "$device_ip" shell 'twrp install /tmp/Magisk-v25.2.zip'
    
    adb -s "$device_ip" reboot
    sleep 60
    
    success "Custom ROM installation completed for ${device_serial}"
}

# Configure Kodi with addons
configure_kodi() {
    local device_ip="$1"
    local device_serial="$2"
    
    info "Configuring Kodi for ${device_serial}..."
    
    # Wait for system to boot
    sleep 30
    
    # Install Kodi if not present
    if ! adb -s "$device_ip" shell pm list packages | grep -q "org.xbmc.kodi"; then
        adb -s "$device_ip" install "${SCRIPT_DIR}/apps/kodi-20.2-nexus.apk"
    fi
    
    # Push Kodi configuration
    adb -s "$device_ip" push "${SCRIPT_DIR}/kodi-config/" "/storage/emulated/0/Android/data/org.xbmc.kodi/files/.kodi/"
    
    # Install Arctic Zephyr skin
    adb -s "$device_ip" push "${SCRIPT_DIR}/kodi-addons/skin.arctic.zephyr.pigeonhole/" "/storage/emulated/0/Android/data/org.xbmc.kodi/files/.kodi/addons/"
    
    # Install streaming addons
    local addons=("plugin.video.madtitan" "plugin.video.theghost" "plugin.video.tempest" "plugin.video.fen")
    for addon in "${addons[@]}"; do
        adb -s "$device_ip" push "${SCRIPT_DIR}/kodi-addons/${addon}/" "/storage/emulated/0/Android/data/org.xbmc.kodi/files/.kodi/addons/"
    done
    
    # Configure addon settings
    adb -s "$device_ip" push "${SCRIPT_DIR}/kodi-config/addon_data/" "/storage/emulated/0/Android/data/org.xbmc.kodi/files/.kodi/userdata/addon_data/"
    
    success "Kodi configuration completed for ${device_serial}"
}

# Install Surfshark VPN
install_surfshark() {
    local device_ip="$1"
    local device_serial="$2"
    
    info "Installing Surfshark VPN for ${device_serial}..."
    
    # Install Surfshark APK
    adb -s "$device_ip" install "${SCRIPT_DIR}/apps/surfshark-vpn.apk"
    
    # Configure VPN profile (requires manual setup or automation script)
    adb -s "$device_ip" push "${SCRIPT_DIR}/surfshark-config/surfshark.ovpn" "/storage/emulated/0/"
    
    # Setup automatic connection
    adb -s "$device_ip" shell 'settings put secure vpn_auto_connect 1'
    
    success "Surfshark VPN installation completed for ${device_serial}"
}

# Install launcher replacement
install_launcher() {
    local device_ip="$1"
    local device_serial="$2"
    
    info "Installing custom launcher for ${device_serial}..."
    
    # Disable Amazon launcher
    adb -s "$device_ip" shell "su -c 'pm disable-user --user 0 com.amazon.tv.launcher'"
    adb -s "$device_ip" shell "su -c 'pm disable-user --user 0 com.amazon.tv.settings'"
    
    # Install Wolf Launcher
    adb -s "$device_ip" install "${SCRIPT_DIR}/apps/wolf-launcher.apk"
    
    # Set as default launcher
    adb -s "$device_ip" shell "su -c 'pm set-home-activity xyz.wolf.launcher/.MainActivity'"
    
    # Configure launcher settings
    adb -s "$device_ip" push "${SCRIPT_DIR}/launcher-config/wolf-settings.xml" "/storage/emulated/0/"
    
    success "Custom launcher installation completed for ${device_serial}"
}

# Install fleet management agent
install_fleet_agent() {
    local device_ip="$1"
    local device_serial="$2"
    
    info "Installing Pigeonhole fleet agent for ${device_serial}..."
    
    # Install agent APK
    adb -s "$device_ip" install "${SCRIPT_DIR}/apps/pigeonhole-agent.apk"
    
    # Configure agent with device registration
    local config="{
        \"device_id\": \"${device_serial}\",
        \"management_server\": \"https://fleet.pigeonhole.local\",
        \"update_channel\": \"stable\",
        \"reporting_interval\": 300
    }"
    
    echo "$config" | adb -s "$device_ip" shell 'cat > /storage/emulated/0/pigeonhole-agent-config.json'
    
    # Start agent service
    adb -s "$device_ip" shell am startservice -n com.pigeonhole.agent/.AgentService
    
    success "Fleet agent installation completed for ${device_serial}"
}

# Deploy to single device
deploy_device() {
    local device_ip="$1"
    local device_serial="$2"
    
    info "Starting deployment for device ${device_serial} at ${device_ip}"
    
    # Create backup
    if [[ "${SKIP_BACKUP:-false}" != "true" ]]; then
        create_backup "$device_ip" "$device_serial"
    fi
    
    # Root device
    root_device "$device_ip" "$device_serial"
    
    # Install custom ROM (optional)
    if [[ "${INSTALL_ROM:-false}" == "true" ]]; then
        install_custom_rom "$device_ip" "$device_serial"
    fi
    
    # Configure applications
    configure_kodi "$device_ip" "$device_serial"
    install_surfshark "$device_ip" "$device_serial"
    install_launcher "$device_ip" "$device_serial"
    install_fleet_agent "$device_ip" "$device_serial"
    
    # Final reboot
    adb -s "$device_ip" reboot
    
    success "Deployment completed for device ${device_serial}"
}

# Parallel deployment function
deploy_fleet() {
    info "Starting fleet deployment..."
    
    discover_devices
    
    # Read device list
    local pids=()
    while IFS= read -r line; do
        if [[ "$line" =~ ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+):5555.*device ]]; then
            local device_ip="${BASH_REMATCH[1]}:5555"
            local device_serial=$(adb -s "$device_ip" shell getprop ro.serialno | tr -d '\r')
            
            # Deploy in parallel
            deploy_device "$device_ip" "$device_serial" &
            pids+=($!)
            
            # Limit concurrent deployments
            if (( ${#pids[@]} >= 3 )); then
                wait "${pids[0]}"
                pids=("${pids[@]:1}")
            fi
        fi
    done < "${SCRIPT_DIR}/discovered_devices.txt"
    
    # Wait for remaining deployments
    for pid in "${pids[@]}"; do
        wait "$pid"
    done
    
    success "Fleet deployment completed"
}

# Main function
main() {
    echo "=== Pigeonhole Fleet Deployment System ==="
    echo "Fire TV Mass Rooting and Configuration"
    echo "========================================"
    
    # Create necessary directories
    mkdir -p "${SCRIPT_DIR}/logs" "${BACKUP_DIR}"
    
    # Initialize logging
    exec > >(tee -a "$LOG_FILE")
    exec 2>&1
    
    case "${1:-deploy}" in
        "check")
            check_prerequisites
            ;;
        "discover")
            discover_devices
            ;;
        "deploy")
            check_prerequisites
            deploy_fleet
            ;;
        "deploy-single")
            if [[ -z "${2:-}" ]]; then
                error "Usage: $0 deploy-single <device_ip>"
            fi
            check_prerequisites
            deploy_device "$2" "$(adb -s "$2" shell getprop ro.serialno | tr -d '\r')"
            ;;
        "backup")
            if [[ -z "${2:-}" ]]; then
                error "Usage: $0 backup <device_ip>"
            fi
            create_backup "$2" "$(adb -s "$2" shell getprop ro.serialno | tr -d '\r')"
            ;;
        *)
            echo "Usage: $0 {check|discover|deploy|deploy-single|backup} [options]"
            echo ""
            echo "Commands:"
            echo "  check         - Check prerequisites"
            echo "  discover      - Discover Fire TV devices"
            echo "  deploy        - Deploy to all discovered devices"
            echo "  deploy-single - Deploy to single device"
            echo "  backup        - Create backup of single device"
            echo ""
            echo "Environment variables:"
            echo "  SKIP_BACKUP=true    - Skip backup creation"
            echo "  INSTALL_ROM=true    - Install custom ROM"
            exit 1
            ;;
    esac
}

# Execute main function
main "$@"