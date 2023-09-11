from typing import List

from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from src.models import Client, ClientField,  FilterType
from src.config import ConfigManager
from fastapi import APIRouter, HTTPException, Depends

router = APIRouter()


@router.post("/", response_model=Client)
async def create_client(client: Client, ):
    db = (await ConfigManager.get_manager()).get_db()
    # print('client', client)

    try:
        client_dict = client.dict()
        await db.clients.insert_one(client_dict)
        return client_dict
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Client insert issue.")


@router.get("/", response_model=List[Client])
async def read_all_clients():
    db = (await ConfigManager.get_manager()).get_db()
    clients = []
    async for client_doc in db.clients.find({}):
        # Create a Client instance from the retrieved document
        clients.append(client_doc)
    if clients is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return clients


@router.get("/{client_id}", response_model=Client)
async def read_client(client_id: str, ):
    db = (await ConfigManager.get_manager()).get_db()
    client = await db.clients.find_one({"clientId": client_id})
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


# Get all clients by type
@router.get("/type/{client_type}", response_model=List[Client])
async def read_all_clients_by_type(client_type: str, ):
    db = (await ConfigManager.get_manager()).get_db()
    clients = []
    async for client_doc in db.clients.find({"type": client_type}):
        # Create a Client instance from the retrieved document
        clients.append(client_doc)
    if clients is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return clients


@router.put("/{client_id}", response_model=Client)
async def update_client(client_id: str, client: Client, ):
    db = (await ConfigManager.get_manager()).get_db()
    existing_client = await db.clients.find_one({"clientId": client_id})
    if existing_client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    client_dict = client.dict()
    await db.clients.replace_one({"clientId": client_id}, client_dict)
    return client_dict


@router.delete("/{client_id}", response_model=Client)
async def delete_client(client_id: str, ):
    db = (await ConfigManager.get_manager()).get_db()
    existing_client = await db.clients.find_one({"clientId": client_id})
    if existing_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    await db.clients.delete_one({"clientId": client_id})
    return existing_client


# Get all fields for a given clientId
@router.get("/field/", response_model=List[ClientField])
async def read_all_client_fields_by_client_id(clientId: str, ):
    db = (await ConfigManager.get_manager()).get_db()
    client_fields = []
    async for client_field_doc in db.client_fields.find({"clientId": clientId}):
        # Create a Client instance from the retrieved document
        client_fields.append(client_field_doc)
    if client_fields is None:
        raise HTTPException(status_code=404, detail="Client Field not found")
    return client_fields


@router.post("/field/", response_model=ClientField)
async def create_client_field(client_field: ClientField, ):
    db = (await ConfigManager.get_manager()).get_db()
    print('client_field', client_field)
    if await db.client_fields.find_one({"clientFieldId": client_field.clientFieldId}):
        raise HTTPException(status_code=400, detail="Client Field already exists")
    client_field_dict = client_field.dict()
    result = await db.client_fields.insert_one(client_field_dict)
    return client_field_dict


@router.get("/field/{client_field_id}", response_model=ClientField)
async def read_client_field(client_field_id: str, ):
    db = (await ConfigManager.get_manager()).get_db()
    client_field = await db.client_fields.find_one({"clientFieldId": client_field_id})
    if client_field is None:
        raise HTTPException(status_code=404, detail="Client Field not found")
    return client_field


# Client Field by ClientId
@router.get("/field/client/{client_id}", response_model=List[ClientField])
async def read_by_client_id(client_id: str, ):
    db = (await ConfigManager.get_manager()).get_db()
    client_fields = []
    async for client_field_doc in db.client_fields.find({"clientId": client_id}):
        # Create a Client instance from the retrieved document
        client_fields.append(client_field_doc)
    if client_fields is None:
        raise HTTPException(status_code=404, detail="Client Field not found")
    return client_fields


@router.put("/field/{client_field_id}", response_model=ClientField)
async def update_client_field(client_field_id: str, client_field: ClientField,
                              ):
    db = (await ConfigManager.get_manager()).get_db()
    existing_client_field = await db.client_fields.find_one({"clientFieldId": client_field_id})
    if existing_client_field is None:
        raise HTTPException(status_code=404, detail="Client Field not found")

    client_field_dict = client_field.dict()
    await db.client_fields.replace_one({"clientFieldId": client_field_id}, client_field_dict)
    return client_field_dict


@router.delete("/field/{client_field_id}", response_model=ClientField)
async def delete_client_field(client_field_id: str, ):
    db = (await ConfigManager.get_manager()).get_db()
    existing_client_field = await db.client_fields.find_one({"clientFieldId": client_field_id})
    if existing_client_field is None:
        raise HTTPException(status_code=404, detail="Client Field not found")
    await db.client_fields.delete_one({"clientFieldId": client_field_id})
    return existing_client_field


# Filter Types Admin
@router.post("/filter/", response_model=FilterType)
async def create_filter(filter_item: FilterType, ):
    db = (await ConfigManager.get_manager()).get_db()
    if await db.filters.find_one({"filterId": filter_item.filterId}):
        raise HTTPException(status_code=400, detail="FilterType already exists")
    filter_dict = filter_item.dict()
    await db.filters.insert_one(filter_dict)
    return filter_dict


@router.get("/filter/{filter_id}", response_model=FilterType)
async def read_filter(filter_id: str, ):
    db = (await ConfigManager.get_manager()).get_db()
    filter_item = await db.filters.find_one({"filterId": filter_id})
    if filter_item is None:
        raise HTTPException(status_code=404, detail="FilterType not found")
    return filter_item


@router.put("/filter/{filter_id}", response_model=FilterType)
async def update_filter(filter_id: str, filter_item: FilterType, ):
    db = (await ConfigManager.get_manager()).get_db()
    existing_filter = await db.filters.find_one({"filterId": filter_id})
    if existing_filter is None:
        raise HTTPException(status_code=404, detail="FilterType not found")

    filter_dict = filter_item.dict()
    await db.filters.replace_one({"filterId": filter_id}, filter_dict)
    return filter_dict


@router.delete("/filter/{filter_id}", response_model=FilterType)
async def delete_filter(filter_id: str, ):
    db = (await ConfigManager.get_manager()).get_db()
    existing_filter = await db.filters.find_one({"filterId": filter_id})
    if existing_filter is None:
        raise HTTPException(status_code=404, detail="FilterType not found")
    await db.filters.delete_one({"filterId": filter_id})
    return existing_filter


# Get all filters by clientId
@router.get("/filter/client/{clientId}", response_model=List[FilterType])
async def read_all_filters_by_client_id(clientId: str, ):
    db = (await ConfigManager.get_manager()).get_db()
    filters = []
    async for filter_doc in db.filters.find({"clientId": clientId}):
        # Create a Client instance from the retrieved document
        filters.append(filter_doc)
    if filters is None:
        raise HTTPException(status_code=404, detail="FilterType not found")
    return filters
