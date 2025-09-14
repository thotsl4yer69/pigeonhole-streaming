import xbmc
import xbmcgui
import xbmcplugin
import sys

def main():
    try:
        xbmcplugin.setContent(int(sys.argv[1]), 'videos')
        
        # Movies section
        listitem = xbmcgui.ListItem('Movies')
        listitem.setArt({'icon': 'DefaultMovies.png'})
        xbmcplugin.addDirectoryItem(
            handle=int(sys.argv[1]),
            url=f'{sys.argv[0]}?action=movies',
            listitem=listitem,
            isFolder=True
        )
        
        # TV Shows section
        listitem = xbmcgui.ListItem('TV Shows')
        listitem.setArt({'icon': 'DefaultTVShows.png'})
        xbmcplugin.addDirectoryItem(
            handle=int(sys.argv[1]),
            url=f'{sys.argv[0]}?action=tvshows',
            listitem=listitem,
            isFolder=True
        )
        
        # Real Debrid Tools
        listitem = xbmcgui.ListItem('Real Debrid Tools')
        listitem.setArt({'icon': 'DefaultAddonService.png'})
        xbmcplugin.addDirectoryItem(
            handle=int(sys.argv[1]),
            url=f'{sys.argv[0]}?action=realdebrid',
            listitem=listitem,
            isFolder=True
        )
        
        # Settings
        listitem = xbmcgui.ListItem('Settings')
        listitem.setArt({'icon': 'DefaultAddonProgram.png'})
        xbmcplugin.addDirectoryItem(
            handle=int(sys.argv[1]),
            url=f'{sys.argv[0]}?action=settings',
            listitem=listitem,
            isFolder=False
        )
        
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
        # Show notification
        xbmcgui.Dialog().notification(
            'The Crew',
            'Ready for streaming with Real Debrid',
            xbmcgui.NOTIFICATION_INFO,
            3000
        )
        
    except Exception as e:
        xbmc.log(f'The Crew Error: {str(e)}', xbmc.LOGERROR)

if __name__ == '__main__':
    main()