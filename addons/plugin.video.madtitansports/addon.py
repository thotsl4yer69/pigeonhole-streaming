import xbmc
import xbmcgui
import xbmcplugin
import sys

def main():
    try:
        xbmcplugin.setContent(int(sys.argv[1]), 'videos')
        
        # Live Sports
        listitem = xbmcgui.ListItem('Live Sports')
        listitem.setArt({'icon': 'DefaultTVShows.png'})
        xbmcplugin.addDirectoryItem(
            handle=int(sys.argv[1]),
            url=f'{sys.argv[0]}?action=live',
            listitem=listitem,
            isFolder=True
        )
        
        # NFL
        listitem = xbmcgui.ListItem('NFL')
        listitem.setArt({'icon': 'DefaultMovies.png'})
        xbmcplugin.addDirectoryItem(
            handle=int(sys.argv[1]),
            url=f'{sys.argv[0]}?action=nfl',
            listitem=listitem,
            isFolder=True
        )
        
        # NBA
        listitem = xbmcgui.ListItem('NBA')
        listitem.setArt({'icon': 'DefaultMovies.png'})
        xbmcplugin.addDirectoryItem(
            handle=int(sys.argv[1]),
            url=f'{sys.argv[0]}?action=nba',
            listitem=listitem,
            isFolder=True
        )
        
        # Soccer
        listitem = xbmcgui.ListItem('Soccer')
        listitem.setArt({'icon': 'DefaultMovies.png'})
        xbmcplugin.addDirectoryItem(
            handle=int(sys.argv[1]),
            url=f'{sys.argv[0]}?action=soccer',
            listitem=listitem,
            isFolder=True
        )
        
        # Schedule
        listitem = xbmcgui.ListItem('Today\'s Schedule')
        listitem.setArt({'icon': 'DefaultAddonProgram.png'})
        xbmcplugin.addDirectoryItem(
            handle=int(sys.argv[1]),
            url=f'{sys.argv[0]}?action=schedule',
            listitem=listitem,
            isFolder=True
        )
        
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
        xbmcgui.Dialog().notification(
            'Mad Titan Sports',
            'Live sports streaming ready',
            xbmcgui.NOTIFICATION_INFO,
            3000
        )
        
    except Exception as e:
        xbmc.log(f'Mad Titan Sports Error: {str(e)}', xbmc.LOGERROR)

if __name__ == '__main__':
    main()