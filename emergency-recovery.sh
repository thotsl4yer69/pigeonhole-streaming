#!/bin/bash
# Pigeonhole Emergency Recovery System
# Fire TV Unbrick and Recovery Tool

set -euo pipefail

# Configuration
RECOVERY_DIR="/opt/pigeonhole/recovery"
BACKUP_DIR="/opt/pigeonhole/backups"
FASTBOOT_DIR="/opt/pigeonhole/fastboot-images"
LOG_FILE="/var/log/pigeonhole/recovery-$(date +%Y%m%d-%H%M%S).log"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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

# Check if device is in fastboot mode
check_fastboot_mode() {
    local device_serial="$1"
    
    if fastboot devices | grep -q "$device_serial"; then
        return 0
    else
        return 1
    fi
}

# Enter fastboot mode
enter_fastboot_mode() {
    local device_ip="$1"
    
    info "Attempting to enter fastboot mode..."
    
    # Method 1: ADB reboot bootloader
    if adb devices | grep -q "$device_ip"; then
        adb -s "$device_ip" reboot bootloader
        sleep 10
        return 0
    fi
    
    # Method 2: Hardware button combination
    warning "ADB not available. Use hardware method:"
    echo "1. Unplug Fire TV power cable"
    echo "2. Hold SELECT + PLAY/PAUSE buttons"
    echo "3. Plug in power cable while holding buttons"
    echo "4. Hold for 10 seconds until Amazon logo appears"
    read -p "Press Enter when in fastboot mode..."
    
    return 0
}

# Flash stock firmware
flash_stock_firmware() {
    local device_serial="$1"
    local firmware_path="$2"
    
    info "Flashing stock firmware for device ${device_serial}..."
    
    if [[ ! -f "$firmware_path" ]]; then
        error "Firmware file not found: $firmware_path"
    fi
    
    # Extract firmware if needed
    if [[ "$firmware_path" == *.zip ]]; then
        local extract_dir="/tmp/firmware-${device_serial}"
        mkdir -p "$extract_dir"
        unzip -q "$firmware_path" -d "$extract_dir"
        firmware_path="$extract_dir"
    fi
    
    # Flash critical partitions
    fastboot -s "$device_serial" flash bootloader "${firmware_path}/bootloader.img"
    fastboot -s "$device_serial" flash boot "${firmware_path}/boot.img"
    fastboot -s "$device_serial" flash recovery "${firmware_path}/recovery.img"
    fastboot -s "$device_serial" flash system "${firmware_path}/system.img"
    fastboot -s "$device_serial" flash userdata "${firmware_path}/userdata.img"
    
    # Reboot to system
    fastboot -s "$device_serial" reboot
    
    success "Stock firmware flash completed"
}

# Restore from backup
restore_from_backup() {
    local device_serial="$1"
    local backup_path="$2"
    
    info "Restoring device ${device_serial} from backup..."
    
    if [[ ! -d "$backup_path" ]]; then
        error "Backup directory not found: $backup_path"
    fi
    
    # Flash boot partition
    if [[ -f "${backup_path}/boot.img" ]]; then
        fastboot -s "$device_serial" flash boot "${backup_path}/boot.img"
        success "Boot partition restored"
    fi
    
    # Flash recovery partition
    if [[ -f "${backup_path}/recovery.img" ]]; then
        fastboot -s "$device_serial" flash recovery "${backup_path}/recovery.img"
        success "Recovery partition restored"
    fi
    
    # Reboot to recovery for system restore
    fastboot -s "$device_serial" reboot recovery
    sleep 15
    
    # Wait for ADB in recovery
    adb wait-for-recovery
    
    # Restore userdata if available
    if [[ -f "${backup_path}/userdata.tar.gz" ]]; then
        adb push "${backup_path}/userdata.tar.gz" /tmp/
        adb shell "cd /data && tar -xzf /tmp/userdata.tar.gz"
        success "User data restored"
    fi
    
    # Reboot to system
    adb reboot
    
    success "Backup restoration completed"
}

# Fix bootloop
fix_bootloop() {
    local device_serial="$1"
    
    info "Attempting to fix bootloop for device ${device_serial}..."
    
    # Enter fastboot mode
    if ! check_fastboot_mode "$device_serial"; then
        warning "Device not in fastboot mode. Attempting to enter..."
        enter_fastboot_mode "unknown"
    fi
    
    # Clear cache and userdata
    info "Clearing cache and userdata..."
    fastboot -s "$device_serial" erase cache
    fastboot -s "$device_serial" erase userdata
    
    # Flash minimal recovery
    if [[ -f "${FASTBOOT_DIR}/minimal-recovery.img" ]]; then
        fastboot -s "$device_serial" flash recovery "${FASTBOOT_DIR}/minimal-recovery.img"
    fi
    
    # Reboot
    fastboot -s "$device_serial" reboot
    
    info "Bootloop fix attempt completed. Device should boot normally."
}

# Emergency ADB over WiFi setup
setup_adb_wifi() {
    local device_ip="$1"
    
    info "Setting up ADB over WiFi for device ${device_ip}..."
    
    # Enable ADB over TCP
    adb -s "$device_ip" tcpip 5555
    
    # Connect via WiFi
    adb connect "${device_ip}:5555"
    
    # Verify connection
    if adb devices | grep -q "${device_ip}:5555"; then
        success "ADB over WiFi enabled for ${device_ip}"
    else
        error "Failed to enable ADB over WiFi"
    fi
}

# Download stock firmware
download_stock_firmware() {
    local model="$1"
    local version="$2"
    
    info "Downloading stock firmware for ${model} version ${version}..."
    
    local firmware_url=""
    case "$model" in
        "AFTGAZL")  # Fire TV Cube 3rd Gen
            firmware_url="https://fireos-tablet-src.s3.amazonaws.com/AFTGAZL_${version}_stock.zip"
            ;;
        "AFTBKA")   # Fire TV Stick 4K Max
            firmware_url="https://fireos-tablet-src.s3.amazonaws.com/AFTBKA_${version}_stock.zip"
            ;;
        *)
            error "Unknown device model: $model"
            ;;
    esac
    
    local firmware_file="${FASTBOOT_DIR}/${model}_${version}_stock.zip"
    
    if [[ ! -f "$firmware_file" ]]; then
        wget -O "$firmware_file" "$firmware_url" || error "Failed to download firmware"
        success "Firmware downloaded: $firmware_file"
    else
        info "Firmware already exists: $firmware_file"
    fi
    
    echo "$firmware_file"
}

# Device health check
device_health_check() {
    local device_ip="$1"
    
    info "Performing health check for device ${device_ip}..."
    
    # Check ADB connectivity
    if ! adb devices | grep -q "$device_ip"; then
        error "Device not accessible via ADB"
    fi
    
    # Check system properties
    local model=$(adb -s "$device_ip" shell getprop ro.product.model | tr -d '\r')
    local android_version=$(adb -s "$device_ip" shell getprop ro.build.version.release | tr -d '\r')
    local serial=$(adb -s "$device_ip" shell getprop ro.serialno | tr -d '\r')
    
    info "Device Model: $model"
    info "Android Version: $android_version"
    info "Serial Number: $serial"
    
    # Check root status
    if adb -s "$device_ip" shell "su -c 'id'" &> /dev/null; then
        success "Root access: Available"
    else
        warning "Root access: Not available"
    fi
    
    # Check storage space
    local storage_info=$(adb -s "$device_ip" shell df /data | tail -n 1)
    local storage_used=$(echo "$storage_info" | awk '{print $5}' | tr -d '%')
    
    if (( storage_used > 90 )); then
        warning "Storage usage high: ${storage_used}%"
    else
        info "Storage usage: ${storage_used}%"
    fi
    
    # Check CPU temperature
    local temp_files=(
        "/sys/class/thermal/thermal_zone0/temp"
        "/sys/devices/system/cpu/cpu0/cpufreq/cpu_temp"
        "/sys/class/hwmon/hwmon0/temp1_input"
    )
    
    for temp_file in "${temp_files[@]}"; do
        if adb -s "$device_ip" shell "test -f $temp_file" &> /dev/null; then
            local temp=$(adb -s "$device_ip" shell cat "$temp_file" | tr -d '\r')
            # Convert millidegrees to degrees if needed
            if (( temp > 1000 )); then
                temp=$((temp / 1000))
            fi
            info "CPU Temperature: ${temp}°C"
            break
        fi
    done
    
    # Check running processes
    local kodi_running=$(adb -s "$device_ip" shell "ps | grep kodi" | wc -l)
    local surfshark_running=$(adb -s "$device_ip" shell "ps | grep surfshark" | wc -l)
    
    info "Kodi processes: $kodi_running"
    info "Surfshark processes: $surfshark_running"
    
    success "Health check completed"
}

# Create recovery image
create_recovery_image() {
    local device_ip="$1"
    local output_path="$2"
    
    info "Creating recovery image for device ${device_ip}..."
    
    # Get device info
    local serial=$(adb -s "$device_ip" shell getprop ro.serialno | tr -d '\r')
    local model=$(adb -s "$device_ip" shell getprop ro.product.model | tr -d '\r')
    
    local recovery_dir="${output_path}/${serial}-recovery-$(date +%Y%m%d-%H%M%S)"
    mkdir -p "$recovery_dir"
    
    # Dump critical partitions
    info "Dumping boot partition..."
    adb -s "$device_ip" shell "su -c 'dd if=/dev/block/platform/*/by-name/boot of=/sdcard/boot.img'"
    adb -s "$device_ip" pull /sdcard/boot.img "$recovery_dir/"
    
    info "Dumping recovery partition..."
    adb -s "$device_ip" shell "su -c 'dd if=/dev/block/platform/*/by-name/recovery of=/sdcard/recovery.img'"
    adb -s "$device_ip" pull /sdcard/recovery.img "$recovery_dir/"
    
    # Create system backup
    info "Creating system configuration backup..."
    adb -s "$device_ip" shell pm list packages > "$recovery_dir/installed_packages.txt"
    adb -s "$device_ip" shell dumpsys > "$recovery_dir/system_dump.txt"
    
    # Backup Kodi configuration
    if adb -s "$device_ip" shell "test -d /storage/emulated/0/Android/data/org.xbmc.kodi" &> /dev/null; then
        info "Backing up Kodi configuration..."
        adb -s "$device_ip" shell "cd /storage/emulated/0/Android/data/org.xbmc.kodi && tar -czf /sdcard/kodi-backup.tar.gz files/"
        adb -s "$device_ip" pull /sdcard/kodi-backup.tar.gz "$recovery_dir/"
    fi
    
    # Create recovery script
    cat > "$recovery_dir/recovery-script.sh" << EOF
#!/bin/bash
# Auto-generated recovery script for $serial ($model)
# Created: $(date)

DEVICE_IP="\$1"
SCRIPT_DIR="\$(dirname "\$0")"

echo "Starting recovery for device $serial..."

# Flash boot partition
fastboot -s "$serial" flash boot "\$SCRIPT_DIR/boot.img"

# Flash recovery partition  
fastboot -s "$serial" flash recovery "\$SCRIPT_DIR/recovery.img"

# Reboot to recovery
fastboot -s "$serial" reboot recovery
sleep 15

# Restore Kodi if backup exists
if [[ -f "\$SCRIPT_DIR/kodi-backup.tar.gz" ]]; then
    adb -s "\$DEVICE_IP" push "\$SCRIPT_DIR/kodi-backup.tar.gz" /tmp/
    adb -s "\$DEVICE_IP" shell "cd /storage/emulated/0/Android/data/org.xbmc.kodi && tar -xzf /tmp/kodi-backup.tar.gz"
fi

# Reboot to system
adb -s "\$DEVICE_IP" reboot

echo "Recovery completed for device $serial"
EOF

    chmod +x "$recovery_dir/recovery-script.sh"
    
    success "Recovery image created: $recovery_dir"
    echo "$recovery_dir"
}

# Main recovery function
main() {
    echo "=== Pigeonhole Emergency Recovery System ==="
    echo "Fire TV Unbrick and Recovery Tool"
    echo "=================================="
    
    case "${1:-help}" in
        "health")
            if [[ -z "${2:-}" ]]; then
                error "Usage: $0 health <device_ip>"
            fi
            device_health_check "$2"
            ;;
        "bootloop")
            if [[ -z "${2:-}" ]]; then
                error "Usage: $0 bootloop <device_serial>"
            fi
            fix_bootloop "$2"
            ;;
        "restore")
            if [[ -z "${2:-}" ]] || [[ -z "${3:-}" ]]; then
                error "Usage: $0 restore <device_serial> <backup_path>"
            fi
            restore_from_backup "$2" "$3"
            ;;
        "flash")
            if [[ -z "${2:-}" ]] || [[ -z "${3:-}" ]]; then
                error "Usage: $0 flash <device_serial> <firmware_path>"
            fi
            flash_stock_firmware "$2" "$3"
            ;;
        "download")
            if [[ -z "${2:-}" ]] || [[ -z "${3:-}" ]]; then
                error "Usage: $0 download <model> <version>"
            fi
            download_stock_firmware "$2" "$3"
            ;;
        "backup")
            if [[ -z "${2:-}" ]]; then
                error "Usage: $0 backup <device_ip> [output_path]"
            fi
            create_recovery_image "$2" "${3:-$BACKUP_DIR}"
            ;;
        "adb-wifi")
            if [[ -z "${2:-}" ]]; then
                error "Usage: $0 adb-wifi <device_ip>"
            fi
            setup_adb_wifi "$2"
            ;;
        *)
            echo "Usage: $0 {health|bootloop|restore|flash|download|backup|adb-wifi} [options]"
            echo ""
            echo "Commands:"
            echo "  health <device_ip>                    - Perform device health check"
            echo "  bootloop <device_serial>              - Fix bootloop issues"
            echo "  restore <device_serial> <backup_path> - Restore from backup"
            echo "  flash <device_serial> <firmware_path> - Flash stock firmware"
            echo "  download <model> <version>            - Download stock firmware"
            echo "  backup <device_ip> [output_path]      - Create recovery backup"
            echo "  adb-wifi <device_ip>                  - Setup ADB over WiFi"
            echo ""
            echo "Examples:"
            echo "  $0 health 192.168.1.100:5555"
            echo "  $0 bootloop G000AB123456"
            echo "  $0 restore G000AB123456 /opt/pigeonhole/backups/G000AB123456"
            echo "  $0 download AFTGAZL 7.2.2.3"
            exit 1
            ;;
    esac
}

# Execute main function
main "$@"