from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel

from src.config import ConfigManager

router = APIRouter()

# Connect to MongoDB
db = ConfigManager.get_manager().get_db()
config_collection = db["config"]

# Define models
class ClientConfig(BaseModel):
    server_url: str
    access_token: str
    type: str

class Config(BaseModel):
    clients: dict = {}
    libraries: dict = {}
    sync: dict = {}
    collections: dict = {}
    playlists: dict = {}

# Retrieve configuration
@router.get("/", response_model=Config)
async def read_config():
    config = config_collection.find_one()
    if config:
        return config
    else:
        raise HTTPException(status_code=404, detail="Configuration not found")

# Update configuration
# ... (other imports)

from pydantic import BaseModel

class ConfigUpdate(BaseModel):
    userId: str = '1'
    clientData: dict
# Update client configurations within the existing config object
@router.put("/", response_model=Config)
async def update_client_config(updated_config: ConfigUpdate):
    existing_config = config_collection.find_one({"userId": updated_config.userId})
    print(existing_config, updated_config)

    if existing_config is None:
        print("Creating new config")
        config_collection.insert_one({"userId": '1' ,"config": {
            "clients": {},
            "libraries": {},
            "sync": {},
            "collections": {},
            "playlists": {}
        }})
        existing_config = config_collection.find_one({"userId": updated_config.userId})

    if existing_config:
        print("Updating existing config")
        existing_clients = existing_config["config"]["clients"]
        updated_clients = updated_config.clientData
        merged_clients = {**existing_clients, **updated_clients}  # Merge the dictionaries

        existing_config["config"]["clients"] = merged_clients  # Update the clients sub-object

        config_collection.update_one({"userId": updated_config.userId}, {"$set": existing_config})

        # existing_config["config"]["clients"].update(updated_config.clientData)  # Update the clients sub-object
        # existing_config["libraries"].update(updated_config.libraries)  # Update the libraries sub-object
        # existing_config["sync"].update(updated_config.sync)  # Update the sync sub-object
        # existing_config["collections"].update(updated_config.collections)  # Update the collections sub-object
        # existing_config["playlists"].update(updated_config.playlists)  # Update the playlists sub-object

        # config_collection.update_one({"user_id": updated_config.userId}, {"$set": existing_config})

        return existing_config
    else:
        raise HTTPException(status_code=404, detail="Config not found")


# Delete configuration
@router.delete("/", response_model=dict)
async def delete_config():
    result = config_collection.delete_one({})
    if result.deleted_count > 0:
        return {"message": "Configuration deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Configuration not found")

# Create configuration
@router.post("/", response_model=dict)
async def create_config():
    config = config_collection.find_one()
    if config:
        raise HTTPException(status_code=400, detail="Configuration already exists")
    else:
        config_collection.insert_one({"userId": '1' ,"config": {
            "clients": {},
            "libraries": {},
            "sync": {},
            "collections": {},
            "playlists": {}
        }})
        return {"message": "Configuration created successfully"}
