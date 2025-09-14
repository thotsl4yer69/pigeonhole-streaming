import xbmc
import xbmcgui
import xbmcplugin
import sys

def main():
    try:
        # Create test menu
        xbmcplugin.setContent(int(sys.argv[1]), 'videos')
        
        # Add test item
        listitem = xbmcgui.ListItem('Pigeonhole Test - Setup Working!')
        listitem.setInfo('video', {'title': 'Pigeonhole Test', 'plot': 'Congratulations! Your Pigeonhole Streaming setup is working correctly.'})
        
        xbmcplugin.addDirectoryItem(
            handle=int(sys.argv[1]),
            url='plugin://plugin.video.pigeonhole.test/?action=test',
            listitem=listitem,
            isFolder=False
        )
        
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
        # Show success notification
        xbmcgui.Dialog().notification(
            'Pigeonhole Streaming',
            'Setup verification successful!',
            xbmcgui.NOTIFICATION_INFO,
            3000
        )
        
    except Exception as e:
        xbmc.log(f'Pigeonhole Test Error: {str(e)}', xbmc.LOGERROR)

if __name__ == '__main__':
    main()