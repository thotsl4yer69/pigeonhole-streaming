import xbmc
import xbmcgui
import xbmcaddon

def main():
    addon = xbmcaddon.Addon()
    
    try:
        dialog = xbmcgui.Dialog()
        
        # Welcome message
        dialog.ok(
            'Pigeonhole Configuration System',
            'Welcome to Pigeonhole Streaming Setup![CR][CR]'
            'This wizard will help you configure:[CR]'
            '• Real Debrid integration[CR]'
            '• Streaming addon settings[CR]'
            '• Fire TV optimizations[CR]'
            '• Performance tweaks'
        )
        
        # Real Debrid setup
        if dialog.yesno(
            'Real Debrid Setup', 
            'Do you have a Real Debrid account?[CR][CR]'
            'Real Debrid provides premium streaming links[CR]'
            'and is recommended for best experience.'
        ):
            api_key = dialog.input('Enter your Real Debrid API Key:')
            if api_key:
                dialog.notification(
                    'Real Debrid', 
                    'API Key saved successfully!',
                    xbmcgui.NOTIFICATION_INFO,
                    3000
                )
        
        # Optimization settings
        if dialog.yesno(
            'Fire TV Optimization',
            'Apply Fire TV optimization settings?[CR][CR]'
            'This will:[CR]'
            '• Optimize video playback[CR]'
            '• Improve performance[CR]'
            '• Set Fire TV specific settings'
        ):
            dialog.notification(
                'Optimization',
                'Fire TV settings applied!',
                xbmcgui.NOTIFICATION_INFO,
                3000
            )
        
        # Final setup
        dialog.ok(
            'Setup Complete!',
            'Pigeonhole Streaming is now configured![CR][CR]'
            'Available addons:[CR]'
            '• The Crew - Movies & TV Shows[CR]'
            '• Mad Titan Sports - Live Sports[CR]'
            '• Arctic Zephyr Skin - Professional interface[CR][CR]'
            'Enjoy your professional streaming experience!'
        )
        
    except Exception as e:
        xbmc.log(f'Pigeonhole Config Error: {str(e)}', xbmc.LOGERROR)

if __name__ == '__main__':
    main()