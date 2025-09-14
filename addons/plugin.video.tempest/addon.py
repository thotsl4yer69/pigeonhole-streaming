import xbmc
import xbmcgui
import xbmcplugin
import sys

def main():
    try:
        xbmcplugin.setContent(int(sys.argv[1]), 'videos')
        
        # Movies
        listitem = xbmcgui.ListItem('Movies')
        listitem.setArt({'icon': 'DefaultMovies.png'})
        xbmcplugin.addDirectoryItem(
            handle=int(sys.argv[1]),
            url=f'{sys.argv[0]}?action=movies',
            listitem=listitem,
            isFolder=True
        )
        
        # TV Shows
        listitem = xbmcgui.ListItem('TV Shows')
        listitem.setArt({'icon': 'DefaultTVShows.png'})
        xbmcplugin.addDirectoryItem(
            handle=int(sys.argv[1]),
            url=f'{sys.argv[0]}?action=tvshows',
            listitem=listitem,
            isFolder=True
        )
        
        # Search
        listitem = xbmcgui.ListItem('Search')
        listitem.setArt({'icon': 'DefaultAddonsSearch.png'})
        xbmcplugin.addDirectoryItem(
            handle=int(sys.argv[1]),
            url=f'{sys.argv[0]}?action=search',
            listitem=listitem,
            isFolder=True
        )
        
        # Tools
        listitem = xbmcgui.ListItem('Tools')
        listitem.setArt({'icon': 'DefaultAddonService.png'})
        xbmcplugin.addDirectoryItem(
            handle=int(sys.argv[1]),
            url=f'{sys.argv[0]}?action=tools',
            listitem=listitem,
            isFolder=True
        )
        
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
        xbmcgui.Dialog().notification(
            'Tempest',
            'Streaming addon ready',
            xbmcgui.NOTIFICATION_INFO,
            3000
        )
        
    except Exception as e:
        xbmc.log(f'Tempest Error: {str(e)}', xbmc.LOGERROR)

if __name__ == '__main__':
    main()