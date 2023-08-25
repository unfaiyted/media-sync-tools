
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase

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

async def get_media_list_item_with_media(db: AsyncIOMotorDatabase, list_item_id: str) -> dict:
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
