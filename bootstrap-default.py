#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import xbmc
import xbmcaddon
import xbmcvfs
import xbmcgui

def install_repository():
    """Install Pigeonhole repository directly via Python"""
    
    addon = xbmcaddon.Addon()
    addon_path = xbmc.translatePath(addon.getAddonInfo('path'))
    
    # Target repository directory
    repo_path = xbmc.translatePath('special://home/addons/repository.pigeonhole/')
    
    # Create directory
    if not xbmcvfs.exists(repo_path):
        xbmcvfs.mkdirs(repo_path)
    
    # Repository addon.xml content
    repo_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<addon id="repository.pigeonhole" name="Pigeonhole Repository" version="1.0.0" provider-name="Pigeonhole Project">
    <extension point="xbmc.addon.repository" name="Pigeonhole Repository">
        <dir minversion="19.0.0">
            <info compressed="false">https://raw.githubusercontent.com/pigeonhole-project/repository/main/addons.xml</info>
            <checksum>https://raw.githubusercontent.com/pigeonhole-project/repository/main/addons.xml.md5</checksum>
            <datadir zip="true">https://raw.githubusercontent.com/pigeonhole-project/repository/main/repo/</datadir>
        </dir>
    </extension>
    <extension point="xbmc.addon.metadata">
        <summary lang="en">Pigeonhole Streaming Repository</summary>
        <description lang="en">Australian-focused streaming addons with Surfshark VPN integration</description>
        <platform>all</platform>
        <license>MIT</license>
    </extension>
</addon>'''
    
    # Write addon.xml
    addon_xml_path = os.path.join(repo_path, 'addon.xml')
    with open(addon_xml_path, 'w', encoding='utf-8') as f:
        f.write(repo_xml)
    
    # Notify user
    xbmcgui.Dialog().notification('Pigeonhole Bootstrap', 'Repository installed successfully!', xbmcgui.NOTIFICATION_INFO, 5000)
    
    # Trigger addon scan
    xbmc.executebuiltin('UpdateLocalAddons')
    xbmc.executebuiltin('UpdateAddonRepos')

if __name__ == '__main__':
    install_repository()