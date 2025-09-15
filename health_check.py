#!/usr/bin/env python3
"""
Pigeonhole Project Health Check & Beginner Diagnostic Tool

This tool helps beginners understand their Pigeonhole Streaming project 
by checking what's working, what's not, and providing simple explanations.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

class PigeonholeHealthCheck:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.issues_found = []
        self.all_good = []
        
    def print_header(self):
        print("🎬" + "="*60 + "🎬")
        print("     PIGEONHOLE STREAMING - PROJECT HEALTH CHECK")
        print("     Understanding Your Project Status")
        print("🎬" + "="*60 + "🎬")
        print()

    def check_python_environment(self):
        """Check if Python and required modules are available"""
        print("🐍 CHECKING PYTHON ENVIRONMENT...")
        
        # Python version
        python_version = sys.version.split()[0]
        print(f"   ✅ Python Version: {python_version}")
        self.all_good.append(f"Python {python_version} is working")
        
        # Required modules
        required_modules = ['yaml', 'pathlib', 'subprocess']
        missing_modules = []
        
        for module in required_modules:
            try:
                __import__(module)
                print(f"   ✅ Module '{module}' available")
            except ImportError:
                print(f"   ❌ Module '{module}' missing")
                missing_modules.append(module)
        
        if missing_modules:
            self.issues_found.append(f"Missing Python modules: {', '.join(missing_modules)}")
        else:
            self.all_good.append("All required Python modules available")
        
        print()

    def check_project_structure(self):
        """Check if essential project files exist"""
        print("📁 CHECKING PROJECT STRUCTURE...")
        
        essential_files = {
            'deploy_pigeonhole_stable_final.bat': 'Main deployment script',
            'config/pigeonhole_config.yaml': 'Configuration file',
            'scripts/pigeonhole_config.py': 'Python configuration framework',
            'README.md': 'Project documentation',
            'CLAUDE.md': 'AI assistant guidance',
        }
        
        essential_directories = {
            'scripts/': 'Python automation scripts',
            'config/': 'Configuration files',
            'addons/': 'Kodi addons',
            'documentation/': 'Setup guides'
        }
        
        # Check files
        for file_path, description in essential_files.items():
            full_path = self.project_root / file_path
            if full_path.exists():
                print(f"   ✅ {file_path} - {description}")
                self.all_good.append(f"Found {description}")
            else:
                print(f"   ❌ {file_path} - {description} (MISSING)")
                self.issues_found.append(f"Missing {description} at {file_path}")
        
        # Check directories
        for dir_path, description in essential_directories.items():
            full_path = self.project_root / dir_path
            if full_path.exists() and full_path.is_dir():
                item_count = len(list(full_path.iterdir()))
                print(f"   ✅ {dir_path} - {description} ({item_count} items)")
                self.all_good.append(f"Found {description} with {item_count} items")
            else:
                print(f"   ❌ {dir_path} - {description} (MISSING)")
                self.issues_found.append(f"Missing {description} directory at {dir_path}")
        
        print()

    def check_configuration(self):
        """Check if configuration system is working"""
        print("⚙️ CHECKING CONFIGURATION SYSTEM...")
        
        config_file = self.project_root / 'config' / 'pigeonhole_config.yaml'
        
        if config_file.exists():
            print(f"   ✅ Configuration file found")
            print(f"   📄 Size: {config_file.stat().st_size} bytes")
            self.all_good.append("Configuration file exists")
            
            # Try to load configuration
            try:
                from scripts.pigeonhole_config import get_config
                
                config = get_config()
                print(f"   ✅ Configuration system loads successfully")
                self.all_good.append("Configuration system working")
                
                # Check some basic config values
                if hasattr(config, 'branding'):
                    print(f"   🎨 Branding configured")
                    self.all_good.append("Branding configuration found")
                
            except Exception as e:
                print(f"   ❌ Configuration system error: {str(e)}")
                self.issues_found.append(f"Configuration system not working: {str(e)}")
        else:
            print(f"   ❌ Configuration file not found")
            self.issues_found.append("Configuration file missing")
        
        print()

    def check_deployment_scripts(self):
        """Check deployment scripts"""
        print("🚀 CHECKING DEPLOYMENT SCRIPTS...")
        
        deployment_scripts = [
            'deploy_pigeonhole_stable_final.bat',
            'deploy_pigeonhole_final.bat',
            'deploy_pigeonhole_gold.bat'
        ]
        
        working_scripts = []
        for script in deployment_scripts:
            script_path = self.project_root / script
            if script_path.exists():
                print(f"   ✅ {script} - Available")
                working_scripts.append(script)
            else:
                print(f"   ❌ {script} - Missing")
        
        if working_scripts:
            print(f"   🎯 Primary deployment script: {working_scripts[0]}")
            self.all_good.append(f"Found {len(working_scripts)} deployment scripts")
        else:
            self.issues_found.append("No deployment scripts found")
        
        print()

    def check_adb_availability(self):
        """Check if ADB is available for Fire TV deployment"""
        print("📱 CHECKING ADB (ANDROID DEBUG BRIDGE)...")
        
        try:
            # Try to run adb command
            result = subprocess.run(['adb', 'version'], 
                                   capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                adb_version = result.stdout.split('\n')[0]
                print(f"   ✅ ADB Available: {adb_version}")
                self.all_good.append("ADB is available for Fire TV deployment")
                
                # Check for connected devices
                device_result = subprocess.run(['adb', 'devices'], 
                                             capture_output=True, text=True, timeout=10)
                if device_result.returncode == 0:
                    devices = device_result.stdout.strip().split('\n')[1:]  # Skip header
                    connected_devices = [d for d in devices if d.strip() and 'device' in d]
                    
                    if connected_devices:
                        print(f"   🔗 Connected devices: {len(connected_devices)}")
                        for device in connected_devices:
                            print(f"      📱 {device}")
                        self.all_good.append(f"Found {len(connected_devices)} connected Fire TV devices")
                    else:
                        print(f"   ⚠️  No Fire TV devices connected")
                        print(f"      💡 This is normal - connect when ready to deploy")
            else:
                print(f"   ❌ ADB command failed")
                self.issues_found.append("ADB not working properly")
                
        except FileNotFoundError:
            print(f"   ❌ ADB not found in system PATH")
            print(f"      💡 Install Android Debug Bridge or use included tools")
            self.issues_found.append("ADB not installed or not in PATH")
            
        except subprocess.TimeoutExpired:
            print(f"   ❌ ADB command timed out")
            self.issues_found.append("ADB not responding")
            
        print()

    def check_documentation(self):
        """Check if documentation is available"""
        print("📚 CHECKING DOCUMENTATION...")
        
        docs = {
            'README.md': 'Main project overview',
            'BEGINNER_GUIDE.md': 'Beginner-friendly guide',
            'CLAUDE.md': 'AI assistant guidance',
            'PIGEONHOLE_PROJECT_STRUCTURE.md': 'Project structure guide'
        }
        
        available_docs = []
        for doc, description in docs.items():
            doc_path = self.project_root / doc
            if doc_path.exists():
                print(f"   ✅ {doc} - {description}")
                available_docs.append(doc)
            else:
                print(f"   ❌ {doc} - {description} (missing)")
        
        if available_docs:
            self.all_good.append(f"Found {len(available_docs)} documentation files")
        else:
            self.issues_found.append("Documentation files missing")
        
        print()

    def provide_recommendations(self):
        """Provide beginner-friendly recommendations"""
        print("🎯 RECOMMENDATIONS FOR NEXT STEPS...")
        print()
        
        if not self.issues_found:
            print("   🎉 EXCELLENT! Your project looks healthy!")
            print("   You're ready to start deploying to Fire TV devices.")
            print()
            print("   📋 Suggested next steps:")
            print("   1. Read BEGINNER_GUIDE.md for step-by-step instructions")
            print("   2. Connect your Fire TV device with ADB")
            print("   3. Run deploy_pigeonhole_stable_final.bat")
            print("   4. Customize config/pigeonhole_config.yaml for your preferences")
            
        else:
            print("   ⚠️  Found some issues that need attention:")
            print()
            for i, issue in enumerate(self.issues_found, 1):
                print(f"   {i}. {issue}")
            
            print()
            print("   🔧 Quick fixes:")
            if any("ADB" in issue for issue in self.issues_found):
                print("   • For ADB issues: Enable Developer Options → ADB Debugging on Fire TV")
            if any("Configuration" in issue for issue in self.issues_found):
                print("   • For config issues: Check if config/pigeonhole_config.yaml exists")
            if any("module" in issue.lower() for issue in self.issues_found):
                print("   • For module issues: Run 'pip install pyyaml pillow requests'")
        
        print()

    def run_health_check(self):
        """Run complete health check"""
        self.print_header()
        
        self.check_python_environment()
        self.check_project_structure()
        self.check_configuration()
        self.check_deployment_scripts()
        self.check_adb_availability()
        self.check_documentation()
        
        print("📊 HEALTH CHECK SUMMARY")
        print("=" * 50)
        
        print(f"✅ Working components: {len(self.all_good)}")
        for item in self.all_good:
            print(f"   • {item}")
        
        print()
        print(f"❌ Issues found: {len(self.issues_found)}")
        for item in self.issues_found:
            print(f"   • {item}")
        
        print()
        self.provide_recommendations()

if __name__ == "__main__":
    health_checker = PigeonholeHealthCheck()
    health_checker.run_health_check()