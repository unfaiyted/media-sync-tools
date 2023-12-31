import asyncio
from motor.motor_asyncio import AsyncIOMotorDatabase
from starlette.background import BackgroundTasks

from src.create.plex import sync_plex_collections, sync_plex_playlists, sync_plex_sample_searches
from src.db.queries import media_list_queries
from src.create import ListBuilder
from src.models.configs import SyncOptions
from src.models import MediaList, MediaListType, MediaListOptions
from src.config import ConfigManager
from src.create.toplists import sync_top_lists
from src.sync.collections import sync_collections, emby_to_plex_sync_collection
from src.create.lists import Lists
from src.create.trakt import sync_trakt_user_lists, sync_trakt_popular_lists, sync_trakt_trending_lists
from src.create.playlists import create_emby_playlist

from starlette.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException

from src.tasks.tasks import sync_libraries_from_provider, sync_all_collections_from_provider, \
    sync_media_list_to_provider

router = APIRouter()
config = ConfigManager.get_manager()


@router.get("/watched")
async def trigger_sync_watchlist():
    try:
        # sync_watchlist(config)
        config = ConfigManager.get_manager()
        list_maker = Lists(config)
        list_maker.create_previously_watchedlist()

        return JSONResponse(status_code=200, content={"message": "Sync watchlist started successfully."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@router.get("/playlists")
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

        create_emby_playlist(config, name, shows)

        return JSONResponse(status_code=200, content={"message": "Sync watchlist started successfully."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@router.get("/topLists")
async def trigger_sync_toplist():
    try:
        await sync_top_lists(config)

        return JSONResponse(status_code=200, content={"message": "Sync watchlist started successfully."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@router.get("/collections")
async def trigger_sync_collection():
    settings = config.get_collection_settings()
    emby_to_plex_sync_collection(config)
    try:

        print('Syncing Collections', settings['sync'])
        if settings['sync']:
            print("Sync collection is enabled.")
            sync_collections(config)
        else:
            print("Sync collection is disabled.")

        return JSONResponse(status_code=200, content={"message": "Sync collections successfully."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@router.get("/libraries")
async def trigger_sync_libraries():
    try:
        await sync_libraries_from_provider(config)

        return JSONResponse(status_code=200, content={"message": "Sync libraries successfully."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@router.get("/plex")
async def trigger_sync_plex():
    try:
        # await sync_plex_collections(config)
        #await sync_plex_playlists(config)
        await sync_plex_sample_searches(config)

        return JSONResponse(status_code=200, content={"message": "Sync plex libraries successfully."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@router.get('/trakt')
async def handle_trakt():
    try:

        # await sync_trakt_user_lists(config, 'faiyt')
        await sync_trakt_popular_lists(config)
        await sync_trakt_trending_lists(config)

        return JSONResponse(status_code=200, content={"message": "User lists synced from Trakt", })
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@router.get('/ratings')
async def handle_ratings(background_tasks: BackgroundTasks):
    try:

        # Create new list with listBuilder
        # details = {
        #     'name': 'Emby Provider Test',
        #     'description': 'This is a test.',  # assuming the description might be optional
        #     'provider': 'emby',
        #     'type': MediaListType.COLLECTION,
        #     'filters': [{
        #         'type': 'list_id',
        #         'value': 168737
        #     }],
        #     'include': ['Movies'],  # assuming lists are for movies only, adjust if necessary
        #     'options': {
        #         'add_prev_watched': False,
        #         'add_missing_to_library': False,
        #         'limit': 100,  # adjust as necessary
        #         'sort': 'rank',  # adjust as necessary
        #         'poster': {
        #             'enabled': True,
        #         }
        #     }
        # }

        def run_in_thread(task, *args, **kwargs):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(task(*args, **kwargs))

        # background_tasks.add_task(await sync_all_collecions_from_provider(payload=None), name="sync_all_lists_from_provider")

        # payload = {
        #     'list_id': '9bab7eeb-fa54-4061-baa0-c1ec99ec95dd',
        # }

        # await sync_all_collections_from_provider(payload=None)
        # await sync_media_list_to_provider(payload)
        # Here, I'm assuming you want to process movie lists only. Adjust this if lists can be for other media types too.
        # list_builder = ListBuilder(config, list=details)
        # await list_builder.build()

        details = {
            "name": "Newly__ Popular Movies",
            "sort_name": "!001_Newly Popular Movies",
            "provider": "tmdb",
            "filters": [
                {"type": "sort_by", "value": "popularity.desc"},
                {"type": "page", "value": "1"},
                {"type": "language", "value": "en-US"},
                {"type": "vote_average.gte", "value": "6"}
            ],
            "include": ["Movies"],
            "options": {
                "add_prev_watched": False,
                "add_missing_to_library": True,
                "limit": 50,
                "sort": "random",
                "poster": {
                    "enabled": True,
                    "bg_image_query": 'awesome people'
                    # "icon": False,
                    # "icon_path": '/resources/icons/mdb.png'
                }
            }
        }

        list_builder = ListBuilder(config, list=details)
        list_builder = await list_builder.build()
        list_builder = await list_builder.sync('emby')

        return JSONResponse(status_code=200, content={"message": "Test completed", })
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


# Sync list to ConfiguredClient
@router.get('/list/{list_id}/client/{client_id}', response_model=MediaList)
async def sync_list_to_client(list_id: str, client_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    list_item = await db.media_lists.find_one({"mediaListId": list_id})
    if list_item is None:
        raise HTTPException(status_code=404, detail="List not found")

    client = config.get_client(client_id)

    # TODO: implement logic to get list and sync to client
    print('Syncing list to client', list_item, client)

    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")


@router.post("/list/", response_model=MediaListOptions)
async def sync_media_list_to_provider(payload: MediaListOptions, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    # Add a record to the database if it doesn't exist for MediaListOptions each user should have a unique record
    # for each list they want to sync.


    # Check which clients are selected for sync. We will loop over each client and sync the list to that client.

    # Collection where MediaListOptions are stored
    collection = db.media_list_options

    # Assuming you have user_id and list_name as unique identifiers in your model
    existing_record = await collection.find_one({
        "userId": payload.userId,
        "mediaListId": payload.mediaListId
    })

    if not existing_record:
        # If the record doesn't exist, insert it
        await collection.insert_one(payload.dict())

    if existing_record:
        # If the record exists, update it
        payload.mediaListOptionsId = existing_record['mediaListOptionsId']

        await collection.replace_one({
            "userId": payload.userId,
            "mediaListId": payload.mediaListId
        }, payload.dict())

    # Fetch the clients for syncing. Assuming this is a field in your MediaListOptions model.
    clients_to_sync = payload.clients

    # get media list based on mediaListId
    media_list = await media_list_queries.get_media_list_with_items(db, payload.mediaListId)
    media_list = MediaList(**media_list)


    print(f'Found {len(clients_to_sync)} clients to sync to.')
    print(f'Found {len(media_list.items)} items to sync.')

    # Loop over clients and sync
    for client in clients_to_sync:
        # print(client)
        list = ListBuilder(config, media_list=media_list)
        print(f'Syncing list to client {client.client.name}')
        await list.sync(client.client.name.lower())


        #   Your syncing logic here. For example:
        # await sync_to_client(client, payload)
    return payload


# CRUD operations for SyncOptions
@router.post("/options/", response_model=SyncOptions)
async def create_sync_options(sync_option: SyncOptions, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    if await db.sync_options.find_one({"syncOptionsId": sync_option.syncOptionsId}):
        raise HTTPException(status_code=400, detail="SyncOption already exists")
    sync_option_dict = sync_option.dict()
    await db.sync_options.insert_one(sync_option_dict)
    return sync_option_dict


@router.get("/options/{sync_options_id}", response_model=SyncOptions)
async def read_sync_options(sync_options_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    sync_option = await db.sync_options.find_one({"syncOptionsId": sync_options_id})
    if sync_option is None:
        raise HTTPException(status_code=404, detail="SyncOption not found")
    return sync_option


# Get Sync Options by Config ID
@router.get("/options/config/{config_id}", response_model=SyncOptions)
async def read_sync_options_by_config_id(config_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    SyncOptions.update_forward_refs()
    sync_option = await db.sync_options.find_one({"configId": config_id})
    print(sync_option)
    if sync_option is None:
        raise HTTPException(status_code=404, detail="SyncOption not found")
    return sync_option


@router.put("/options/{sync_options_id}", response_model=SyncOptions)
async def update_sync_options(sync_options_id: str, sync_option: SyncOptions,
                              db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_sync_option = await db.sync_options.find_one({"syncOptionsId": sync_options_id})
    if existing_sync_option is None:
        raise HTTPException(status_code=404, detail="SyncOption not found")

    sync_option_dict = sync_option.dict()
    await db.sync_options.replace_one({"syncOptionsId": sync_options_id}, sync_option_dict)
    return sync_option_dict


@router.delete("/options/{sync_options_id}", response_model=SyncOptions)
async def delete_sync_options(sync_options_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_sync_option = await db.sync_options.find_one({"syncOptionsId": sync_options_id})
    if existing_sync_option is None:
        raise HTTPException(status_code=404, detail="SyncOption not found")
    await db.sync_options.delete_one({"syncOptionsId": sync_options_id})
    return existing_sync_option
