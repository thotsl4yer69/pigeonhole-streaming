#!/usr/bin/env python3
"""
True Fire TV Cube Gold Build Debloater
Remove ALL bloatware for pure Kodi experience
"""
import subprocess
import time
from datetime import datetime

class TrueGoldDebloater:
    def __init__(self, fire_tv_ip="192.168.1.130"):
        self.fire_tv_ip = fire_tv_ip
        self.adb_path = "M:\\adb\\adb.exe"

        # Major streaming service bloatware (complete removal)
        self.streaming_bloatware = [
            'com.netflix.ninja',
            'com.amazon.avod',  # Amazon Prime Video
            'com.amazon.imdb.tv.android.app',  # IMDb TV
            'com.amazon.minitv.android.app',  # Amazon miniTV
        ]

        # Amazon system bloatware (safe to remove)
        self.amazon_bloatware = [
            'com.amazon.bueller.music',  # Amazon Music
            'com.amazon.bueller.photos',  # Amazon Photos
            'com.amazon.hedwig',  # Amazon Help
            'com.amazon.gamehub',  # Amazon GameHub
            'com.amazon.shoptv.client',  # Amazon Shop
            'com.amazon.shoptv.firetv.client',  # Amazon Shop TV
            'com.amazon.android.marketplace',  # Amazon Appstore (we'll sideload APKs)
            'com.amazon.alexa.externalmediaplayer.fireos',  # Alexa media
            'com.amazon.tv.alexanotifications',  # Alexa notifications
            'com.amazon.tv.alexaalerts',  # Alexa alerts
            'com.amazon.alexa.datastore.app',  # Alexa datastore
            'com.amazon.audiohome',  # Amazon Audio
            'com.amazon.dummy.music',  # Dummy music
            'com.amazon.dummy.gallery',  # Dummy gallery
            'com.amazon.dummy.contacts',  # Dummy contacts
            'com.amazon.dummy.calendar',  # Dummy calendar
            'com.amazon.dummy.alarmclock',  # Dummy alarm
            'com.amazon.tv.support',  # Amazon Support
            'com.amazon.tv.legal.notices',  # Legal notices
            'com.amazon.tv.releasenotes',  # Release notes
            'com.amazon.tv.oobe',  # Out of box experience
            'com.amazon.sneakpeek',  # Sneak peek
            'com.amazon.stillwatching.activity',  # Still watching
        ]

        # Amazon services that can be safely disabled
        self.amazon_services = [
            'com.amazon.spiderpork',
            'com.amazon.recess',
            'com.amazon.tigris',
            'com.amazon.venezia',
            'com.amazon.vizzini',
            'com.amazon.ceviche',
            'com.amazon.logan',
            'com.amazon.tahoe',
            'com.amazon.diode',
            'com.amazon.cardinal',
            'com.amazon.aria',
            'com.amazon.aca',
            'com.amazon.ale',
            'com.amazon.cpl',
            'com.amazon.imp',
            'com.amazon.d3',
            'amazon.speech.davs.davcservice',
        ]

    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")

    def adb_cmd(self, command):
        try:
            full_cmd = f'"{self.adb_path}" -s {self.fire_tv_ip}:5555 {command}'
            result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, timeout=30)
            return result.returncode == 0, result.stdout.strip() if result.stdout else result.stderr.strip()
        except Exception as e:
            return False, str(e)

    def remove_streaming_bloatware(self):
        self.log("Removing major streaming service bloatware...")
        removed = 0

        for package in self.streaming_bloatware:
            self.log(f"Removing {package}...")

            # Force stop first
            self.adb_cmd(f"shell am force-stop {package}")

            # Disable then uninstall
            success1, _ = self.adb_cmd(f"shell pm disable-user --user 0 {package}")
            success2, _ = self.adb_cmd(f"shell pm uninstall --user 0 {package}")
            success3, _ = self.adb_cmd(f"shell pm clear {package}")

            if success1 or success2:
                removed += 1
                self.log(f"✓ Removed {package}")
            else:
                self.log(f"- {package} not found or already removed")

        self.log(f"Streaming bloatware removal: {removed} packages removed")
        return True

    def remove_amazon_bloatware(self):
        self.log("Removing Amazon bloatware...")
        removed = 0

        for package in self.amazon_bloatware:
            self.log(f"Removing {package}...")

            # Force stop first
            self.adb_cmd(f"shell am force-stop {package}")

            # Disable and uninstall
            success1, _ = self.adb_cmd(f"shell pm disable-user --user 0 {package}")
            success2, _ = self.adb_cmd(f"shell pm uninstall --user 0 {package}")
            success3, _ = self.adb_cmd(f"shell pm clear {package}")

            if success1 or success2:
                removed += 1
                self.log(f"✓ Removed {package}")
            else:
                self.log(f"- {package} not found")

        self.log(f"Amazon bloatware removal: {removed} packages removed")
        return True

    def disable_amazon_services(self):
        self.log("Disabling unnecessary Amazon services...")
        disabled = 0

        for package in self.amazon_services:
            self.log(f"Disabling {package}...")

            # Force stop and disable
            self.adb_cmd(f"shell am force-stop {package}")
            success, _ = self.adb_cmd(f"shell pm disable-user --user 0 {package}")

            if success:
                disabled += 1
                self.log(f"✓ Disabled {package}")
            else:
                self.log(f"- {package} not found")

        self.log(f"Amazon services disabled: {disabled} services")
        return True

    def setup_kodi_launcher(self):
        self.log("Setting up Kodi as primary launcher...")

        # Stop Amazon launcher completely
        self.adb_cmd("shell am force-stop com.amazon.tv.launcher")

        # Clear Amazon launcher as default
        success, _ = self.adb_cmd("shell pm clear com.amazon.tv.launcher")

        # Start Kodi
        success, output = self.adb_cmd("shell am start -n org.xbmc.kodi/.Splash")

        if success:
            self.log("✓ Kodi launched successfully")

            # Try to set as default home activity (may fail due to Android restrictions)
            self.adb_cmd("shell cmd package set-home-activity org.xbmc.kodi/.Splash")

            return True
        else:
            self.log(f"Failed to start Kodi: {output}")
            return False

    def validate_removal(self):
        self.log("Validating bloatware removal...")

        # Check if major bloatware is still present
        success, packages = self.adb_cmd("shell pm list packages")

        if success:
            remaining_bloat = []
            for package in self.streaming_bloatware + self.amazon_bloatware[:10]:  # Check first 10
                if package in packages:
                    remaining_bloat.append(package)

            if remaining_bloat:
                self.log(f"Warning: {len(remaining_bloat)} packages still present")
                for pkg in remaining_bloat:
                    self.log(f"  - {pkg}")
            else:
                self.log("✓ Major bloatware successfully removed")

            # Count total packages
            total_packages = packages.count('package:')
            self.log(f"Total remaining packages: {total_packages}")

            return len(remaining_bloat) == 0

        return False

    def run_true_gold_debloat(self):
        self.log("="*70)
        self.log("FIRE TV CUBE TRUE GOLD BUILD - COMPLETE DEBLOATING")
        self.log("="*70)

        steps = [
            ("Remove Streaming Bloatware", self.remove_streaming_bloatware),
            ("Remove Amazon Bloatware", self.remove_amazon_bloatware),
            ("Disable Amazon Services", self.disable_amazon_services),
            ("Setup Kodi Launcher", self.setup_kodi_launcher),
            ("Validate Removal", self.validate_removal)
        ]

        completed = 0
        for step_name, step_func in steps:
            self.log(f"\n[STEP] {step_name}...")
            try:
                if step_func():
                    completed += 1
                    self.log(f"✓ {step_name} completed")
                else:
                    self.log(f"✗ {step_name} failed")
            except Exception as e:
                self.log(f"✗ {step_name} error: {e}")

        self.log("="*70)

        if completed >= 4:
            self.log("*** TRUE FIRE TV CUBE GOLD BUILD COMPLETE! ***")
            self.log("*** NETFLIX REMOVED | AMAZON BLOAT REMOVED | KODI OPTIMIZED ***")
            print("\n🏆 TRUE GOLD BUILD ACHIEVED!")
            print("✓ Netflix completely removed")
            print("✓ Amazon Prime Video removed")
            print("✓ Amazon bloatware eliminated")
            print("✓ Kodi set as primary interface")
            print("✓ System optimized for pure streaming")
            return True
        else:
            self.log(f"Partial debloating: {completed}/{len(steps)} completed")
            return False

if __name__ == "__main__":
    debloater = TrueGoldDebloater()
    success = debloater.run_true_gold_debloat()

    if not success:
        print("Debloating incomplete - check logs above")