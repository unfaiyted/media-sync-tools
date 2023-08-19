from motor.motor_asyncio import AsyncIOMotorDatabase

from src.models import SyncOptions, MediaList
from src.config import ConfigManager
from src.create.toplists import sync_top_lists
from src.sync.watchlist import sync_watchlist
from src.sync.collections import sync_collections
from src.create.lists import Lists
from src.create.trakt import sync_trakt_user_lists
from src.create.playlists import create_emby_playlist

from starlette.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException

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
        sync_top_lists(config)

        return JSONResponse(status_code=200, content={"message": "Sync watchlist started successfully."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@router.get("/collections")
async def trigger_sync_collection():
    settings = config.get_collection_settings()

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


@router.get('/trakt')
async def handle_trakt():
    try:

        sync_trakt_user_lists(config, 'faiyt')

        return JSONResponse(status_code=200, content={"message": "User lists synced from Trakt", })
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
    sync_option = await db.sync_options.find_one({"configId": config_id})
    if sync_option is None:
        raise HTTPException(status_code=404, detail="SyncOption not found")
    return sync_option

@router.put("/options/{sync_options_id}", response_model=SyncOptions)
async def update_sync_options(sync_options_id: str, sync_option: SyncOptions, db: AsyncIOMotorDatabase = Depends(config.get_db)):
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
