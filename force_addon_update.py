import xbmc
import xbmcgui
import xbmcaddon

# Force Kodi to update local addons
xbmc.executebuiltin('UpdateLocalAddons')

# Show notification
xbmcgui.Dialog().notification('Pigeonhole Repository', 'Addon update initiated', xbmcgui.NOTIFICATION_INFO, 5000)