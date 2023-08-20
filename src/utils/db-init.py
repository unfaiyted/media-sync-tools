import asyncio
import uuid

import motor
from pymongo import MongoClient
from typing import Optional

from src.config import ConfigManager
from src.models import ClientType, Config, FieldType, ClientField, SyncOptions, User

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

from typing import Optional
from src.config import ConfigManager

# ... [keep your clients_data unchanged] ...


class DatabaseInitializer:
    def __init__(self, config, database_name: str = 'sync-tools-db'):
        self.db = config.get_db()
        self.users = self.db["users"]
        self.configs = self.db["configs"]
        self.sync_options = self.db["sync_options"]

    async def get_user(self) -> Optional[dict]:
        return await self.users.find_one()

    async def create_admin_user(self):
        admin_user = {
            "userId": str(uuid.uuid4()),
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
            "ratings": False
        }

        sync = SyncOptions(**sync_options)
        await self.sync_options.insert_one(sync.dict())
        return sync_options

    async def run(self):
        user = await self.get_user()
        if not user:
            user = await self.create_admin_user()

        config = await self.get_config()
        if not config:
            config = await self.create_default_config(user)

        sync_options = await self.get_sync_options()
        if not sync_options:
            sync_options = await self.create_default_sync_options(config)

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


# To run
loop = asyncio.get_event_loop()
config_setup = ConfigManager.get_manager()
dbinit = DatabaseInitializer(config=config_setup)
loop.run_until_complete(dbinit.run())

