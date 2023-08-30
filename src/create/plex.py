from typing import List

from plexapi.playlist import Playlist
from plexapi.server import PlexServer

from src.models import MediaListType
from src.create import ListBuilder
from src.config import ConfigManager

def get_all_collections(plex):
    collections = []
    for library in plex.library.sections():
        if hasattr(library, 'collections'):
            collections.extend(library.collections())
    return collections


async def sync_plex_collections(config: ConfigManager):
    plex: PlexServer = config.get_client('plex')
    mdb = config.get_client('mdb')

    # Get all collections from Plex
    plex_collections = get_all_collections(plex)
    print('Plex Collections ======================')
    # print(plex_collections)

    for plex_collection in plex_collections:
        print(plex_collection.title, plex_collection.ratingKey, plex_collection.summary, plex_collection.items())
        details = {
            'name': plex_collection.title,
            'description': plex_collection.summary,
            'provider': 'plex',
            'filters': [{
                'type': 'list_id',
                'value': plex_collection.ratingKey
            },{
                'type': 'list_type',
                'value': MediaListType.COLLECTION
            }],
            'include': ['Movies'],
            'options': {
                'add_prev_watched': False,
                'add_missing_to_library': False,
                'limit': 100,
                'sort': 'title',
                'poster': {
                    'enabled': True,
                    'bg_image_query': plex_collection.title
                }
            }
        }

        list = ListBuilder(config, list_type=MediaListType.COLLECTION, list=details)
        await list.build()

async def sync_plex_playlists(config: ConfigManager):
    plex: PlexServer = config.get_client('plex')

    # Get all playlists from Plex
    plex_playlists: List[Playlist] = plex.playlists()
    print('Plex Playlists ======================')

    for plex_playlist in plex_playlists:
        print(plex_playlist.title, plex_playlist.ratingKey, plex_playlist.summary, plex_playlist.items())
        details = {
            'name': plex_playlist.title,
            'description': plex_playlist.summary,
            'provider': 'plex',
            'filters': [{
                'type': 'list_id',
                'value': plex_playlist.title
             },{
                'type': 'list_type',
                'value': MediaListType.PLAYLIST
            }],
            'include': ['Movies'],
            'options': {
                'add_prev_watched': False,
                'add_missing_to_library': False,
                'limit': 100,
                'sort': 'title',
                'poster': {
                    'enabled': True,
                    'bg_image_query': plex_playlist.title
                }
            }
        }

        list = ListBuilder(config, list_type=MediaListType.PLAYLIST, list=details)
        await list.build()
