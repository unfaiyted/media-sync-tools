from typing import List

from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from src.create import ListBuilder
from src.models import Library, LibraryClient
from src.config import ConfigManager

router = APIRouter()
config = ConfigManager.get_manager()

# CRUD operations for Library
@router.post("/", response_model=Library)
async def create_library(library: Library, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    if await db.libraries.find_one({"libraryId": library.libraryId}):
        raise HTTPException(status_code=400, detail="Library already exists")
    library_dict = library.dict()
    await db.libraries.insert_one(library_dict)
    return library_dict

# Get all libraries
# Assuming the Library model is imported from somewhere
# from .models import Library

@router.get("/all", response_model=List[Library])
async def read_all_libraries(db: AsyncIOMotorDatabase = Depends(config.get_db)):
    libraries = [library_doc async for library_doc in db.libraries.find({})]

    if not libraries:
        return []

    return libraries


@router.get("/{library_id}", response_model=Library)
async def read_library(library_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    library_item = await db.libraries.find_one({"libraryId": library_id})
    if library_item is None:
        raise HTTPException(status_code=404, detail="Library not found")
    return library_item

@router.put("/{library_id}", response_model=Library)
async def update_library(library_id: str, library: Library, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_library = await db.libraries.find_one({"libraryId": library_id})
    if existing_library is None:
        raise HTTPException(status_code=404, detail="Library not found")

    library_dict = library.dict()
    await db.libraries.replace_one({"libraryId": library_id}, library_dict)
    return library_dict

@router.delete("/{library_id}", response_model=Library)
async def delete_library(library_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_library = await db.libraries.find_one({"libraryId": library_id})
    if existing_library is None:
        raise HTTPException(status_code=404, detail="Library not found")
    await db.libraries.delete_one({"libraryId": library_id})
    return existing_library
@router.post("/client/", response_model=LibraryClient)
async def create_library_client(library_client: LibraryClient, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    if await db.library_clients.find_one({"libraryClientId": library_client.libraryClientId}):
        raise HTTPException(status_code=400, detail="Library Client already exists")
    library_client_dict = library_client.dict()
    result = await db.library_clients.insert_one(library_client_dict)
    return library_client_dict

# Get all library Clients by LibraryId
@router.get("/clients/{library_id}", response_model=list[LibraryClient])
async def read_all_library_clients(library_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    library_clients = []
    async for library_client_doc in db.library_clients.find({"libraryId": library_id}):
        # Create a LibraryClient instance from the retrieved document
        library_clients.append(library_client_doc)
    if library_clients is None:
        raise HTTPException(status_code=404, detail="Library Client not found")
    return library_clients

@router.get("/client/{library_client_id}", response_model=LibraryClient)
async def read_library_client(library_client_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    library_client = await db.library_clients.find_one({"libraryClientId": library_client_id})
    if library_client is None:
        raise HTTPException(status_code=404, detail="Library Client not found")
    return library_client

@router.put("/client/{library_client_id}", response_model=LibraryClient)
async def update_library_client(library_client_id: str, library_client: LibraryClient, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_library_client = await db.library_clients.find_one({"libraryClientId": library_client_id})
    if existing_library_client is None:
        raise HTTPException(status_code=404, detail="Library Client not found")

    library_client_dict = library_client.dict()
    await db.library_clients.replace_one({"libraryClientId": library_client_id}, library_client_dict)
    return library_client_dict

@router.delete("/client/{library_client_id}", response_model=LibraryClient)
async def delete_library_client(library_client_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_library_client = await db.library_clients.find_one({"libraryClientId": library_client_id})
    if existing_library_client is None:
        raise HTTPException(status_code=404, detail="Library Client not found")
    await db.library_clients.delete_one({"libraryClientId": library_client_id})
    return existing_library_client


# update library clients media list records
@router.get("/trigger/update/{library_client_id}/", response_model=LibraryClient)
async def trigger_update_library_client(library_client_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_library_client = await db.library_clients.find_one({"libraryClientId": library_client_id})
    if existing_library_client is None:
        raise HTTPException(status_code=404, detail="Library Client not found")

    # get library client
    library_client = LibraryClient(**existing_library_client)
    client = db.clients.find_one({"clientId": library_client.clientId})
    # find out what type of client this is
    print('client', client)

    details = {
            'name': library_client.libraryName,
            'description': f'{client.label} - {library_client.libraryName}',
            'provider': client.name,
            'filters': [{
                'type': 'library',
                'value': library_client.libraryName
            }],
            'include': ['Movies'],
            'options': {
                'add_prev_watched': False,
                'add_missing_to_library': False,
                'limit': 1000,
                'sort': 'rank',
                'poster': {
                    'enabled': True,
                }
            }
        }

    list_builder = ListBuilder(config, list=details)
    list_builder.build()

    return library_client



