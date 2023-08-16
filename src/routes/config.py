from typing import List

from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient
from bson import ObjectId
from src.models import Config, ConfigClient, ClientField, ConfigClientFieldsValue
from src.config import ConfigManager

router = APIRouter()

# Connect to MongoDB
db = ConfigManager.get_manager().get_db()
config_collection = db["config"]

# # Define models
# class ClientConfig(BaseModel):
#     server_url: str
#     access_token: str
#     type: str
#
# class Config(BaseModel):
#     clients.ts: dict = {}
#     libraries: dict = {}
#     sync: dict = {}
#     collections: dict = {}
#     playlists: dict = {}
#
# # Retrieve configuration
# @router.get("/", response_model=Config)
# async def read_config():
#     clients.ts = config_collection.find_one({"userId": "1"})
#     print('clients.ts',clients.ts)
#     if clients.ts:
#         return clients.ts['config']
#     else:
#         raise HTTPException(status_code=404, detail="Configuration not found")
#
# # Update configuration
# # ... (other imports)
#
# from pydantic import BaseModel
#
# class ConfigUpdate(BaseModel):
#     userId: str = '1'
#     clientData: dict
# # Update client configurations within the existing config object
# @router.put("/", response_model=Config)
# async def update_client_config(updated_config: ConfigUpdate):
#     existing_config = config_collection.find_one({"userId": updated_config.userId})
#     print(existing_config, updated_config)
#
#     if existing_config is None:
#         print("Creating new config")
#         config_collection.insert_one({"userId": '1' ,"config": {
#             "clients.ts": {},
#             "libraries": {},
#             "sync": {},
#             "collections": {},
#             "playlists": {}
#         }})
#         existing_config = config_collection.find_one({"userId": updated_config.userId})
#
#     if existing_config:
#         print("Updating existing config")
#         existing_clients = existing_config["config"]["clients.ts"]
#         updated_clients = updated_config.clientData
#         merged_clients = {**existing_clients, **updated_clients}  # Merge the dictionaries
#
#         existing_config["config"]["clients.ts"] = merged_clients  # Update the clients.ts sub-object
#
#         config_collection.update_one({"userId": updated_config.userId}, {"$set": existing_config})
#
#         return existing_config
#     else:
#         raise HTTPException(status_code=404, detail="Config not found")
#
#
# # Delete configuration
# @router.delete("/", response_model=dict)
# async def delete_config():
#     result = config_collection.delete_one({})
#     if result.deleted_count > 0:
#         return {"message": "Configuration deleted successfully"}
#     else:
#         raise HTTPException(status_code=404, detail="Configuration not found")
#
# # Create configuration
# @router.post("/", response_model=dict)
# async def create_config():
#     config = config_collection.find_one()
#     if config:
#         raise HTTPException(status_code=400, detail="Configuration already exists")
#     else:
#         config_collection.insert_one({"userId": '1' ,"config": {
#             "clients.ts": {},
#             "libraries": {},
#             "sync": {},
#             "collections": {},
#             "playlists": {}
#         }})
#         return {"message": "Configuration created successfully"}
#
# @router.delete("/client/{client_id}", response_model=dict)
# async def delete_client(client_id: str):
#     config = config_collection.find_one({"userId": "1"})  # Assuming you have only one document for the user
#
#     if "clients.ts" in config["config"]:
#         clients.ts = config["config"]["clients.ts"]
#         if client_id in clients.ts:
#             del clients.ts[client_id]
#             config_collection.update_one({"userId": "1"}, {"$set": {"config.clients.ts": clients.ts}})
#
#             return {"message": "Client deleted successfully"}
#
#
#     raise HTTPException(status_code=404, detail="Client not found")
#
#
# # Update libraries configuration within the existing config object using object merge
# @router.put("/libraries", response_model=Config)
# async def update_libraries_config(updated_libraries: dict):
#     existing_config = config_collection.find_one({"userId": "1"})
#
#     if existing_config:
#         existing_libraries = existing_config["config"]["libraries"]
#         existing_libraries.update(updated_libraries)
#
#         existing_config["config"]["libraries"] = existing_libraries
#         config_collection.update_one({"userId": "1"}, {"$set": existing_config})
#
#         return existing_config["config"]
#     else:
#         raise HTTPException(status_code=404, detail="Config not found")
#
# # Update sync configuration within the existing config object using object merge
# @router.put("/sync", response_model=Config)
# async def update_sync_config(updated_sync: dict):
#     existing_config = config_collection.find_one({"userId": "1"})
#
#     if existing_config:
#         existing_sync = existing_config["config"]["sync"]
#         existing_sync.update(updated_sync)
#
#         existing_config["config"]["sync"] = existing_sync
#         config_collection.update_one({"userId": "1"}, {"$set": existing_config})
#
#         return existing_config["config"]
#     else:
#         raise HTTPException(status_code=404, detail="Config not found")
#
#
#
# # Get libraries
# @router.get("/libraries", response_model=dict)
# async def get_libraries():
#     config = config_collection.find_one({"userId": "1"})
#     if config:
#         return config["config"]["libraries"]
#     else:
#         raise HTTPException(status_code=404, detail="Config not found")


router = APIRouter()
config = ConfigManager.get_manager()

# CRUD operations for Config
@router.post("/", response_model=Config)
async def create_config(config_item: Config, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    if await db.configs.find_one({"configId": config_item.configId}):
        raise HTTPException(status_code=400, detail="Config already exists")
    config_dict = config_item.dict()
    await db.configs.insert_one(config_dict)
    return config_dict

#get all configs
@router.get("/", response_model=List[Config])
async def read_all_configs(db: AsyncIOMotorDatabase = Depends(config.get_db)):
    configs = []
    async for config_doc in db.configs.find({}):
        # Create a Config instance from the retrieved document
        configs.append(config_doc)
    if configs is None:
        raise HTTPException(status_code=404, detail="Config not found")
    return configs

@router.get("/{config_id}", response_model=Config)
async def read_config(config_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    config_item = await db.configs.find_one({"configId": config_id})
    if config_item is None:
        raise HTTPException(status_code=404, detail="Config not found")
    return config_item

@router.put("/{config_id}", response_model=Config)
async def update_config(config_id: str, config_item: Config, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_config = await db.configs.find_one({"configId": config_id})
    if existing_config is None:
        raise HTTPException(status_code=404, detail="Config not found")

    config_dict = config_item.dict()
    await db.configs.replace_one({"configId": config_id}, config_dict)
    return config_dict

@router.delete("/{config_id}", response_model=Config)
async def delete_config(config_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_config = await db.configs.find_one({"configId": config_id})
    if existing_config is None:
        raise HTTPException(status_code=404, detail="Config not found")
    await db.configs.delete_one({"configId": config_id})
    return existing_config


@router.get("/client/", response_model=List[ConfigClient])
async def get_config_clients_by_config_id(configId: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    print('configId', configId)
    config_clients = await db.config_clients.find({"configId": configId}).to_list(length=1000)
    print(config_clients)
    if not config_clients:
        raise HTTPException(status_code=404, detail="Config Clients not found")
    return config_clients

@router.post("/client/", response_model=ConfigClient)
async def create_config_client(config_client: ConfigClient, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    if await db.config_clients.find_one({"configClientId": config_client.configClientId}):
        raise HTTPException(status_code=400, detail="Config Client already exists")
    config_client_dict = config_client.dict()
    result = await db.config_clients.insert_one(config_client_dict)
    return config_client_dict

@router.get("/client/{config_client_id}", response_model=ConfigClient)
async def read_config_client(config_client_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    config_client = await db.config_clients.find_one({"configClientId": config_client_id})
    if config_client is None:
        raise HTTPException(status_code=404, detail="Config Client not found")
    return config_client

@router.put("/client/{config_client_id}", response_model=ConfigClient)
async def update_config_client(config_client_id: str, config_client: ConfigClient, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_config_client = await db.config_clients.find_one({"configClientId": config_client_id})
    if existing_config_client is None:
        raise HTTPException(status_code=404, detail="Config Client not found")

    config_client_dict = config_client.dict()
    await db.config_clients.replace_one({"configClientId": config_client_id}, config_client_dict)
    return config_client_dict

@router.delete("/client/{config_client_id}", response_model=ConfigClient)
async def delete_config_client(config_client_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_config_client = await db.config_clients.find_one({"configClientId": config_client_id})
    if existing_config_client is None:
        raise HTTPException(status_code=404, detail="Config Client not found")
    await db.config_clients.delete_one({"configClientId": config_client_id})
    return existing_config_client


@router.post("/client-fields-value/", response_model=ConfigClientFieldsValue)
async def create_config_client_fields_value(value: ConfigClientFieldsValue, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    if await db.config_client_fields_values.find_one({"configClientFieldsId": value.configClientFieldsId}):
        raise HTTPException(status_code=400, detail="Config Client Fields Value already exists")
    value_dict = value.dict()
    result = await db.config_client_fields_values.insert_one(value_dict)
    return value_dict

@router.get("/client-fields-value/{value_id}", response_model=ConfigClientFieldsValue)
async def read_config_client_fields_value(value_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    value = await db.config_client_fields_values.find_one({"configClientFieldsId": value_id})
    if value is None:
        raise HTTPException(status_code=404, detail="Config Client Fields Value not found")
    return value

@router.put("/client-fields-value/{value_id}", response_model=ConfigClientFieldsValue)
async def update_config_client_fields_value(value_id: str, value: ConfigClientFieldsValue, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_value = await db.config_client_fields_values.find_one({"configClientFieldsId": value_id})
    if existing_value is None:
        raise HTTPException(status_code=404, detail="Config Client Fields Value not found")

    value_dict = value.dict()
    await db.config_client_fields_values.replace_one({"configClientFieldsId": value_id}, value_dict)
    return value_dict

@router.delete("/client-fields-value/{value_id}", response_model=ConfigClientFieldsValue)
async def delete_config_client_fields_value(value_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_value = await db.config_client_fields_values.find_one({"configClientFieldsId": value_id})
    if existing_value is None:
        raise HTTPException(status_code=404, detail="Config Client Fields Value not found")
    await db.config_client_fields_values.delete_one({"configClientFieldsId": value_id})
    return existing_value
