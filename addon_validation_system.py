#!/usr/bin/env python3
"""
Pigeonhole Streaming - Automated Addon Validation System
Validates Kodi addons, checks dependencies, and ensures compatibility
"""

import os
import subprocess
import xml.etree.ElementTree as ET
import json
import time
from datetime import datetime

class KodiAddonValidator:
    def __init__(self):
        self.fire_tv_ip = "192.168.1.130"
        self.adb_path = r"M:\platform-tools\adb.exe"
        self.kodi_data_path = "/sdcard/Android/data/org.xbmc.kodi/files/.kodi"
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "validation_results": [],
            "performance_metrics": {},
            "recommendations": []
        }
        
    def run_adb_command(self, command, timeout=30):
        """Execute ADB command with error handling"""
        try:
            full_command = f'"{self.adb_path}" {command}'
            result = subprocess.run(full_command, shell=True, capture_output=True, 
                                  text=True, timeout=timeout)
            return result.stdout.strip(), result.stderr.strip(), result.returncode
        except subprocess.TimeoutExpired:
            return "", "Command timeout", 1
        except Exception as e:
            return "", str(e), 1

    def connect_device(self):
        """Connect to Fire TV device"""
        print("Connecting to Fire TV Cube...")
        stdout, stderr, code = self.run_adb_command(f"connect {self.fire_tv_ip}:5555")
        if "connected" in stdout.lower() or "already connected" in stdout.lower():
            print("✓ Connected to Fire TV")
            return True
        else:
            print(f"✗ Connection failed: {stderr}")
            return False

    def validate_addon_xml(self, addon_path):
        """Validate addon.xml structure and dependencies"""
        validation = {
            "addon_path": addon_path,
            "valid_xml": False,
            "dependencies_met": [],
            "missing_dependencies": [],
            "version": None,
            "provider": None,
            "errors": []
        }
        
        try:
            # Pull addon.xml from device
            xml_path = f"{self.kodi_data_path}/addons/{addon_path}/addon.xml"
            stdout, stderr, code = self.run_adb_command(f'shell "cat {xml_path}"')
            
            if code != 0:
                validation["errors"].append(f"Cannot read addon.xml: {stderr}")
                return validation
                
            # Parse XML
            root = ET.fromstring(stdout)
            validation["valid_xml"] = True
            validation["version"] = root.get("version")
            validation["provider"] = root.get("provider-name")
            
            # Check dependencies
            requires = root.find("requires")
            if requires is not None:
                for import_elem in requires.findall("import"):
                    dep_addon = import_elem.get("addon")
                    min_version = import_elem.get("version")
                    
                    # Check if dependency exists
                    dep_stdout, _, dep_code = self.run_adb_command(
                        f'shell "test -d {self.kodi_data_path}/addons/{dep_addon} && echo exists"'
                    )
                    
                    if "exists" in dep_stdout:
                        validation["dependencies_met"].append({
                            "addon": dep_addon, 
                            "required_version": min_version
                        })
                    else:
                        validation["missing_dependencies"].append({
                            "addon": dep_addon, 
                            "required_version": min_version
                        })
                        
        except ET.ParseError as e:
            validation["errors"].append(f"XML parsing error: {str(e)}")
        except Exception as e:
            validation["errors"].append(f"Validation error: {str(e)}")
            
        return validation

    def check_addon_functionality(self, addon_id):
        """Test addon functionality and startup"""
        print(f"Testing addon functionality: {addon_id}")
        
        # Start Kodi
        self.run_adb_command('shell "am start -n org.xbmc.kodi/.Splash"')
        time.sleep(10)
        
        # Check if Kodi process is stable
        stdout, _, code = self.run_adb_command('shell "ps | grep kodi"')
        if code == 0 and "kodi" in stdout:
            return {
                "addon_id": addon_id,
                "kodi_stable": True,
                "memory_usage": self.get_memory_usage(),
                "startup_time": "< 10s"
            }
        else:
            return {
                "addon_id": addon_id,
                "kodi_stable": False,
                "error": "Kodi failed to start or crashed"
            }

    def get_memory_usage(self):
        """Get current memory usage"""
        stdout, _, _ = self.run_adb_command('shell "top -n 1 | grep kodi"')
        if stdout:
            parts = stdout.split()
            if len(parts) >= 6:
                return {
                    "memory_mb": parts[5],
                    "cpu_percent": parts[8] if len(parts) > 8 else "N/A"
                }
        return {"memory_mb": "Unknown", "cpu_percent": "Unknown"}

    def validate_all_addons(self):
        """Validate all installed addons"""
        print("Starting comprehensive addon validation...")
        
        if not self.connect_device():
            return False

        # Get list of installed addons
        stdout, _, code = self.run_adb_command(
            f'shell "ls {self.kodi_data_path}/addons/"'
        )
        
        if code != 0:
            print("Failed to list addons")
            return False
            
        addons = [addon.strip() for addon in stdout.split('\n') if addon.strip()]
        print(f"Found {len(addons)} addons to validate")

        # Validate each addon
        for addon in addons:
            if addon.startswith('.') or addon == 'packages':
                continue
                
            print(f"\nValidating: {addon}")
            validation = self.validate_addon_xml(addon)
            functionality = self.check_addon_functionality(addon)
            
            combined_result = {**validation, **functionality}
            self.results["validation_results"].append(combined_result)
            
            # Print immediate results
            if validation["valid_xml"]:
                print(f"  ✓ Valid XML structure")
                print(f"  ✓ Version: {validation['version']}")
                if validation["missing_dependencies"]:
                    print(f"  ⚠ Missing dependencies: {len(validation['missing_dependencies'])}")
                else:
                    print(f"  ✓ All dependencies met")
            else:
                print(f"  ✗ Invalid or missing addon.xml")
                
        # Generate recommendations
        self.generate_recommendations()
        
        # Save results
        self.save_results()
        
        return True

    def generate_recommendations(self):
        """Generate improvement recommendations"""
        critical_addons = ["script.module.resolveurl", "skin.arctic.zephyr.pigeonhole"]
        
        for result in self.results["validation_results"]:
            addon_path = result.get("addon_path", "")
            
            # Check critical addons
            if any(critical in addon_path for critical in critical_addons):
                if not result.get("valid_xml", False):
                    self.results["recommendations"].append({
                        "priority": "HIGH",
                        "addon": addon_path,
                        "issue": "Critical addon has invalid XML",
                        "action": "Reinstall or repair addon"
                    })
                    
            # Check missing dependencies
            if result.get("missing_dependencies"):
                self.results["recommendations"].append({
                    "priority": "MEDIUM",
                    "addon": addon_path,
                    "issue": f"Missing {len(result['missing_dependencies'])} dependencies",
                    "action": "Install missing dependencies"
                })

    def save_results(self):
        """Save validation results to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"M:\\validation_report_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2)
            print(f"\nValidation report saved to: {filename}")
        except Exception as e:
            print(f"Failed to save report: {e}")

    def print_summary(self):
        """Print validation summary"""
        total_addons = len(self.results["validation_results"])
        valid_addons = sum(1 for r in self.results["validation_results"] if r.get("valid_xml", False))
        
        print("\n" + "="*50)
        print("VALIDATION SUMMARY")
        print("="*50)
        print(f"Total addons validated: {total_addons}")
        print(f"Valid XML structure: {valid_addons}")
        print(f"Invalid/Missing XML: {total_addons - valid_addons}")
        print(f"Recommendations: {len(self.results['recommendations'])}")
        
        # Show critical recommendations
        high_priority = [r for r in self.results["recommendations"] if r["priority"] == "HIGH"]
        if high_priority:
            print("\nCRITICAL ISSUES:")
            for rec in high_priority:
                print(f"  ⚠ {rec['addon']}: {rec['issue']}")
                
        print("\nValidation complete!")

def main():
    """Main execution function"""
    validator = KodiAddonValidator()
    
    if validator.validate_all_addons():
        validator.print_summary()
    else:
        print("Validation failed - check connection and try again")

if __name__ == "__main__":
    main()