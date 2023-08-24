
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase

async def get_media_list_items_with_media(db: AsyncIOMotorDatabase, list_id: str, max_length: int = 10000) -> List[dict]:
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
        }
    ]

    return await db.media_list_items.aggregate(pipeline).to_list(length=max_length)

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
