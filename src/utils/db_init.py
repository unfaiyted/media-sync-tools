import asyncio
import uuid

import motor
from pymongo import MongoClient
from typing import Optional

from src.models import ClientType, Config, FieldType, ClientField, SyncOptions, User, ConfigClientFieldsValue, \
    ConfigClient

# Provided clients and their fields
clients_data = {
    "plex": {
        "label": "Plex",
        "type": ClientType.MEDIA_SERVER,
        "fields": {
            "server_url": {"placeholderValue": "http://example.com:port", "type": FieldType.STRING},
            "access_token": {"placeholderValue": "xxxx-xxxx-xxxx", "type": FieldType.PASSWORD}
        }
    },
    "myplex": {
        "label": "MyPlex",
        "type": ClientType.MEDIA_SERVER,
        "fields": {
            "username": {"placeholderValue": "example@example.com", "type": FieldType.STRING},
            "password": {"placeholderValue": "password", "type": FieldType.PASSWORD},
            "resource": {"placeholderValue": "Server-Name", "type": FieldType.STRING}
        }
    },
    "emby": {
        "label": "Emby",
        "type": ClientType.MEDIA_SERVER,
        "fields": {
            "server_url": {"placeholderValue": "http://example.com:port", "type": FieldType.STRING},
            "api_key": {"placeholderValue": "xxxxxxxxxxxx", "type": FieldType.PASSWORD},
            "username": {"placeholderValue": "username", "type": FieldType.STRING},
            "isPrimary": {"placeholderValue": "true", "type": FieldType.BOOLEAN}
        }
    },
    "trakt": {
        "label": "Trakt",
        "type": ClientType.LIST_PROVIDER,
        "fields": {
            "client_id": {"placeholderValue": "xxxxxxxxxxxx", "type": FieldType.STRING},
            "client_secret": {"placeholderValue": "xxxxxxxxxxxx", "type": FieldType.PASSWORD},
            "username": {"placeholderValue": "username", "type": FieldType.STRING}
        }
    },
    "tmdb": {
        "label": "TMDb",
        "type": ClientType.LIST_PROVIDER,
        "fields": {
            "username": {"placeholderValue": "username", "type": FieldType.STRING},
            "password": {"placeholderValue": "password", "type": FieldType.PASSWORD},
            "bearer_token": {"placeholderValue": "eyJhxxxxxx", "type": FieldType.PASSWORD}
        }
    },
    "chat": {
        "label": "ChatGPT",
        "type": ClientType.UTILITY,
        "fields": {
            "api_key": {"placeholderValue": "sk-xxxxxxxxxxxx", "type": FieldType.PASSWORD}
        }
    },
    "mdb": {
        "label": "MDBList",
        "type": ClientType.LIST_PROVIDER,
        "fields": {
            "api_key": {"placeholderValue": "xxxxxxxxxxxx", "type": FieldType.PASSWORD}
        }
    },
    "radarr": {
        "label": "Radarr",
        "type": ClientType.UTILITY,
        "fields": {
            "server_url": {"placeholderValue": "http://example.com:port", "type": FieldType.STRING},
            "api_key": {"placeholderValue": "xxxxxxxxxxxx", "type": FieldType.PASSWORD},
            "default_media_path": {"placeholderValue": "/movies", "type": FieldType.STRING},
            "quality_profile": {"placeholderValue": "Any", "type": FieldType.STRING}
        }
    },
    "sonarr": {
        "label": "Sonarr",
        "type": ClientType.UTILITY,
        "fields": {
            "server_url": {"placeholderValue": "http://example.com:port", "type": FieldType.STRING},
            "api_key": {"placeholderValue": "xxxxxxxxxxxx", "type": FieldType.PASSWORD},
            "default_media_path": {"placeholderValue": "/tv", "type": FieldType.STRING},
            "quality_profile": {"placeholderValue": "All", "type": FieldType.STRING}
        }
    }
}

# Let's assume you've defined FieldType and ClientType elsewhere
# as well as the clients_data
import asyncio
import uuid
import yaml
from typing import Optional
from src.config import ConfigManager


# ... [keep your clients_data unchanged] ...

def read_config_yml(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


class DatabaseInitializer:
    def __init__(self, ymlFile: str, database_name: str = 'sync-tools-db'):
        config = ConfigManager.get_manager()
        self.yml_config = read_config_yml(ymlFile)
        print(self.yml_config)
        self.db = config.get_db()
        self.users = self.db["users"]
        self.configs = self.db["configs"]
        self.sync_options = self.db["sync_options"]

    async def get_user(self) -> Optional[dict]:
        return await self.users.find_one()

    async def create_indexes(self):
        # Index for users collection
        await self.users.create_index("userId", unique=True)

        # Index for configs collection
        await self.configs.create_index("configId", unique=True)

        # Index for sync_options collection
        await self.sync_options.create_index("syncOptionsId", unique=True)

        # Index for clients collection
        clients_collection = self.db["clients"]
        await clients_collection.create_index("clientId", unique=True)

        # Index for client_fields collection
        client_fields_collection = self.db["client_fields"]
        await client_fields_collection.create_index("clientFieldId", unique=True)

        # Index for config_clients collection
        config_clients_collection = self.db["config_clients"]
        await config_clients_collection.create_index("configClientId", unique=True)

        # Index for config_client_field_values collection
        config_client_field_values_collection = self.db["config_client_field_values"]
        await config_client_field_values_collection.create_index("configClientFieldValueId", unique=True)

        await self.db["media_list_items"].create_index("mediaItemId")
        await self.db["media_list_items"].create_index("mediaListId")

        # Indexes for the media_items collection
        await self.db["media_items"].create_index("mediaItemId", unique=True)

        # Indexes for the media_lists collection
        await self.db["media_lists"].create_index("mediaListId", unique=True)
        print("Indexes created successfully!")


    async def list_indexes(self):
         db = self.db
         for collection_name in await db.list_collection_names():
            print('collection_name', collection_name)
            collection = db[str(collection_name)]
            indexes = collection.list_indexes()

            print(f"Indexes for {collection_name}:")
            index_list = await indexes.to_list(length=None)  # Get all the items
            for index in index_list:
                print(f"  - {index['name']}: {index['key']}")
                print("\n")


    async def create_admin_user(self):
        admin_user = {
            "userId": 'APP-DEFAULT-USER',
            "configId": 'APP-DEFAULT-CONFIG',
            "email": "admin@media-sync.com",
            "name": "Admin",
            "password": "hashed_password",
        }
        admin = User(**admin_user)
        await self.users.insert_one(admin.dict())
        return admin_user


    async def get_config(self) -> Optional[dict]:
        return await self.configs.find_one()


    async def create_default_config(self, user):
        default_config = {
            "configId": 'APP-DEFAULT-CONFIG',
            "userId": user['userId'],
            "clients": [],
            "libraries": [],
            "sync": None
        }
        await self.configs.insert_one(default_config)
        return default_config


    async def get_sync_options(self) -> Optional[dict]:
        return await self.sync_options.find_one()


    async def create_default_sync_options(self, config):
        sync_options = {
            "syncOptionsId": str(uuid.uuid4()),
            "configId": config['configId'],
            "collections": False,
            "playlists": False,
            "lovedTracks": False,
            "topLists": False,
            "watched": False,
            "ratings": False,
            "libraries": False,
            "trakt": False,
        }

        sync = SyncOptions(**sync_options)
        await self.sync_options.insert_one(sync.dict())
        return sync_options


    async def create_config_client_field_values(self, clientId: str, client_key: str):
        client_config = self.yml_config.get('clients', {}).get(client_key, {})
        client_field_values = []

        for field_name, field_value in client_config.items():
            # We need to retrieve the `clientFieldId` corresponding to this field_name
            client_field = await self.db.client_fields.find_one({
                "clientId": clientId,
                "name": field_name
            })

            if client_field:  # If found
                field_value_entry = {
                    "configClientFieldValueId": str(uuid.uuid4()),
                    "configClientFieldId": client_field["clientFieldId"],
                    "configClientId": clientId,
                    "value": field_value,
                    "clientField": client_field
                    # If you want to keep a reference to the whole field object, but can be omitted to reduce redundancy
                }

                client_field_value = ConfigClientFieldsValue(**field_value_entry)
                client_field_values.append(client_field_value.dict())

        if client_field_values:
            await self.db.config_client_field_values.insert_many(client_field_values)


    async def create_config_client_and_fields(self, clientId: str, client_key: str, configId: str):
        client_config = self.yml_config.get('clients', {}).get(client_key, {})
        client = await self.db.clients.find_one({"clientId": clientId})

        # Create ConfigClient
        config_client_data = {
            "configClientId": str(uuid.uuid4()),
            "label": client["label"],
            "client": client,
            "clientId": clientId,
            "configId": configId
        }
        config_client = ConfigClient(**config_client_data)
        await self.db.config_clients.insert_one(config_client.dict())

        # Create ConfigClientFieldsValue for each field
        client_field_values = []
        for field_name, field_value in client_config.items():
            client_field = await self.db.client_fields.find_one({
                "clientId": clientId,
                "name": field_name
            })

            if client_field:  # If found
                field_value_entry = {
                    "configClientFieldValueId": str(uuid.uuid4()),
                    "configClientFieldId": client_field["clientFieldId"],
                    "configClientId": config_client.configClientId,
                    "value": field_value
                }

                client_field_value = ConfigClientFieldsValue(**field_value_entry)
                client_field_values.append(client_field_value.dict())

        if client_field_values:
            await self.db.config_client_field_values.insert_many(client_field_values)


    async def run(self):
        user = await self.get_user() or await self.create_admin_user()
        config = await self.get_config() or await self.create_default_config(user)
        sync_options = await self.get_sync_options() or await self.create_default_sync_options(config)

        client_collection_exists = await self.db.list_collection_names(filter={"name": "clients"})
        if not client_collection_exists or await self.db.clients.count_documents({}) == 0:
            client_entries = []
            client_field_entries = []

            for key, client_info in clients_data.items():

                clientId = str(uuid.uuid4())

                client_entry = {
                    "clientId": clientId,
                    "label": client_info['label'],
                    "type": client_info['type'],
                    "name": key.upper()
                }
                client_entries.append(client_entry)

                for field_name, field_info in client_info['fields'].items():
                    client_field_entry = {
                        "clientFieldId": str(uuid.uuid4()),
                        "clientId": clientId,
                        "name": field_name,
                        "type": field_info['type'],
                        "placeholderValue": field_info['placeholderValue']
                    }
                    client = ClientField(**client_field_entry)
                    client_field_entries.append(client.dict())

            await self.db.clients.insert_many(client_entries)
            await self.db.client_fields.insert_many(client_field_entries)

            # Now, after initializing clients and client_fields
            config = await self.get_config()  # Assuming you have a config object in db
            for key in clients_data.keys():
                client_in_db = await self.db.clients.find_one({"name": key.upper()})
                if client_in_db:
                    await self.create_config_client_and_fields(client_in_db["clientId"], key, config["configId"])

            # Create indexes
        await self.create_indexes()
        # await self.list_indexes()
    # # To run
    # loop = asyncio.get_event_loop()
    # dbinit = DatabaseInitializer()
    # loop.run_until_complete(dbinit.run())
