#!/usr/bin/env python3
"""
Pigeonhole Advanced Customization Framework
Create highly customized, branded Kodi experiences
"""

import json
import xml.etree.ElementTree as ET
from pathlib import Path
import shutil
import tempfile
import zipfile
import os
import logging
from PIL import Image, ImageDraw, ImageFont
import requests
from typing import Dict, List, Optional
from contextlib import contextmanager

from pigeonhole_config import get_config, BrandingConfig
from pigeonhole_device_manager import Device, DeviceType

class CustomizationError(Exception):
    """Customization related errors"""
    pass

class SkinGenerationError(Exception):
    """Skin generation related errors"""
    pass

class PigeonholeCustomizer:
    """Advanced customization framework for Kodi with enterprise features"""
    
    def __init__(self):
        self.config = get_config()
        self.branding = self.config.get_branding_config()
        self.logger = logging.getLogger('pigeonhole.customizer')
        self.temp_dir = None
        self._cleanup_dirs = []
    
    @contextmanager
    def temp_directory(self):
        """Context manager for temporary directory with automatic cleanup"""
        temp_dir = tempfile.mkdtemp(prefix='pigeonhole_')
        self._cleanup_dirs.append(temp_dir)
        try:
            yield temp_dir
        finally:
            self._cleanup_temp_dirs()
    
    def _cleanup_temp_dirs(self):
        """Clean up temporary directories"""
        for temp_dir in self._cleanup_dirs:
            try:
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
                    self.logger.debug(f"Cleaned up temp dir: {temp_dir}")
            except Exception as e:
                self.logger.warning(f"Failed to cleanup temp dir {temp_dir}: {e}")
        self._cleanup_dirs.clear()
        
    def create_custom_skin(self, device: Device, base_skin: str = "skin.amber") -> str:
        """Create completely customized skin with branding for specific device"""
        try:
            with self.temp_directory() as temp_dir:
                return self._create_skin_package(device, base_skin, temp_dir)
        except Exception as e:
            self.logger.error(f"Failed to create custom skin: {e}")
            raise SkinGenerationError(f"Skin creation failed: {e}")
    
    def _create_skin_package(self, device: Device, base_skin: str, temp_dir: str) -> str:
        """Internal method to create skin package"""
        # Create custom skin directory structure
        custom_skin_dir = os.path.join(temp_dir, "skin.pigeonhole.corporate")
        skin_dirs = [
            "1080i", "media", "resources", "colors", "fonts", "sounds"
        ]
        
        for dir_name in skin_dirs:
            Path(custom_skin_dir, dir_name).mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"Creating custom skin for {device.name} ({device.device_type.value})")
        
        # Generate device-specific components
        self._generate_addon_xml(custom_skin_dir, device)
        self._create_color_schemes(custom_skin_dir)
        self._create_custom_home_screen(custom_skin_dir, device)
        self._create_custom_graphics(custom_skin_dir, device)
        self._create_custom_fonts(custom_skin_dir)
        
        # Package the skin
        skin_zip_path = f"M:/skin.pigeonhole.{device.device_type.value}.zip"
        self._package_skin(custom_skin_dir, skin_zip_path)
        
        self.logger.info(f"Custom skin created: {skin_zip_path}")
        return skin_zip_path
        
    def _generate_addon_xml(self, skin_dir: str, device: Device) -> None:
        """Generate addon.xml for custom Pigeonhole skin"""
        addon_xml = self._create_addon_xml_content(device)
        
        with open(os.path.join(skin_dir, "addon.xml"), 'w', encoding='utf-8') as f:
            f.write(addon_xml)
    
    def _create_addon_xml_content(self, device: Device) -> str:
        """Create addon.xml content"""
        skin_id = f"skin.pigeonhole.{device.device_type.value}"
        device_desc = f"Optimized for {device.device_type.value.upper()} devices ({device.model})"
        
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<addon id="{skin_id}" version="1.0.0" name="{self.branding.name}" provider-name="Pigeonhole Media Solutions">
    <requires>
        <import addon="xbmc.gui" version="5.15.0"/>
        <import addon="script.skinshortcuts" version="0.4.0" optional="true"/>
        <import addon="script.embuary.helper" version="1.2.14" optional="true"/>
    </requires>
    <extension point="xbmc.gui.skin" defaultthemename="Textures.xbt" debugging="false">
        <res width="1920" height="1080" aspect="16:9" default="true" folder="1080i" />
    </extension>
    <extension point="xbmc.addon.metadata">
        <platform>all</platform>
        <license>Proprietary - Pigeonhole Media Solutions</license>
        <summary lang="en">{self.branding.tagline}</summary>
        <description lang="en">Professional corporate media center interface designed for enterprise deployments. {device_desc}. Features custom branding, optimized performance, and streamlined user experience.</description>
        <assets>
            <icon>icon.png</icon>
            <fanart>fanart.jpg</fanart>
            <screenshot>resources/screenshot-01.jpg</screenshot>
        </assets>
    </extension>
</addon>'''

    def _create_color_schemes(self, skin_dir: str):
        """Create custom color scheme files"""
        color_dir = os.path.join(skin_dir, "colors")
        Path(color_dir).mkdir(exist_ok=True)
        
        # Create default color scheme
        self._create_default_color_scheme(color_dir)
    
    def _create_default_color_scheme(self, color_dir: str):
        """Create default Pigeonhole color scheme"""
        colors = {
            'text_primary': self.branding.text_primary,
            'text_secondary': self.branding.text_secondary,
            'background': self.branding.background,
            'highlight': self.branding.primary_color,
            'success': '#10B981',
            'warning': '#F59E0B',
            'error': '#EF4444'
        }
        color_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<colors>
    <color name="White">{colors['text_primary']}</color>
    <color name="Black">{colors['background']}</color>
    <color name="Grey">{colors['text_secondary']}</color>
    <color name="Blue">{colors['highlight']}</color>
    <color name="Green">{colors['success']}</color>
    <color name="Orange">{colors['warning']}</color>
    <color name="Red">{colors['error']}</color>
    <color name="PigeonholeOrange">{self.branding.primary_color}</color>
    <color name="CorporateBlue">{self.branding.secondary_color}</color>
    <color name="AccentGreen">{self.branding.accent_color}</color>
</colors>'''
        
        with open(os.path.join(color_dir, "Pigeonhole.xml"), 'w', encoding='utf-8') as f:
            f.write(color_xml)
    
    def _create_custom_home_screen(self, skin_dir: str, device: Device):
        """Generate custom home screen layout"""
        home_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<window>
    <defaultcontrol>9000</defaultcontrol>
    <menucontrol>9000</menucontrol>
    <controls>
        
        <!-- Background -->
        <control type="image">
            <left>0</left>
            <top>0</top>
            <width>1920</width>
            <height>1080</height>
            <texture>colors/background.png</texture>
        </control>
        
        <!-- Header with Pigeonhole Branding -->
        <control type="group" id="9100">
            <left>0</left>
            <top>0</top>
            <width>1920</width>
            <height>120</height>
            
            <!-- Corporate Logo -->
            <control type="image">
                <left>60</left>
                <top>30</top>
                <width>200</width>
                <height>60</height>
                <texture>pigeonhole-logo.png</texture>
                <aspectratio>keep</aspectratio>
            </control>
            
            <!-- Corporate Title -->
            <control type="label">
                <left>280</left>
                <top>30</top>
                <width>800</width>
                <height>60</height>
                <font>font30</font>
                <textcolor>PigeonholeOrange</textcolor>
                <label>PIGEONHOLE MEDIA CENTER</label>
            </control>
            
            <!-- Time Display -->
            <control type="label">
                <left>1600</left>
                <top>30</top>
                <width>260</width>
                <height>60</height>
                <font>font24</font>
                <textcolor>White</textcolor>
                <align>right</align>
                <label>$INFO[System.Time]</label>
            </control>
        </control>
        
        <!-- Main Menu -->
        <control type="fixedlist" id="9000">
            <left>60</left>
            <top>180</top>
            <width>1800</width>
            <height>600</height>
            <onup>9000</onup>
            <ondown>9000</ondown>
            <onleft>9000</onleft>
            <onright>9000</onright>
            <orientation>horizontal</orientation>
            <focusposition>2</focusposition>
            <movement>2</movement>
            
            <itemlayout height="600" width="450">
                <control type="group">
                    <!-- Menu Item Background -->
                    <control type="image">
                        <left>20</left>
                        <top>20</top>
                        <width>410</width>
                        <height>560</height>
                        <texture border="8">colors/card_background.png</texture>
                    </control>
                    
                    <!-- Menu Item Icon -->
                    <control type="image">
                        <left>175</left>
                        <top>100</top>
                        <width>100</width>
                        <height>100</height>
                        <texture>$INFO[ListItem.Art(icon)]</texture>
                    </control>
                    
                    <!-- Menu Item Label -->
                    <control type="label">
                        <left>40</left>
                        <top>250</top>
                        <width>370</width>
                        <height>40</height>
                        <font>font20</font>
                        <textcolor>White</textcolor>
                        <align>center</align>
                        <label>$INFO[ListItem.Label]</label>
                    </control>
                    
                    <!-- Menu Item Description -->
                    <control type="textbox">
                        <left>60</left>
                        <top>320</top>
                        <width>330</width>
                        <height>200</height>
                        <font>font14</font>
                        <textcolor>Grey</textcolor>
                        <align>center</align>
                        <label>$INFO[ListItem.Label2]</label>
                    </control>
                </control>
            </itemlayout>
            
            <focusedlayout height="600" width="450">
                <control type="group">
                    <!-- Focused Item Background with Glow -->
                    <control type="image">
                        <left>15</left>
                        <top>15</top>
                        <width>420</width>
                        <height>570</height>
                        <texture border="12">colors/card_focus_glow.png</texture>
                        <colordiffuse>PigeonholeOrange</colordiffuse>
                        <animation effect="zoom" center="225,300" start="100" end="105" time="200">Focus</animation>
                        <animation effect="zoom" center="225,300" start="105" end="100" time="200">UnFocus</animation>
                    </control>
                    
                    <control type="image">
                        <left>20</left>
                        <top>20</top>
                        <width>410</width>
                        <height>560</height>
                        <texture border="8">colors/card_focus.png</texture>
                    </control>
                    
                    <!-- Focused Menu Item Icon -->
                    <control type="image">
                        <left>175</left>
                        <top>100</top>
                        <width>100</width>
                        <height>100</height>
                        <texture>$INFO[ListItem.Art(icon)]</texture>
                        <animation effect="zoom" center="50,50" start="100" end="110" time="200">Focus</animation>
                        <animation effect="zoom" center="50,50" start="110" end="100" time="200">UnFocus</animation>
                    </control>
                    
                    <!-- Focused Menu Item Label -->
                    <control type="label">
                        <left>40</left>
                        <top>250</top>
                        <width>370</width>
                        <height>40</height>
                        <font>font22</font>
                        <textcolor>PigeonholeOrange</textcolor>
                        <align>center</align>
                        <label>$INFO[ListItem.Label]</label>
                    </control>
                    
                    <!-- Focused Menu Item Description -->
                    <control type="textbox">
                        <left>60</left>
                        <top>320</top>
                        <width>330</width>
                        <height>200</height>
                        <font>font16</font>
                        <textcolor>White</textcolor>
                        <align>center</align>
                        <label>$INFO[ListItem.Label2]</label>
                    </control>
                </control>
            </focusedlayout>
        </control>
        
        <!-- Footer -->
        <control type="group">
            <left>0</left>
            <top>980</top>
            <width>1920</width>
            <height>100</height>
            
            <!-- Footer Background -->
            <control type="image">
                <left>0</left>
                <top>0</top>
                <width>1920</width>
                <height>100</height>
                <texture>colors/footer_background.png</texture>
            </control>
            
            <!-- Copyright Notice -->
            <control type="label">
                <left>60</left>
                <top>40</top>
                <width>800</width>
                <height>20</height>
                <font>font12</font>
                <textcolor>Grey</textcolor>
                <label>© 2025 Pigeonhole Media Solutions</label>
            </control>
            
            <!-- System Info -->
            <control type="label">
                <left>1400</left>
                <top>40</top>
                <width>460</width>
                <height>20</height>
                <font>font12</font>
                <textcolor>Grey</textcolor>
                <align>right</align>
                <label>$INFO[System.FriendlyName] • $INFO[Network.IPAddress]</label>
            </control>
        </control>
        
    </controls>
</window>'''

        home_xml_path = os.path.join(skin_dir, "1080i", "Home.xml")
        with open(home_xml_path, 'w', encoding='utf-8') as f:
            f.write(home_xml)

    def _create_custom_graphics(self, skin_dir: str, device: Device):
        """Generate custom graphics and branding assets"""
        try:
            media_dir = os.path.join(skin_dir, "media")
            colors_dir = os.path.join(media_dir, "colors")
            Path(colors_dir).mkdir(parents=True, exist_ok=True)
            
            self.logger.info(f"Creating custom graphics for {device.device_type.value}")
            
            # Create color-coded background images
            self._create_gradient_background(os.path.join(colors_dir, "background.png"))
            
            # Create card backgrounds with device-specific sizing
            card_size = self._get_optimal_card_size(device.device_type)
            self._create_card_background(os.path.join(colors_dir, "card_background.png"), card_size)
            self._create_card_background(os.path.join(colors_dir, "card_focus.png"), card_size, focused=True)
            self._create_card_glow(os.path.join(colors_dir, "card_focus_glow.png"), (card_size[0]+10, card_size[1]+10))
            
            # Create footer background
            self._create_footer_background(os.path.join(colors_dir, "footer_background.png"))
            
            # Create corporate logo
            self._create_corporate_logo(os.path.join(media_dir, "pigeonhole-logo.png"))
            
        except Exception as e:
            self.logger.error(f"Failed to create graphics: {e}")
            raise CustomizationError(f"Graphics creation failed: {e}")
        
    def _get_optimal_card_size(self, device_type: DeviceType) -> tuple:
        """Get optimal card size based on device type"""
        size_map = {
            DeviceType.FIRE_TV_STICK: (380, 520),  # Smaller for stick
            DeviceType.FIRE_TV_CUBE: (410, 560),   # Standard size
            DeviceType.NVIDIA_SHIELD: (450, 600),  # Larger for Shield
            DeviceType.FIRE_TV: (410, 560),        # Standard size
            DeviceType.ANDROID_TV: (410, 560)      # Standard size
        }
        return size_map.get(device_type, (410, 560))
    
    def _create_gradient_background(self, path: str):
        """Create gradient background with corporate colors"""
        try:
            img = Image.new('RGBA', (1920, 1080), color=self.branding.background)
            
            # Create subtle gradient overlay
            draw = ImageDraw.Draw(img)
            primary_hex = self.branding.primary_color.lstrip('#')
            
            for y in range(1080):
                alpha = int(30 * (y / 1080))  # Subtle gradient
                color = f"#{primary_hex}10"  # Very transparent
                draw.line([(0, y), (1920, y)], fill=color, width=1)
            
            img.save(path)
            self.logger.debug(f"Gradient background created: {path}")
            
        except Exception as e:
            self.logger.error(f"Failed to create gradient background: {e}")
            raise
        
    def _create_card_background(self, path: str, size: tuple, focused: bool = False):
        """Create card background with corporate styling"""
        try:
            base_color = '#2a2a2a' if not focused else '#3a3a3a'
            img = Image.new('RGBA', size, color=base_color)
            
            # Add border
            draw = ImageDraw.Draw(img)
            border_color = '#404040' if not focused else self.branding.primary_color
            draw.rectangle([0, 0, size[0]-1, size[1]-1], outline=border_color, width=2)
            
            img.save(path)
            self.logger.debug(f"Card background created: {path} ({'focused' if focused else 'normal'})")
            
        except Exception as e:
            self.logger.error(f"Failed to create card background: {e}")
            raise
        
    def _create_card_glow(self, path: str, size: tuple):
        """Create glow effect for focused cards"""
        try:
            img = Image.new('RGBA', size, color=(0, 0, 0, 0))
            
            draw = ImageDraw.Draw(img)
            primary_hex = self.branding.primary_color.lstrip('#')
            
            # Create glow effect
            for i in range(10):
                alpha = int(50 * (1 - i/10))
                color = (*bytes.fromhex(primary_hex), alpha)
                draw.rectangle([i, i, size[0]-1-i, size[1]-1-i], outline=color, width=1)
            
            img.save(path)
            self.logger.debug(f"Card glow created: {path}")
            
        except Exception as e:
            self.logger.error(f"Failed to create card glow: {e}")
            raise
        
    def _create_footer_background(self, path: str):
        """Create footer background with gradient"""
        try:
            img = Image.new('RGBA', (1920, 100), color='#0a0a0a')
            
            # Add gradient
            draw = ImageDraw.Draw(img)
            for y in range(100):
                alpha = int(100 * (1 - y/100))
                color = f"#000000{alpha:02x}"
                draw.line([(0, y), (1920, y)], fill=color, width=1)
            
            img.save(path)
            self.logger.debug(f"Footer background created: {path}")
            
        except Exception as e:
            self.logger.error(f"Failed to create footer background: {e}")
            raise
        
    def _create_corporate_logo(self, path: str):
        """Create corporate logo with text"""
        try:
            img = Image.new('RGBA', (200, 60), color=(0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Try to use custom font, fallback to default
            try:
                font = ImageFont.truetype("arial.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            # Draw company name from branding config
            company_name = self.branding.name.split()[0]  # First word only for logo
            draw.text((10, 20), company_name, fill=self.branding.primary_color, font=font)
            
            img.save(path)
            self.logger.debug(f"Corporate logo created: {path}")
            
        except Exception as e:
            self.logger.error(f"Failed to create corporate logo: {e}")
            raise
        
    def _create_custom_fonts(self, skin_dir: str):
        """Set up custom font configuration"""
        font_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<fonts>
    <fontset id="Default">
        <font>
            <name>font10</name>
            <filename>Roboto-Regular.ttf</filename>
            <size>10</size>
        </font>
        <font>
            <name>font12</name>
            <filename>Roboto-Regular.ttf</filename>
            <size>12</size>
        </font>
        <font>
            <name>font14</name>
            <filename>Roboto-Regular.ttf</filename>
            <size>14</size>
        </font>
        <font>
            <name>font16</name>
            <filename>Roboto-Regular.ttf</filename>
            <size>16</size>
        </font>
        <font>
            <name>font20</name>
            <filename>Roboto-Medium.ttf</filename>
            <size>20</size>
        </font>
        <font>
            <name>font22</name>
            <filename>Roboto-Medium.ttf</filename>
            <size>22</size>
        </font>
        <font>
            <name>font24</name>
            <filename>Roboto-Medium.ttf</filename>
            <size>24</size>
        </font>
        <font>
            <name>font30</name>
            <filename>Roboto-Bold.ttf</filename>
            <size>30</size>
        </font>
    </fontset>
</fonts>'''

        font_xml_path = os.path.join(skin_dir, "1080i", "Font.xml")
        with open(font_xml_path, 'w', encoding='utf-8') as f:
            f.write(font_xml)
            
    def package_skin(self, skin_dir: str, output_path: str):
        """Package the custom skin into a zip file"""
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(skin_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_path = os.path.relpath(file_path, skin_dir)
                    zipf.write(file_path, f"skin.pigeonhole.corporate/{arc_path}")
                    
    def create_custom_addon_package(self, addon_list: List[str]) -> str:
        """Create custom addon package with pre-configured addons"""
        package_dir = f"{self.temp_dir}/addon_package"
        Path(package_dir).mkdir(exist_ok=True)
        
        for addon_id in addon_list:
            # Download or copy addon
            addon_path = self.get_addon(addon_id)
            if addon_path:
                shutil.copy2(addon_path, f"{package_dir}/{addon_id}.zip")
        
        # Create installation script
        install_script = self.generate_addon_install_script(addon_list)
        with open(f"{package_dir}/install_addons.py", 'w') as f:
            f.write(install_script)
            
        return package_dir
        
    def generate_addon_install_script(self, addon_list: List[str]) -> str:
        """Generate script to automatically install addons"""
        return f'''#!/usr/bin/env python3
"""
Automated addon installation for Pigeonhole deployment
"""
import subprocess
import os

def install_addons(device_ip):
    """Install all addons to target device"""
    addons = {addon_list}
    
    for addon in addons:
        print(f"Installing {{addon}}...")
        subprocess.run([
            "adb", "-s", f"{{device_ip}}:5555", "push", 
            f"{{addon}}.zip", 
            f"/storage/emulated/0/Android/data/org.xbmc.kodi/files/.kodi/addons/{{addon}}.zip"
        ])
        
        # Extract addon
        subprocess.run([
            "adb", "-s", f"{{device_ip}}:5555", "shell",
            f"cd /storage/emulated/0/Android/data/org.xbmc.kodi/files/.kodi/addons && unzip -o {{addon}}.zip"
        ])
    
    print("All addons installed successfully!")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        install_addons(sys.argv[1])
    else:
        print("Usage: python install_addons.py <device_ip>")
'''
        
    def get_addon(self, addon_id: str) -> Optional[str]:
        """Download or locate addon file"""
        # This would implement addon downloading logic
        # For now, return None - would need actual implementation
        return None

def main():
    """Main function with proper error handling"""
    import time
    from pigeonhole_device_manager import create_device_manager
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("🎨 Pigeonhole Advanced Customization System")
        logger.info("=" * 50)
        
        # Initialize components
        customizer = PigeonholeCustomizer()
        device_manager = create_device_manager()
        config = get_config()
        
        # Discover devices
        logger.info("Discovering devices...")
        devices = device_manager.discover_devices()
        
        if not devices:
            logger.warning("No devices found. Please check network connectivity.")
            return
        
        logger.info(f"Found {len(devices)} devices")
        
        # Process each device
        for device in devices:
            try:
                logger.info(f"Processing device: {device.name} ({device.ip})")
                
                # Create custom skin for device
                skin_path = customizer.create_custom_skin(device)
                logger.info(f"✅ Custom skin created: {skin_path}")
                
                # Create addon package for device
                streaming_config = config.get_streaming_config()
                essential_addons = streaming_config.get('essential_addons', [])
                
                if essential_addons:
                    addon_package = customizer.create_custom_addon_package(essential_addons, device)
                    logger.info(f"✅ Addon package created: {addon_package}")
                
            except Exception as e:
                logger.error(f"Failed to process device {device.name}: {e}")
                continue
        
        logger.info("✅ Customization process completed successfully!")
        
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
    except Exception as e:
        logger.error(f"Customization process failed: {e}")
        raise
    finally:
        # Cleanup would happen automatically via context managers
        logger.info("Cleanup completed")

# Usage example
if __name__ == "__main__":
    main()