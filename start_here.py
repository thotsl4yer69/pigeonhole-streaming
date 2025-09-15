#!/usr/bin/env python3
"""
Pigeonhole Streaming - Beginner's First Steps

This is your starting point! Run this first to understand your project
and get simple guidance on what to do next.
"""

import os
import sys
from pathlib import Path

def print_welcome():
    print("🎬" + "="*70 + "🎬")
    print("           WELCOME TO PIGEONHOLE STREAMING!")
    print("         Your Personal Fire TV Media Center")
    print("🎬" + "="*70 + "🎬")
    print()

def print_what_you_have():
    """Explain what the user has built"""
    print("🎯 WHAT YOU'VE BUILT:")
    print("You have a professional-grade system that transforms Amazon Fire TV")
    print("devices into custom-branded streaming media centers!")
    print()
    
    print("✨ What it does:")
    print("   📺 Installs Kodi media center on Fire TV")
    print("   🎨 Applies custom 'Pigeonhole Streaming' branding")
    print("   📱 Adds streaming apps (YouTube, movies, live TV, sports)")
    print("   🌐 Enables remote control via web browser")
    print("   🚀 Can deploy to multiple Fire TV devices automatically")
    print()
    
    print("🏢 Perfect for:")
    print("   🏠 Home entertainment systems")
    print("   🏢 Business/corporate environments") 
    print("   🏨 Hotel room entertainment")
    print("   🏪 Retail displays")
    print()

def check_readiness():
    """Check if user is ready to proceed"""
    print("📋 BEFORE WE START:")
    print()
    
    requirements = [
        ("Amazon Fire TV device (Cube, Stick, etc.)", "📺"),
        ("Fire TV and computer on same WiFi network", "🌐"),
        ("ADB debugging enabled on Fire TV", "🔧"),
        ("30 minutes of time for first setup", "⏰")
    ]
    
    print("You'll need:")
    for req, icon in requirements:
        print(f"   {icon} {req}")
    print()
    
    ready = input("Do you have these ready? (y/n) [y]: ").strip().lower()
    return ready in ['', 'y', 'yes']

def show_menu():
    """Show main menu options"""
    print("🎯 WHAT WOULD YOU LIKE TO DO?")
    print()
    
    options = {
        '1': ('📚 Read the Beginner Guide', 'Learn step-by-step how to use your project'),
        '2': ('🔍 Check Project Health', 'See what\'s working and what needs attention'),
        '3': ('🎨 Customize Colors & Branding', 'Make it your own with custom colors and name'),
        '4': ('📱 Connect to Fire TV', 'Get help connecting to your Fire TV device'),
        '5': ('🚀 Deploy to Fire TV', 'Install everything on your Fire TV (main action)'),
        '6': ('🌐 Set Up Remote Control', 'Control Fire TV from phone/computer'),
        '7': ('🆘 Get Help/Troubleshooting', 'Fix problems or get support'),
        '8': ('❓ Explain What Files Do', 'Understand your project structure')
    }
    
    for key, (title, description) in options.items():
        print(f"   {key}. {title}")
        print(f"      {description}")
        print()
    
    print("   9. 🚪 Exit")
    print()
    
    choice = input("Choose an option (1-9): ").strip()
    return choice

def handle_choice(choice):
    """Handle user menu choice"""
    project_root = Path(__file__).parent
    
    if choice == '1':
        print("📚 Opening Beginner Guide...")
        guide_file = project_root / 'BEGINNER_GUIDE.md'
        if guide_file.exists():
            print(f"✅ Found guide at: {guide_file}")
            print("💡 Open this file in any text editor to read the complete guide.")
            input("Press Enter to continue...")
        else:
            print("❌ Beginner guide not found!")
    
    elif choice == '2':
        print("🔍 Running Project Health Check...")
        try:
            os.system('python3 health_check.py')
        except:
            print("❌ Could not run health check. Make sure health_check.py exists.")
        input("Press Enter to continue...")
    
    elif choice == '3':
        print("🎨 Starting Customization Tool...")
        try:
            os.system('python3 easy_customize.py')
        except:
            print("❌ Could not run customization tool. Make sure easy_customize.py exists.")
        input("Press Enter to continue...")
    
    elif choice == '4':
        show_fire_tv_connection_help()
    
    elif choice == '5':
        show_deployment_help()
    
    elif choice == '6':
        show_remote_control_help()
    
    elif choice == '7':
        show_troubleshooting_help()
    
    elif choice == '8':
        print("❓ Opening 'What Does This Do?' guide...")
        guide_file = project_root / 'WHAT_DOES_THIS_DO.md'
        if guide_file.exists():
            print(f"✅ Found guide at: {guide_file}")
            print("💡 Open this file in any text editor to understand each file.")
            input("Press Enter to continue...")
        else:
            print("❌ File explanation guide not found!")
    
    elif choice == '9':
        return False
    
    else:
        print("❌ Invalid choice. Please choose 1-9.")
        input("Press Enter to try again...")
    
    return True

def show_fire_tv_connection_help():
    """Show Fire TV connection instructions"""
    print("📱 CONNECTING TO YOUR FIRE TV")
    print("=" * 50)
    print()
    print("Step 1: Enable Developer Options")
    print("   • Go to Settings → My Fire TV → About")
    print("   • Click on your Fire TV name 7 times quickly")
    print("   • You'll see 'Developer options enabled'")
    print()
    print("Step 2: Enable ADB Debugging")
    print("   • Go to Settings → My Fire TV → Developer Options")
    print("   • Turn ON 'ADB debugging'")
    print("   • Turn ON 'Apps from Unknown Sources'")
    print()
    print("Step 3: Find Your Fire TV IP Address")
    print("   • Go to Settings → My Fire TV → About → Network")
    print("   • Write down the IP address (like 192.168.1.130)")
    print()
    print("Step 4: Test Connection")
    print("   • Open Command Prompt on your computer")
    print("   • Type: adb connect YOUR_IP_ADDRESS:5555")
    print("   • Example: adb connect 192.168.1.130:5555")
    print("   • You should see 'connected to...'")
    print()
    input("Press Enter to continue...")

def show_deployment_help():
    """Show deployment instructions"""
    print("🚀 DEPLOYING TO YOUR FIRE TV")
    print("=" * 50)
    print()
    print("✅ Prerequisites:")
    print("   • Fire TV connected (see option 4 for help)")
    print("   • ADB debugging enabled")
    print("   • Both devices on same WiFi")
    print()
    print("🎯 Main Deployment (Recommended):")
    print("   1. Find file: deploy_pigeonhole_stable_final.bat")
    print("   2. Right-click → 'Run as Administrator'")
    print("   3. Wait 10-15 minutes (it does everything automatically)")
    print("   4. Your Fire TV will restart with new interface")
    print()
    print("⚠️  What to expect:")
    print("   • Kodi will be installed")
    print("   • Streaming apps will be added")
    print("   • Custom Pigeonhole branding applied")
    print("   • Interface will look professional")
    print()
    print("🆘 If something goes wrong:")
    print("   • Run: kodi_recovery_system.bat")
    print("   • Or choose option 7 for troubleshooting")
    print()
    input("Press Enter to continue...")

def show_remote_control_help():
    """Show remote control setup"""
    print("🌐 REMOTE CONTROL VIA WEB BROWSER")
    print("=" * 50)
    print()
    print("After deployment, you can control your Fire TV from any device!")
    print()
    print("📱 How to access:")
    print("   1. Make sure your Fire TV is running Kodi")
    print("   2. Open web browser on phone/computer/tablet")
    print("   3. Go to: http://YOUR_FIRE_TV_IP:8080")
    print("   4. Example: http://192.168.1.130:8080")
    print()
    print("🎮 What you can do:")
    print("   • Navigate menus")
    print("   • Launch apps")
    print("   • Control playback")
    print("   • Change settings")
    print("   • Browse content")
    print()
    print("🔧 Test remote control:")
    print("   • Run: python3 test_kodi_http.py")
    print("   • Or use option 2 (health check)")
    print()
    input("Press Enter to continue...")

def show_troubleshooting_help():
    """Show troubleshooting options"""
    print("🆘 TROUBLESHOOTING & GETTING HELP")
    print("=" * 50)
    print()
    print("🔧 Common Solutions:")
    print()
    print("Problem: Can't connect to Fire TV")
    print("   ✅ Check ADB debugging is enabled")
    print("   ✅ Both devices on same WiFi network")
    print("   ✅ Try: adb kill-server then adb start-server")
    print()
    print("Problem: Deployment fails")
    print("   ✅ Run as Administrator")
    print("   ✅ Check internet connection")
    print("   ✅ Try: kodi_recovery_system.bat")
    print()
    print("Problem: Fire TV shows errors")
    print("   ✅ Restart Fire TV")
    print("   ✅ Run recovery script")
    print("   ✅ Re-run deployment")
    print()
    print("Problem: Remote control not working")
    print("   ✅ Check Kodi is running")
    print("   ✅ Verify IP address")
    print("   ✅ Test with: python3 test_kodi_http.py")
    print()
    print("🔍 Diagnostic Tools:")
    print("   • health_check.py - Check what's working")
    print("   • test_kodi_http.py - Test remote control")
    print("   • test_streaming_functionality.py - Test streaming")
    print()
    input("Press Enter to continue...")

def main():
    """Main program loop"""
    print_welcome()
    print_what_you_have()
    
    if not check_readiness():
        print()
        print("💡 Come back when you're ready! Your project will be waiting.")
        print("📚 In the meantime, read BEGINNER_GUIDE.md to prepare.")
        return
    
    print()
    print("🎉 Great! Let's get started...")
    print()
    
    while True:
        choice = show_menu()
        if not handle_choice(choice):
            break
        print()
    
    print()
    print("🎉 Thanks for using Pigeonhole Streaming!")
    print("🎬 Enjoy your custom Fire TV media center!")

if __name__ == "__main__":
    main()