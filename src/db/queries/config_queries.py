from typing import List, Optional

import structlog.stdlib
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.models import Library, LibraryType, ConfigClient, Config


async def get_full_config(db: AsyncIOMotorDatabase, config_id: str, log: structlog.stdlib.BoundLogger) -> Config | None:
    """
    Retrieve a library and its associated clients.
    :param log: structlog logger
    :param db:
    :param config_id:
    :return:
    """
    pipeline = [
        {
            "$match": {"configId": config_id}
        },
        {
            "$lookup": {
                "from": "config_clients",
                "localField": "configId",
                "foreignField": "configId",
                "as": "clients"
            }
        },
      # {
      #       "$lookup": {
      #           "from": "config_client_field_values",
      #           "localField": "clients.configClientId",
      #           "foreignField": "configClientId",
      #           "as": "clients.clientFieldValues"
      #       }
      #   },
      #   {
      #       "$lookup": {
      #           "from": "client",
      #           "localField": "clientId",
      #           "foreignField": "clientId",
      #           "as": "clients.client"
      #       }
      #   },
        {
            "$lookup": {
                "from": "libraries",
                "localField": "configId",
                "foreignField": "configId",
                "as": "libraries"
            }
        },
        {
            "$lookup": {
                "from": "sync_options",
                "localField": "configId",
                "foreignField": "configId",
                "as": "sync"
            }
        },
        {
            "$lookup": {
                "from": "users",
                "localField": "userId",
                "foreignField": "userId",
                "as": "user"
            }
        },
        # Use $unwind if you expect one-to-one relations and want to get rid of arrays
        {
            "$unwind": "$user"
        },
        {
            "$unwind": "$sync"
        }
    ]

    # print('pipeline', pipeline)
    log.debug('Pipeline sent', pipeline=pipeline)
    configs = await db.configs.aggregate(pipeline).to_list(length=1)
    log.debug('Pipeline result', configs=configs)

    # If no configs found, return None
    if not configs:
        log.error('No configs found')
        return None

    log.debug('Configs found', configs=configs)
    config_data = configs[0]

    # If there are clients in the config data, fetch their details
    if 'clients' in config_data:
        log.debug('Clients found', clients=config_data['clients'])
        detailed_clients = []

        for client in config_data['clients']:
            log.debug('Client found', client=client)
            # Fetch additional details for the client
            client_details = await get_client_details(db, client, log)

            # Merge the basic client info with the detailed info
            merged_client = {**client, **client_details}
            detailed_clients.append(merged_client)

        # Replace the original clients list with the detailed one
        config_data['clients'] = detailed_clients

    log.debug('Config data', config_data=config_data)
    return Config.parse_obj(config_data)


async def get_client_details(db: AsyncIOMotorDatabase, client: dict, log: structlog.stdlib.BoundLogger) -> dict:
    client_details = {}

    # Fetch clientFieldValues
    field_values = await db.config_client_field_values.find({
        "configClientId": client["configClientId"]
    }).to_list(None)  # Fetches all matching documents

    # Add to details if data found
    if field_values:
        client_details['clientFieldValues'] = field_values

    # Fetch client object (assuming there's a unique identifier for it in client data)
    client_object = await db.clients.find_one({
        "clientId": client["clientId"]
    })

    client_fields = await db.client_fields.find({
        "clientId": client["clientId"]
    }).to_list(None)

    if client_fields:
        client_details['clientFields'] = client_fields

    for field in field_values:
        for client_field in client_fields:
            log.debug('Checking client field', field=field, client_field=client_field)
            if field['configClientFieldId'] == client_field['clientFieldId']:
                log.info('Found matching client field', field=field, client_field=client_field)
                field['clientField'] = client_field

    # Add to details if data found
    if client_object:
        log.debug('Client object found', client_object=client_object)
        client_details['client'] = client_object

    log.debug('Client details', client_details=client_details)
    return client_details



async def get_config_client_with_client(db: AsyncIOMotorDatabase, config_client_id: str, log) -> Config | None:
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

    log.debug('Pipeline sent', pipeline=pipeline)
    configs = await db.config_clients.aggregate(pipeline).to_list(length=1)
    log.debug('Configs found', configs=configs)

    # Since we used to_list, the result is a list. Return the first (and only) element.
    config = Config.parse_obj(configs[0])
    log.debug('Config found', config=config)
    return config or None


async def get_full_config_client(db: AsyncIOMotorDatabase, config_client_id: str, log: structlog.stdlib.BoundLogger) -> ConfigClient | None:
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


async def get_config_clients_with_client_by_config_id(db: AsyncIOMotorDatabase, config_id: str,  log: structlog.stdlib.BoundLogger) -> list[Config] | None:
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

    # print(pipeline)
    raw_configs = await db.config_clients.aggregate(pipeline).to_list(length=1)  # Adjust length as necessary
    # print(raw_configs)
    # Convert the raw dictionary data into Pydantic Library models
    configs = [ConfigClient.parse_obj(config) for config in raw_configs]

    return configs or None


# Get Library with Library Clients
async def get_library_with_clients(db: AsyncIOMotorDatabase, library_id: str,  log: structlog.stdlib.BoundLogger) -> Library:
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
    return library


async def get_full_config_clients_by_config_id(db: AsyncIOMotorDatabase, config_id: str,  log: structlog.stdlib.BoundLogger) -> list[ConfigClient] | None:
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

    # print(pipeline)
    raw_configs = await db.config_clients.aggregate(pipeline).to_list(length=1000)# Adjust length as necessary
    # print(list(raw_configs))
    # Convert the raw dictionary data into Pydantic Library models
    configs = [ConfigClient.parse_obj(config) for config in raw_configs]

    return configs or None


async def find_lists_containing_item(db: AsyncIOMotorDatabase, media_item_id: str,  log: structlog.stdlib.BoundLogger):

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



async def find_lists_containing_items(db: AsyncIOMotorDatabase, media_item_ids: List[str], log: structlog.stdlib.BoundLogger):
    """
    Find all lists containing a given media item.
    :param db:
    :param media_item_ids:
    :param log:
    :return:
    """
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

    log.debug('Pipeline sent', pipeline=pipeline)
    cursor = db.media_list_items.aggregate(pipeline)
    log.debug('Pipeline result', pipeline=pipeline)
    return await cursor.to_list(None)


