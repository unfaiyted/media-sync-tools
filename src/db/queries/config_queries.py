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


async def get_full_config_client(db: AsyncIOMotorDatabase, config_client_id: str) -> ConfigClient | None:
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
        },
        {
            "$unwind": "$client"
        },
        {
            "$lookup": {
                "from": "config_client_field_values",
                "localField": "configClientId",
                "foreignField": "configClientId",
                "as": "clientFieldValues"
            }
        },
        # {
        #     "$unwind": "$clientFieldValues"
        # }
    ]

    configs = await db.config_clients.aggregate(pipeline).to_list(length=1)

    # Since we used to_list, the result is a list. Return the first (and only) element.
    config = ConfigClient.parse_obj(configs[0])

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
                "from": "clients",
                "localField": "clientId",
                "foreignField": "clientId",
                "as": "client"
            }
        },
        {
            "$unwind": "$client"
        }
    ]

    print(pipeline)
    raw_configs = await db.config_clients.aggregate(pipeline).to_list(length=1)  # Adjust length as necessary
    print(raw_configs)
    # Convert the raw dictionary data into Pydantic Library models
    configs = [ConfigClient.parse_obj(config) for config in raw_configs]

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


async def get_full_config_clients_by_config_id(db: AsyncIOMotorDatabase, config_id: str) -> list[ConfigClient] | None:
    """
    Retreive all config clients for a given config ID.
    :param db:
    :param config_id:
    :return:
    """

    # Use aggregation to combine the libraries with their clients
    pipeline = [
        {
            "$match": {"configId": config_id}
        },
        {
            "$lookup": {
                "from": "clients",
                "localField": "clientId",
                "foreignField": "clientId",
                "as": "client"
            }
        },
        {
            "$unwind": "$client"
        },
        {
            "$lookup": {
                "from": "config_client_field_values",
                "localField": "configClientId",
                "foreignField": "configClientId",
                "as": "clientFieldValues"
            }
        },
        # {
        #     "$unwind": "$clientFieldValues"
        # }
    ]

    print(pipeline)
    raw_configs = await db.config_clients.aggregate(pipeline).to_list(length=1000)# Adjust length as necessary
    print(list(raw_configs))
    # Convert the raw dictionary data into Pydantic Library models
    configs = [ConfigClient.parse_obj(config) for config in raw_configs]

    return configs or None


async def find_lists_containing_item(db: AsyncIOMotorDatabase, media_item_id: str):

    pipeline = [
        {
            "$match": {"mediaItemId": media_item_id}
        },
        {
            "$lookup": {
                "from": "media_items",  # Adjust if your collection name is different
                "localField": "mediaItemId",
                "foreignField": "mediaItemId",
                "as": "mediaItemDetails"
            }
        },
        {
            "$unwind": "$mediaItemDetails"  # Deconstructs mediaItemDetails to output one document for each item
        },
        {
            "$project": {
                "listName": "$name",
                "itemName": "$mediaItemDetails.title",
                "itemYear": "$mediaItemDetails.year"
            }
        }
    ]

    cursor = db.media_list_items.aggregate(pipeline)  # Adjust if your collection name is different
    return await cursor.to_list(None)

# Sample usage
# result = await find_lists_containing_item("some_media_item_id")
# print(result)

async def find_lists_containing_items(db: AsyncIOMotorDatabase, media_item_ids: List[str]):

    pipeline = [
        {
            "$match": {"mediaItemId": {"$in": media_item_ids}}
        },
        {
            "$lookup": {
                "from": "media_items",
                "localField": "mediaItemId",
                "foreignField": "mediaItemId",
                "as": "mediaItemDetails"
            }
        },
        {
            "$lookup": {
                "from": "media_lists",
                "localField": "mediaListId",
                "foreignField": "mediaListId",
                "as": "mediaListDetails"
            }
        },
        {
            "$unwind": "$mediaItemDetails"
        },
        {
            "$unwind": "$mediaListDetails"
        },
        {
            "$group": {
                "_id": "$mediaItemId",
                "lists": {
                    "$push": {
                        "listId": "$mediaListDetails.mediaListId",
                        "name": "$mediaListDetails.name",
                        "poster": "$mediaListDetails.poster"
                    }
                },
                "itemDetails": {"$first": "$mediaItemDetails"}
            }
        },
        {
            "$project": {
                "mediaItemId": "$_id",
                "title": "$itemDetails.title",
                "year": "$itemDetails.year",
                "containingLists": "$lists"
            }
        }
    ]

    cursor = db.media_list_items.aggregate(pipeline)
    return await cursor.to_list(None)

# # Sample usage
# media_item_ids = ["item_id_1", "item_id_2"]
# result = await find_lists_containing_items(media_item_ids)
# print(result)
