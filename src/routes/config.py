from typing import List

from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient
from bson import ObjectId
from src.models import Config, ConfigClient, ClientField, ConfigClientFieldsValue
from src.config import ConfigManager
from src.db.queries import config_queries
router = APIRouter()

# Connect to MongoDB

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

# CRUD operations for Config
@router.post("/", response_model=Config)
async def create_config(config_item: Config):
    db = (await ConfigManager.get_manager()).get_db()
    if await db.configs.find_one({"configId": config_item.configId}):
        raise HTTPException(status_code=400, detail="Config already exists")
    config_dict = config_item.dict()
    await db.configs.insert_one(config_dict)
    return config_dict

#get all configs
@router.get("/", response_model=List[Config])
async def read_all_config():
    db = (await ConfigManager.get_manager()).get_db()
    configs = []
    async for config_doc in db.configs.find({}):
        # Create a Config instance from the retrieved document
        configs.append(config_doc)
    if configs is None:
        raise HTTPException(status_code=404, detail="Config not found")
    return configs

@router.get("/{config_id}", response_model=Config)
async def read_config(config_id: str):
    db = (await ConfigManager.get_manager()).get_db()
    config_item = await db.configs.find_one({"configId": config_id})
    if config_item is None:
        raise HTTPException(status_code=404, detail="Config not found")
    return config_item

@router.put("/{config_id}", response_model=Config)
async def update_config(config_id: str, config_item: Config):
    db = (await ConfigManager.get_manager()).get_db()
    existing_config = await db.configs.find_one({"configId": config_id})
    if existing_config is None:
        raise HTTPException(status_code=404, detail="Config not found")

    config_dict = config_item.dict()
    await db.configs.replace_one({"configId": config_id}, config_dict)
    return config_dict

@router.delete("/{config_id}", response_model=Config)
async def delete_config(config_id: str):
    db = (await ConfigManager.get_manager()).get_db()
    existing_config = await db.configs.find_one({"configId": config_id})
    if existing_config is None:
        raise HTTPException(status_code=404, detail="Config not found")
    await db.configs.delete_one({"configId": config_id})
    return existing_config


@router.get("/client/", response_model=List[ConfigClient])
async def get_config_clients_by_config_id(configId: str):
    config = await ConfigManager.get_manager()
    db = config.get_db()
    log = config.get_logger(__name__)
    log.debug("Getting config clients by config id", configId=configId)
    config_clients = await config_queries.get_full_config_clients_by_config_id(db, config_id=configId, log=log)
    # print(config_clients)
    if not config_clients:
        raise HTTPException(status_code=404, detail="Config Clients not found")
    return config_clients

@router.post("/client/", response_model=ConfigClient)
async def create_config_client(config_client: ConfigClient):
    db = (await ConfigManager.get_manager()).get_db()
    if await db.config_clients.find_one({"configClientId": config_client.configClientId}):
        raise HTTPException(status_code=400, detail="Config Client already exists")
    config_client_dict = config_client.dict()
    result = await db.config_clients.insert_one(config_client_dict)
    return config_client_dict


# get config client by configId and type
@router.get("/client/{config_id}/{type}", response_model=List[ConfigClient])
async def read_config_client_by_config_id_and_type(config_id: str, type: str):
    db = (await ConfigManager.get_manager()).get_db()

    # 1. Find all clients of the given type.
    clients_of_type = await db.clients.find({"type": type}).to_list(length=None)

    if not clients_of_type:
        raise HTTPException(status_code=404, detail="Clients of the given type not found")

    # 2. Extract their IDs.
    client_ids = [client['_id'] for client in clients_of_type]

    # 3. Find config_clients matching those IDs and the given config_id.
    matching_config_clients = await db.config_clients.find({
        "configId": config_id,
        "clientId": {"$in": client_ids}
    }).to_list(length=None)

    if not matching_config_clients:
        raise HTTPException(status_code=404, detail="Matching Config Clients not found")

    return matching_config_clients

@router.get("/client/{config_client_id}", response_model=ConfigClient)
async def read_config_client(config_client_id: str):
    db = (await ConfigManager.get_manager()).get_db()
    config_client = await db.config_clients.find_one({"configClientId": config_client_id})
    if config_client is None:
        raise HTTPException(status_code=404, detail="Config Client not found")
    return config_client

@router.put("/client/{config_client_id}", response_model=ConfigClient)
async def update_config_client(config_client_id: str, config_client: ConfigClient):
    db = (await ConfigManager.get_manager()).get_db()
    existing_config_client = await db.config_clients.find_one({"configClientId": config_client_id})
    if existing_config_client is None:
        raise HTTPException(status_code=404, detail="Config Client not found")

    config_client_dict = config_client.dict()
    await db.config_clients.replace_one({"configClientId": config_client_id}, config_client_dict)
    return config_client_dict

@router.delete("/client/{config_client_id}", response_model=ConfigClient)
async def delete_config_client(config_client_id: str):
    db = (await ConfigManager.get_manager()).get_db()
    existing_config_client = await db.config_clients.find_one({"configClientId": config_client_id})
    if existing_config_client is None:
        raise HTTPException(status_code=404, detail="Config Client not found")
    await db.config_clients.delete_one({"configClientId": config_client_id})
    return existing_config_client


@router.post("/client-fields-value/", response_model=ConfigClientFieldsValue)
async def create_config_client_fields_value(fieldValue: ConfigClientFieldsValue):
    db = (await ConfigManager.get_manager()).get_db()

    # if await db.config_client_fields_values.find_one({"configClientFieldValueId": fieldValue.configClientFieldValueId}):
    #     raise HTTPException(status_code=400, detail="Config Client Fields Value already exists")

    result = await db.config_client_fields_values.find_one({"configClientId": fieldValue.configClientId,
                                                            "configClientFieldId": fieldValue.configClientFieldId})
    if(result is not None):
        fieldValue.configClientFieldValueId = fieldValue.configClientId
        value_dict = fieldValue.dict()

        await db.config_client_fields_values.replace_one({"configClientId": fieldValue.configClientId,
                                                          "configClientFieldId": fieldValue.configClientFieldId}, value_dict)

        return value_dict

    value_dict = fieldValue.dict()
    await db.config_client_fields_values.insert_one(value_dict)
    return value_dict


# Get all field values for a given configClientId
@router.get("/client-fields-value/", response_model=List[ConfigClientFieldsValue])
async def read_all_config_client_fields_values_by_config_client_id(configClientId: str):
    db = (await ConfigManager.get_manager()).get_db()
    values = []
    async for value_doc in db.config_client_fields_values.find({"configClientId": configClientId}):
        # Create a ConfigClientFieldsValue instance from the retrieved document
        values.append(value_doc)
    if values is None:
        raise HTTPException(status_code=404, detail="Config Client Fields Value not found")
    return values


@router.get("/client-fields-value/{value_id}", response_model=ConfigClientFieldsValue)
async def read_config_client_fields_value(value_id: str):
    db = (await ConfigManager.get_manager()).get_db()
    value = await db.config_client_fields_values.find_one({"configClientFieldsId": value_id})
    if value is None:
        raise HTTPException(status_code=404, detail="Config Client Fields Value not found")
    return value

@router.put("/client-fields-value/{value_id}", response_model=ConfigClientFieldsValue)
async def update_config_client_fields_value(value_id: str, value: ConfigClientFieldsValue):
    db = (await ConfigManager.get_manager()).get_db()
    existing_value = await db.config_client_fields_values.find_one({"configClientFieldsId": value_id})
    if existing_value is None:
        raise HTTPException(status_code=404, detail="Config Client Fields Value not found")

    value_dict = value.dict()
    await db.config_client_fields_values.replace_one({"configClientFieldsId": value_id}, value_dict)
    return value_dict

@router.delete("/client-fields-value/{value_id}", response_model=ConfigClientFieldsValue)
async def delete_config_client_fields_value(value_id: str):
    db = (await ConfigManager.get_manager()).get_db()
    existing_value = await db.config_client_fields_values.find_one({"configClientFieldsId": value_id})
    if existing_value is None:
        raise HTTPException(status_code=404, detail="Config Client Fields Value not found")
    await db.config_client_fields_values.delete_one({"configClientFieldsId": value_id})
    return existing_value

# Fetch Field Values for a Given configId
@router.get("/client-fields-value/config/{config_id}", response_model=List[ConfigClientFieldsValue])
async def read_all_config_client_fields_values_by_config_id(config_id: str):
    db = (await ConfigManager.get_manager()).get_db()
    values = []
    async for value_doc in db.config_client_fields_values.find({"configId": config_id}):
        # Create a ConfigClientFieldsValue instance from the retrieved document
        values.append(value_doc)
    if values is None:
        raise HTTPException(status_code=404, detail="Config Client Fields Value not found")
    return values

#
# @router.post("/filter/", response_model=Filter)
# async def create_filter(filter_item: Filter):
#     db = (await ConfigManager.get_manager()).get_db()
#     if await db.filters.find_one({"filterId": filter_item.filterId}):
#         raise HTTPException(status_code=400, detail="Filter already exists")
#     filter_dict = filter_item.dict()
#     await db.filters.insert_one(filter_dict)
#     return filter_dict
#
# @router.get("/filter/{filter_id}", response_model=Filter)
# async def read_filter(filter_id: str):
#     db = (await ConfigManager.get_manager()).get_db()
#     filter_item = await db.filters.find_one({"filterId": filter_id})
#     if filter_item is None:
#         raise HTTPException(status_code=404, detail="Filter not found")
#     return filter_item
#
# @router.put("/filter/{filter_id}", response_model=Filter)
# async def update_filter(filter_id: str, filter_item: Filter):
#     db = (await ConfigManager.get_manager()).get_db()
#     existing_filter = await db.filters.find_one({"filterId": filter_id})
#     if existing_filter is None:
#         raise HTTPException(status_code=404, detail="Filter not found")
#
#     filter_dict = filter_item.dict()
#     await db.filters.replace_one({"filterId": filter_id}, filter_dict)
#     return filter_dict
#
# @router.delete("/filter/{filter_id}", response_model=Filter)
# async def delete_filter(filter_id: str):
#     db = (await ConfigManager.get_manager()).get_db()
#     existing_filter = await db.filters.find_one({"filterId": filter_id})
#     if existing_filter is None:
#         raise HTTPException(status_code=404, detail="Filter not found")
#     await db.filters.delete_one({"filterId": filter_id})
#     return existing_filter
#
#
# # Get all filters by Media ListId
# @router.get("/filter/list/", response_model=List[Filter])
# async def read_all_filters_by_list_id(mediaListId: str):
#     db = (await ConfigManager.get_manager()).get_db()
#     filters = []
#     async for filter_doc in db.filters.find({"mediaListId": mediaListId}):
#         # Create a Client instance from the retrieved document
#         filters.append(filter_doc)
#     if filters is None:
#         raise HTTPException(status_code=404, detail="Filter not found")
#     return filters
#

@router.get("/full/{config_id}", response_model=Config)
async def read_full_config(config_id: str):
    config = await ConfigManager.get_manager()
    db = config.get_db()
    log = config.get_logger(__name__)
    config_object = await config_queries.get_full_config(db, config_id=config_id, log=log)
    if config_object is None:
        raise HTTPException(status_code=404, detail="Config not found")
    return config_object

@router.get("/hydrate/{user_id}", response_model=Config)
async def hydrate_config(user_id: str):
    db = (await ConfigManager.get_manager()).get_db()

    # Fetch the user data
    user = await db.users.find_one({"userId": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch the related config data for the user
    appConfig = Config(**await db.configs.find_one({"userId": user_id}))

    # Fetch client data
    clients = await db.clients.find({}).to_list(length=None)

    # Fetch Library data based on the found clients
    libraries = await db.libraries.find({"configId": appConfig.configId}).to_list(length=None)

    # Fetch ConfigClient data based on the found clients
    config_clients = await db.config_clients.find({"configId": appConfig.configId}).to_list(length=None)

    if libraries is not None:
        print('libraries', libraries)
        library_clients = await db.library_clients.find({"libraryId": {"$in": [library['libraryId'] for library in libraries]}}).to_list(length=None)

        for library in libraries:
            library['clients'] = [library_client for library_client in library_clients if library_client['libraryId'] == library['libraryId']]

    # Fetch ClientField data based on the found clients
    client_fields = await db.client_fields.find({"clientId": {"$in": [client['clientId'] for client in config_clients]}}).to_list(length=None)

    for config_client in config_clients:
        config_client['clientFields'] = [field for field in client_fields if field['clientId'] == config_client['clientId']]
        config_client['clientFieldValues'] = list(
            await db.config_client_field_values.find(
                {"configClientId": config_client['configClientId']}
            ).to_list(length=None)
        )

        print('config_client', config_client['clientFieldValues'])

        config_client['client'] = [client for client in clients if client['clientId'] == config_client['clientId']][0]
    sync_options = await db.sync_options.find_one({"configId": appConfig.configId})


    appConfig.user = user
    appConfig.clients = config_clients
    appConfig.libraries = libraries
    appConfig.sync = sync_options





    return appConfig
