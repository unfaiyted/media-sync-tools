from typing import List, Optional, Any
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient

from src.models import MediaList


async def get_media_list_items_with_media(db: AsyncIOMotorDatabase, list_id: str, skip=0, limit=100) -> List[dict]:
    """
    Retrieve media list items with their associated media.
    """
    pipeline = [
        {
            "$match": {"mediaListId": list_id}
        },
        {
            "$lookup": {
                "from": "media_items",
                "localField": "mediaItemId",
                "foreignField": "mediaItemId",
                "as": "item"
            }
        },
        {
            "$unwind": "$item"
        },
        {
            "$skip": skip
        },
        {
            "$limit": limit
        }
    ]

    return await db.media_list_items.aggregate(pipeline).to_list(length=limit)


async def get_media_list_with_items(db: AsyncIOMotorDatabase, list_id: str, skip=0, limit=10) -> Optional[dict]:
    # Fetch the media list by its ID.
    media_list = await db.media_lists.find_one({"mediaListId": list_id})
    if not media_list:
        return None

    # Fetch associated media list items.
    media_list_items_cursor = db.media_list_items.find({"mediaListId": list_id}).skip(skip).limit(limit)
    media_list_items = await media_list_items_cursor.to_list(length=limit)

    # For each media list item, fetch the associated media item.
    for mli in media_list_items:
        media_item = await db.media_items.find_one({"mediaItemId": mli["mediaItemId"]})
        mli["item"] = media_item

    media_list["items"] = media_list_items

    return media_list


def get_media_list_item_by_id(db: AsyncIOMotorDatabase, item_id: str) -> dict:
    """
    Retrieve a single media list item by its ID.
    """
    return db.media_list_items.find_one({"_id": item_id})


# Add other necessary database operations related to media_list as functions.

async def get_media_list_item_with_media(db: AsyncIOMotorDatabase, list_item_id: str) -> Any | None:
    """
    Retrieve a media list item and its associated media by the list item's ID.
    """
    # Fetch the media list item
    list_item = await db.media_list_items.find_one({"mediaListItemId": list_item_id})

    if not list_item:
        return None

    # Fetch the associated media item
    list_item["item"] = await db.media_items.find_one({"mediaItemId": list_item["mediaItemId"]})

    return list_item


async def get_media_list_by_source_id(db, source_id: str) -> Optional[MediaList]:
    """
    Query the database to find a MediaList by its sourceListId.

    :param db: Database connection or session.
    :param source_id: The sourceListId to search for.
    :return: A MediaList instance if found, otherwise None.
    """

    # The exact query depends on your database setup and choice of ORM or database driver.
    # I'll demonstrate with a hypothetical ORM-like query, but you'll need to adjust to match your actual setup:

    collection = db['media_lists']  # Assuming the collection's name in MongoDB is 'media_lists'
    media_list_document = await collection.find_one({'sourceListId': source_id})
    return MediaList(**media_list_document) if media_list_document else None


async def create_media_list(db: AsyncIOMotorClient, new_media_list: MediaList) -> MediaList:
    collection = db['media_lists']
    result = await collection.insert_one(new_media_list.dict())
    return new_media_list if result.inserted_id else None


def update_media_list(db, mediaListId, matching_collection):
    collections = db['media_lists']
    result = collections.update_one({'mediaListId': mediaListId}, {'$set': matching_collection.dict()})
    return None


def get_media_list_by_id(db, list_id):
    collections = db['media_lists']
    media_list = collections.find_one({'mediaListId': list_id})
    return media_list if media_list else None

async def find_lists_containing_item(db, media_item_id: str):
    # The MongoDB aggregation might look something like this (depending on your schema)
    pipeline = [
        {"$match": {"mediaItemId": media_item_id}},
        {
            "$lookup": {
                "from": "media_lists",
                "localField": "mediaListId",
                "foreignField": "mediaListId",
                "as": "containingList"
            }
        },
        {"$unwind": "$containingList"},
        {
            "$lookup": {
                "from": "media_items",
                "localField": "mediaItemId",
                "foreignField": "mediaItemId",
                "as": "item"
            }
        },
        {"$unwind": "$item"},
    ]

    results = await db.media_list_items.aggregate(pipeline).to_list(length=None)
    # print(results)

    # Parse the results into the desired format
    item_name = results[0]['item']['title'] if results else None
    item_year = results[0]['item']['year'] if results else None

    containing_lists = [
        {
            "listId": str(list_entry['mediaListId']),
            "name": list_entry['containingList']['name'],
            "poster": list_entry['containingList']['poster']
        } for list_entry in results
    ]

    return {
        "mediaItemId": media_item_id,
        "title": item_name,
        "year": item_year,
        "containingLists": containing_lists
    }



async def find_lists_containing_items(db: AsyncIOMotorDatabase, media_list_id: str):

    media_item_ids = await db["media_list_items"].find({"mediaListId": media_list_id}).distinct("mediaItemId")

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
                        "type": "$mediaListDetails.type",
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
# print(result)ef find_lists_containing_item(db, media_item_id):
