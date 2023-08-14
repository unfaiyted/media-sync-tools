from src.config import ConfigManager
from src.create.toplists import sync_top_lists
from src.sync.watchlist import sync_watchlist
from src.sync.collections import sync_collections
from src.create.lists import Lists
from src.create.trakt import sync_trakt_user_lists
from src.create.playlists import create_emby_playlist

from starlette.responses import JSONResponse
from fastapi import APIRouter

router = APIRouter()
config_manager = ConfigManager.get_manager()


@router.get("/watchlist")
async def trigger_sync_watchlist():
    try:
        sync_watchlist(config_manager)
        list_maker = Lists(config_manager)
        list_maker.create_previously_watchedlist()

        return JSONResponse(status_code=200, content={"message": "Sync watchlist started successfully."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@router.get("/playlist")
async def trigger_sync_playlist():
    try:

        name = 'Sleeping Shows'

        shows = [
            'How I Met Your Mother',
            'Ancient Aliens',
            'Bob\'s Burgers',
            'Bojack Horseman',
            'Forensic Files',
            'Downton Abbey',
            'Parks and Recreation',
            '30 Rock',
            'Daria',
            'Better Off Ted',
            'The Good Place',
            'The Office (US)',
            'Friends',
            'Rick and Morty'
        ]

        create_emby_playlist(config_manager, name, shows)

        return JSONResponse(status_code=200, content={"message": "Sync watchlist started successfully."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@router.get("/top-lists")
async def trigger_sync_toplist():
    try:
        sync_top_lists(config_manager)

        return JSONResponse(status_code=200, content={"message": "Sync watchlist started successfully."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@router.get("/collections")
async def trigger_sync_collection():
    settings = config_manager.get_collection_settings()

    try:

        print('Syncing Collections', settings['sync'])
        if settings['sync']:
            print("Sync collection is enabled.")
            sync_collections(config_manager)
        else:
            print("Sync collection is disabled.")

        return JSONResponse(status_code=200, content={"message": "Sync collections successfully."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@router.get('/trakt')
async def handle_trakt():
    try:

        sync_trakt_user_lists(config_manager, 'faiyt')

        return JSONResponse(status_code=200, content={"message": "User lists synced from Trakt", })
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@router.get('/config')
async def handle_config():
    # get playlist from config

    # get collections from config
    collections = config_manager.collections.get('lists', {})

    playlists = config_manager.playlists.get('lists', {})

    # for collection in collections:
    #     print(collections[collection])
    #     list = ListBuilder(config_manager, "Collection", collections[collection])
    #     list.build()

    # for playlist in playlists:

    # list = ListBuilder(config_manager, "Playlist", playlists[playlist])
    # list.build()

    return JSONResponse(status_code=200, content={"message": "Config started successfully.", "collections": collections,
                                                  "playlists": playlists})
