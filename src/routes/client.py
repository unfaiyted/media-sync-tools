from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from src.models import Client, List, ClientField
from src.config import ConfigManager
from fastapi import APIRouter, HTTPException, Depends

router = APIRouter()
config = ConfigManager.get_manager()

@router.post("/", response_model=Client)
async def create_client(client: Client, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    if await db.clients.find_one({"clientId": ObjectId(client.clientId)}):
        raise HTTPException(status_code=400, detail="Client already registered")
    client_dict = client.dict()
    await db.clients.insert_one(client_dict)
    return client_dict


@router.get("/", response_model=Client)
async def read_clients(client_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    clients = await db.clients.all()
    if clients is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return clients

@router.get("/{client_id}", response_model=Client)
async def read_client(client_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    client = await db.clients.find_one({"clientId": ObjectId(client_id)})
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.put("/{client_id}", response_model=Client)
async def update_client(client_id: str, client: Client, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_client = await db.clients.find_one({"clientId": ObjectId(client_id)})
    if existing_client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    client_dict = client.dict()
    await db.clients.replace_one({"clientId": ObjectId(client_id)}, client_dict)
    return client_dict


@router.delete("/{client_id}", response_model=Client)
async def delete_client(client_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_client = await db.clients.find_one({"clientId": ObjectId(client_id)})
    if existing_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    await db.clients.delete_one({"clientId": ObjectId(client_id)})
    return existing_client

@router.post("/field/", response_model=ClientField)
async def create_client_field(client_field: ClientField, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    if await db.client_fields.find_one({"clientFieldId": ObjectId(client_field.clientFieldId)}):
        raise HTTPException(status_code=400, detail="Client Field already exists")
    client_field_dict = client_field.dict()
    result = await db.client_fields.insert_one(client_field_dict)
    return client_field_dict

@router.get("/field/{client_field_id}", response_model=ClientField)
async def read_client_field(client_field_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    client_field = await db.client_fields.find_one({"clientFieldId": ObjectId(client_field_id)})
    if client_field is None:
        raise HTTPException(status_code=404, detail="Client Field not found")
    return client_field

@router.put("/field/{client_field_id}", response_model=ClientField)
async def update_client_field(client_field_id: str, client_field: ClientField, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_client_field = await db.client_fields.find_one({"clientFieldId": ObjectId(client_field_id)})
    if existing_client_field is None:
        raise HTTPException(status_code=404, detail="Client Field not found")

    client_field_dict = client_field.dict()
    await db.client_fields.replace_one({"clientFieldId": ObjectId(client_field_id)}, client_field_dict)
    return client_field_dict

@router.delete("/field/{client_field_id}", response_model=ClientField)
async def delete_client_field(client_field_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_client_field = await db.client_fields.find_one({"clientFieldId": ObjectId(client_field_id)})
    if existing_client_field is None:
        raise HTTPException(status_code=404, detail="Client Field not found")
    await db.client_fields.delete_one({"clientFieldId": ObjectId(client_field_id)})
    return existing_client_field
