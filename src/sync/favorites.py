from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
from utils.emby import Emby

from config import ConfigManager

config = ConfigManager()

plex = config.get_client('plex')
emby = config.get_client('emby')


# EMBY
# emby_server_url = 'http://192.168.0.120:8096'
# username = 'Faiyt'
# api_key = 'b16d19b536094363a902347ee455d0a7'
# emby = Emby(emby_server_url, username, api_key)
#
# # PLEX
# PLEX_SERVER_URL = 'http://192.168.0.120:32400'
# PLEX_ACCESS_TOKEN = 'NtvJEgd6zMY8CZ2BLsyx'
#
# Instantiate a PlexServer instance
# plex = PlexServer(PLEX_SERVER_URL, PLEX_ACCESS_TOKEN)

# Get all libraries in Plex
plex_libraries = plex.library.sections()

# Loop through all libraries and all items in each library
for library in plex_libraries:
    print(f"Processing library: {library.title}")
    for item in library.all():
        print(f"Processing item: {item.title}")
        # Check if the item is a favorite in Plex
        if item.isFavorite:
            # Search for the item in Emby
            emby_item = emby.search(item.title)[0]
            print('Emby item: ', emby_item)
            # Add the item to Emby favorites
            emby.set_favorite(emby_item['Id'])
            print(f"Added {item.title} to Emby favorites")
