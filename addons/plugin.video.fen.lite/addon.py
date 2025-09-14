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
        
        # My Lists
        listitem = xbmcgui.ListItem('My Lists')
        listitem.setArt({'icon': 'DefaultPlaylist.png'})
        xbmcplugin.addDirectoryItem(
            handle=int(sys.argv[1]),
            url=f'{sys.argv[0]}?action=mylists',
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
        listitem = xbmcgui.ListItem('Real Debrid Tools')
        listitem.setArt({'icon': 'DefaultAddonService.png'})
        xbmcplugin.addDirectoryItem(
            handle=int(sys.argv[1]),
            url=f'{sys.argv[0]}?action=tools',
            listitem=listitem,
            isFolder=True
        )
        
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
        xbmcgui.Dialog().notification(
            'FEN Lite',
            'Fire TV optimized streaming ready',
            xbmcgui.NOTIFICATION_INFO,
            3000
        )
        
    except Exception as e:
        xbmc.log(f'FEN Lite Error: {str(e)}', xbmc.LOGERROR)

if __name__ == '__main__':
    main()