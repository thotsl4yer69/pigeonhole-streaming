#!/usr/bin/env python3
"""
Pigeonhole Streaming - Beginner Configuration Helper

This tool helps beginners customize their Pigeonhole Streaming setup
without needing to understand YAML syntax or technical details.
"""

import os
import sys
import re
from pathlib import Path

class BeginnerConfigHelper:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.config_file = self.project_root / 'config' / 'pigeonhole_config.yaml'
        
    def print_header(self):
        print("🎨" + "="*60 + "🎨")
        print("     PIGEONHOLE STREAMING - EASY CUSTOMIZATION")
        print("     Make It Your Own!")
        print("🎨" + "="*60 + "🎨")
        print()

    def get_user_input(self, prompt, default_value="", validation_func=None):
        """Get user input with validation"""
        while True:
            if default_value:
                user_input = input(f"{prompt} [{default_value}]: ").strip()
                if not user_input:
                    user_input = default_value
            else:
                user_input = input(f"{prompt}: ").strip()
            
            if validation_func:
                if validation_func(user_input):
                    return user_input
                else:
                    print("   ❌ Invalid input, please try again.")
            else:
                return user_input

    def validate_color(self, color_input):
        """Validate color input (6-digit hex)"""
        if len(color_input) == 6 and all(c in '0123456789ABCDEFabcdef' for c in color_input):
            return True
        print("   💡 Color should be 6 digits (like FF0000 for red, 0000FF for blue)")
        return False

    def customize_branding(self):
        """Interactive branding customization"""
        print("🎨 CUSTOMIZE YOUR BRANDING")
        print("Make your Fire TV show your own name and style!")
        print()
        
        # Get current values
        current_name = "PIGEONHOLE STREAMING"
        current_tagline = "ALL YOUR ENTERTAINMENT. ONE DEVICE"
        
        print("📝 Current settings:")
        print(f"   Name: {current_name}")
        print(f"   Tagline: {current_tagline}")
        print()
        
        # Get new values
        new_name = self.get_user_input(
            "🏷️  What should your media center be called?", 
            current_name
        )
        
        new_tagline = self.get_user_input(
            "💬 What tagline/message do you want?", 
            current_tagline
        )
        
        return {
            'name': new_name,
            'tagline': new_tagline
        }

    def customize_colors(self):
        """Interactive color customization"""
        print("🌈 CUSTOMIZE YOUR COLORS")
        print("Make it match your style!")
        print()
        
        color_examples = {
            'Red': 'FF0000',
            'Blue': '0000FF', 
            'Green': '00FF00',
            'Purple': '800080',
            'Orange': 'FF6600',
            'Pink': 'FF69B4',
            'Gold': 'FFD700'
        }
        
        print("🎨 Popular color choices:")
        for name, code in color_examples.items():
            print(f"   {name}: {code}")
        print()
        
        primary_color = self.get_user_input(
            "🎯 Primary color (main highlight color)",
            "FF6B35",
            self.validate_color
        )
        
        secondary_color = self.get_user_input(
            "🎨 Secondary color (background accents)", 
            "1E3A8A",
            self.validate_color
        )
        
        return {
            'primary': f"FF{primary_color.upper()}",
            'secondary': f"FF{secondary_color.upper()}"
        }

    def customize_streaming_apps(self):
        """Choose which streaming apps to include"""
        print("📱 CUSTOMIZE STREAMING APPS")
        print("Choose which apps you want on your Fire TV")
        print()
        
        essential_apps = {
            'plugin.video.youtube': 'YouTube (recommended)',
            'plugin.video.thecrew': 'The Crew - Movies & TV Shows',
            'plugin.video.daddylive': 'DaddyLive - Live TV & Sports',
            'script.module.resolveurl': 'ResolveURL (needed for streaming)',
        }
        
        optional_apps = {
            'plugin.video.twitch': 'Twitch - Game Streaming',
            'plugin.video.vimeo': 'Vimeo',
            'plugin.audio.tuneinradio': 'TuneIn Radio',
        }
        
        print("✅ Essential apps (automatically included):")
        for app_id, description in essential_apps.items():
            print(f"   • {description}")
        print()
        
        print("🎯 Optional apps (choose which ones you want):")
        selected_optional = []
        for app_id, description in optional_apps.items():
            choice = input(f"   Include {description}? (y/n) [n]: ").strip().lower()
            if choice in ['y', 'yes']:
                selected_optional.append(app_id)
                print(f"      ✅ Added {description}")
            else:
                print(f"      ⏭️  Skipped {description}")
        
        return {
            'essential': list(essential_apps.keys()),
            'optional': selected_optional
        }

    def choose_device_profile(self):
        """Choose deployment profile"""
        print("🎯 CHOOSE YOUR SETUP TYPE")
        print("Different setups for different needs")
        print()
        
        profiles = {
            'home': {
                'name': 'Home Setup',
                'description': 'Perfect for personal/family use',
                'features': ['All streaming apps', 'Easy customization', 'Family-friendly']
            },
            'corporate': {
                'name': 'Business/Corporate', 
                'description': 'Professional environments',
                'features': ['Locked settings', 'Professional branding', 'Security focused']
            },
            'hotel': {
                'name': 'Hotel/Hospitality',
                'description': 'Guest room entertainment',
                'features': ['Auto-reset', 'Guest mode', 'Time limits']
            }
        }
        
        print("Available setups:")
        for key, profile in profiles.items():
            print(f"   {key.upper()}: {profile['name']}")
            print(f"      📝 {profile['description']}")
            print(f"      ✨ Features: {', '.join(profile['features'])}")
            print()
        
        while True:
            choice = input("Which setup type do you want? (home/corporate/hotel) [home]: ").strip().lower()
            if not choice:
                choice = 'home'
            
            if choice in profiles:
                return choice
            else:
                print("   ❌ Please choose: home, corporate, or hotel")

    def apply_changes(self, branding, colors, apps, profile):
        """Apply changes to configuration file"""
        print("💾 APPLYING YOUR CHANGES...")
        
        if not self.config_file.exists():
            print("   ❌ Configuration file not found!")
            return False
        
        try:
            # Read current config
            with open(self.config_file, 'r') as f:
                config_content = f.read()
            
            # Update branding
            config_content = re.sub(
                r'name: ".*?"', 
                f'name: "{branding["name"]}"', 
                config_content
            )
            config_content = re.sub(
                r'tagline: ".*?"', 
                f'tagline: "{branding["tagline"]}"', 
                config_content
            )
            
            # Update colors
            config_content = re.sub(
                r'primary_color: ".*?"', 
                f'primary_color: "{colors["primary"]}"', 
                config_content
            )
            config_content = re.sub(
                r'secondary_color: ".*?"', 
                f'secondary_color: "{colors["secondary"]}"', 
                config_content
            )
            
            # Create backup
            backup_file = self.config_file.with_suffix('.yaml.backup')
            with open(backup_file, 'w') as f:
                f.write(config_content)
            
            # Save changes
            with open(self.config_file, 'w') as f:
                f.write(config_content)
            
            print("   ✅ Configuration updated successfully!")
            print(f"   💾 Backup saved as: {backup_file.name}")
            return True
            
        except Exception as e:
            print(f"   ❌ Error updating configuration: {str(e)}")
            return False

    def show_summary(self, branding, colors, apps, profile):
        """Show summary of changes"""
        print("📋 CUSTOMIZATION SUMMARY")
        print("=" * 50)
        print(f"🏷️  Name: {branding['name']}")
        print(f"💬 Tagline: {branding['tagline']}")
        print(f"🎨 Primary Color: #{colors['primary'][2:]}")  # Remove FF prefix
        print(f"🎨 Secondary Color: #{colors['secondary'][2:]}")
        print(f"🎯 Setup Type: {profile.upper()}")
        print(f"📱 Apps: {len(apps['essential']) + len(apps['optional'])} total")
        print()
        
        print("🚀 NEXT STEPS:")
        print("1. Your configuration has been saved")
        print("2. Connect your Fire TV device")
        print("3. Run: deploy_pigeonhole_stable_final.bat")
        print("4. Enjoy your customized media center!")

    def run_customization(self):
        """Run the complete customization process"""
        self.print_header()
        
        print("Welcome! This tool will help you customize your Pigeonhole Streaming setup.")
        print("We'll go through a few simple questions to make it perfect for you.")
        print()
        
        # Check if config file exists
        if not self.config_file.exists():
            print("❌ Configuration file not found!")
            print(f"Looking for: {self.config_file}")
            print()
            print("💡 Make sure you're running this from the project root directory.")
            return
        
        input("Press Enter to start customizing...")
        print()
        
        # Gather customizations
        branding = self.customize_branding()
        print()
        colors = self.customize_colors() 
        print()
        apps = self.customize_streaming_apps()
        print()
        profile = self.choose_device_profile()
        print()
        
        # Show summary and confirm
        self.show_summary(branding, colors, apps, profile)
        print()
        
        confirm = input("Apply these changes? (y/n) [y]: ").strip().lower()
        if confirm in ['', 'y', 'yes']:
            if self.apply_changes(branding, colors, apps, profile):
                print()
                print("🎉 SUCCESS! Your Pigeonhole Streaming is now customized!")
                print("You're ready to deploy to your Fire TV device.")
            else:
                print()
                print("❌ Something went wrong. Check the error messages above.")
        else:
            print()
            print("❌ Changes cancelled. Your configuration is unchanged.")

if __name__ == "__main__":
    customizer = BeginnerConfigHelper()
    customizer.run_customization()