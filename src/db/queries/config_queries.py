from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.models import Library, LibraryType, ConfigClient, Config


async def get_config_client_with_client(db: AsyncIOMotorDatabase, config_client_id: str) -> Config | None:
    """
    Retrieve a library and its associated clients.
    :param db:
    :param config_client_id:
    :return:
    """
    pipeline = [
        {
            "$match": {"configClientId": config_client_id}
        },
        {
            "$lookup": {
                "from": "clients",
                "localField": "clientId",
                "foreignField": "clientId",
                "as": "client"
            }
        }
    ]

    configs = await db.config_clients.aggregate(pipeline).to_list(length=1)

    # Since we used to_list, the result is a list. Return the first (and only) element.
    config = Config.parse_obj(configs[0])

    return config or None


async def get_config_clients_with_client_by_config_id(db: AsyncIOMotorDatabase, config_id: str) -> list[Config] | None:
    """
    Retrieve all libraries and their associated clients by a configuration ID.
    """

    # Use aggregation to combine the libraries with their clients
    pipeline = [
        {
            "$match": {"configId": config_id}
        },
        {
            "$lookup": {
                "from": "config",
                "localField": "clientId",
                "foreignField": "clientId",
                "as": "client"
            }
        }
    ]

    raw_configs = await db.config_clients.aggregate(pipeline).to_list(length=100)  # Adjust length as necessary

    # Convert the raw dictionary data into Pydantic Library models
    configs = [Config.parse_obj(config) for config in raw_configs]

    return configs or None


# Get Library with Library Clients
async def get_library_with_clients(db: AsyncIOMotorDatabase, library_id: str) -> Library:
    """
    Retrieve a library and its associated clients.
    """
    pipeline = [
        {
            "$match": {"libraryId": library_id}
        },
        {
            "$lookup": {
                "from": "library_clients",
                "localField": "libraryId",
                "foreignField": "libraryId",
                "as": "clients"
            }
        }
    ]

    libraries = await db.libraries.aggregate(pipeline).to_list(length=1)

    # Since we used to_list, the result is a list. Return the first (and only) element.
    library = Library.parse_obj(libraries[0])
