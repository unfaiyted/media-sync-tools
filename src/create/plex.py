import uuid
from datetime import datetime
from typing import List

from plexapi.playlist import Playlist
from plexapi.server import PlexServer

from src.models.filters import PlexFilters, FilterType
from src.models import MediaListType, MediaList
from src.create import ListBuilder
from src.config import ConfigManager


def get_all_collections(plex):
    collections = []
    for library in plex.library.sections():
        if hasattr(library, 'collections'):
            collections.extend(library.collections())
    return collections


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
            }, {
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


async def sync_plex_lists(config: ConfigManager):
    await sync_plex_collections(config)
    await sync_plex_playlists(config)


async def sync_plex_collections(config: ConfigManager):
    plex: PlexServer = config.get_client('plex')

    # Get all collections from Plex
    plex_collections = get_all_collections(plex)
    print('Plex Collections ======================')
    # print(plex_collections)

    for plex_collection in plex_collections:
        filters = {
            'filtersId': str(uuid.uuid4()),
            'clientId': 'plex',
            'filterType': FilterType.PLEX,
            'listId': plex_collection.ratingKey,
            'listType': MediaListType.COLLECTION,
        }

        mediaList = {
            'mediaListId': str(uuid.uuid4()),
            'name': plex_collection.title,
            'type': MediaListType.COLLECTION,
            'description': plex_collection.summary,
            'sortName': plex_collection.title,
            'clientId': 'plex',
            'createdAt': datetime.now(),
            'creatorId': 'USERID',
            'items': [],
            'filters': filters
        }

        media_list: MediaList = MediaList(**mediaList)

        # print(media_list, 'MEDIA LIST')
        print(media_list.filters, 'FILTERS')

        list = ListBuilder(config, list_type=MediaListType.COLLECTION, media_list=media_list)
        await list.build()


async def sync_plex_sample_searches(config: ConfigManager):
    eighties_sci_fi = PlexFilters(
        filterType=FilterType.PLEX,
        clientId='plex',
        filtersId=str(uuid.uuid4()),
        library="Movies",
        type="movie",
        decade=1980,
        genre="Sci-Fi",
        sort="year",
        limit=50
    )

    nolan_zimmer = PlexFilters(
        filterType=FilterType.PLEX,
        clientId='plex',
        filtersId=str(uuid.uuid4()),
        library="Movies",
        type="movie",
        director="Christopher Nolan",
        actor="Hans Zimmer",
        sort="year",
        limit=10
    )
    hd_action_2000s = PlexFilters(
        filterType=FilterType.PLEX,
        clientId='plex',
        filtersId=str(uuid.uuid4()),
        library="Movies",
        type="movie",
        decade=2000,
        genre="Action",
        resolution="1080p",
        audioChannels="5.1",
        sort="rating",
        limit=25
    )
    hbo_shows = PlexFilters(
        filterType=FilterType.PLEX,
        clientId='plex',
        filtersId=str(uuid.uuid4()),
        library="TV Shows",
        type="show",
        studio="HBO",
        sort="titleSort",
        limit=20
    )

    filters = [eighties_sci_fi, nolan_zimmer, hd_action_2000s, hbo_shows]

    media_lists = [MediaList(
        mediaListId=str(uuid.uuid4()),
        name=filters[0].genre + " from the 80s",
        type=MediaListType.COLLECTION,
        description="Sci-Fi movies from the 80s",
        sortName=filters[0].genre + " from the 80s",
        clientId='plex',
        createdAt=datetime.now(),
        creatorId='USERID',
        items=[],
        filters=filters[0]
    ), MediaList(
        mediaListId=str(uuid.uuid4()),
        name="Nolan and Zimmer",
        type=MediaListType.COLLECTION,
        description="Movies directed by Christopher Nolan and scored by Hans Zimmer",
        sortName="Nolan and Zimmer",
        clientId='plex',
        createdAt=datetime.now(),
        creatorId='USERID',
        items=[],
        filters=filters[1]
    ), MediaList(
        mediaListId=str(uuid.uuid4()),
        name="HD Action Movies from the 2000s",
        type=MediaListType.COLLECTION,
        description="HD Action Movies from the 2000s",
        sortName="HD Action Movies from the 2000s",
        clientId='plex',
        createdAt=datetime.now(),
        creatorId='USERID',
        items=[],
        filters=filters[2]

    #), MediaList(
    #     mediaListId=str(uuid.uuid4()),
    #     name="HBO Shows",
    #     type=MediaListType.COLLECTION,
    #     description="HBO Shows",
    #     sortName="HBO Shows",
    #     clientId='plex',
    #     createdAt=datetime.now(),
    #     creatorId='USERID',
    #     items=[],
    #     filters=filters[3]
    )]

    for media_list in media_lists:
        list = ListBuilder(config, list_type=MediaListType.COLLECTION, media_list=media_list)
        await list.build()
