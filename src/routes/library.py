import uuid
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from src.models import MediaList, MediaListType, EmbyFilters
from src.create import ListBuilder
from src.models import Library, LibraryGroup
from src.config import ConfigManager

router = APIRouter()


# CRUD operations for Library
@router.post("/", response_model=Library)
async def create_library(library: Library):
    db = (await ConfigManager.get_manager()).get_db()
    if await db.libraries.find_one({"libraryId": library.libraryId}):
        raise HTTPException(status_code=400, detail="Library already exists")
    library_dict = library.dict()
    await db.libraries.insert_one(library_dict)
    return library_dict


# Get all libraries
# Assuming the Library model is imported from somewhere
# from .models import Library

@router.get("/all", response_model=List[Library])
async def read_all_libraries():
    db = (await ConfigManager.get_manager()).get_db()
    libraries = [library_doc async for library_doc in db.libraries.find({})]

    return [] if not libraries else libraries


@router.get("/{library_id}", response_model=Library)
async def read_library(library_id: str):
    db = (await ConfigManager.get_manager()).get_db()
    library_item = await db.libraries.find_one({"libraryId": library_id})
    if library_item is None:
        raise HTTPException(status_code=404, detail="Library not found")
    return library_item


@router.put("/{library_id}", response_model=Library)
async def update_library(library_id: str, library: Library):
    db = (await ConfigManager.get_manager()).get_db()
    existing_library = await db.libraries.find_one({"libraryId": library_id})
    if existing_library is None:
        raise HTTPException(status_code=404, detail="Library not found")

    library_dict = library.dict()
    await db.libraries.replace_one({"libraryId": library_id}, library_dict)
    return library_dict


@router.delete("/{library_id}", response_model=Library)
async def delete_library(library_id: str):
    db = (await ConfigManager.get_manager()).get_db()
    existing_library = await db.libraries.find_one({"libraryId": library_id})
    if existing_library is None:
        raise HTTPException(status_code=404, detail="Library not found")
    await db.libraries.delete_one({"libraryId": library_id})
    return existing_library


# update library media list records
@router.get("/trigger/update/{library_id}/", response_model=Library)
async def trigger_update_library_client(library_id: str):
    config = await ConfigManager.get_manager()
    db = config.get_db()
    log = config.get_logger(__name__)

    existing_library = await db.library_clients.find_one({"libraryId": library_id})
    if existing_library is None:
        log.error(f"Library not found.", library_id=library_id)
        raise HTTPException(status_code=404, detail="Library Client not found")

    # get library client
    library = Library(**existing_library)
    client = db.clients.find_one({"clientId": library.clientId})
    # find out what type of client this is
    print('client', client)

    # details = {
    #         'name': library.name,
    #         'description': f'{client.label} - {library.name}',
    #         'provider': client.name,
    #         'filters': [{
    #             'type': 'library',
    #             'value': library.name
    #         }],
    #         'include': ['Movies'],
    #         'options': {
    #             'add_prev_watched': False,
    #             'add_missing_to_library': False,
    #             'limit': 1000,
    #             'sort': 'rank',
    #             'poster': {
    #                 'enabled': True,
    #             }
    #         }
    #     }

    filters = EmbyFilters(
        clientId=client.clientId,
        library=library.name,
    )

    media_list = MediaList(
        mediaListId=str(uuid.uuid4()),
        name=library.name,
        type=MediaListType.COLLECTION,
        description=f'{client.label} - {library.name}',
        sortName=library.name,
        filters=filters.dict(),
        clientId='emby',
        createdAt=datetime.now(),
        creatorId=config.get_user().userId
    )

    list_builder = ListBuilder(config, media_list=media_list)
    await list_builder.build()

    return library
