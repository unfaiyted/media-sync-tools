from typing import List, Optional

from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel

from src.models import MediaList, MediaListItem, MediaListOptions
from src.config import ConfigManager
from fastapi import APIRouter, HTTPException, Depends, Query
from src.db.queries import media_list_queries

router = APIRouter()
config = ConfigManager.get_manager()


# LISTS main CRUD operations for List
@router.post("/", response_model=MediaList)
async def create_list(list: MediaList, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    if await db.media_lists.find_one({"mediaListId": list.mediaListId}):
        raise HTTPException(status_code=400, detail="List already exists")
    list_dict = list.dict()
    await db.media_lists.insert_one(list_dict)
    return list_dict


@router.get("/", response_model=List[MediaList])
async def read_lists(db: AsyncIOMotorDatabase = Depends(config.get_db)):
    lists = await db.media_lists.find({}).to_list(length=10000)
    if lists is None:
        raise HTTPException(status_code=404, detail="List not found")
    return lists


@router.get("/{list_id}", response_model=MediaList)
async def read_list(list_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    list_item = await db.media_lists.find_one({"mediaListId": list_id})
    if list_item is None:
        raise HTTPException(status_code=404, detail="List not found")
    return list_item


@router.put("/{list_id}", response_model=MediaList)
async def update_list(list_id: str, list: MediaList, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_list = await db.media_lists.find_one({"mediaListId": list_id})
    if existing_list is None:
        raise HTTPException(status_code=404, detail="List not found")

    list_dict = list.dict()
    await db.media_lists.replace_one({"listId": list_id}, list_dict)
    return list_dict


# get all lists for a user
@router.get("/user/{user_id}", response_model=List[MediaList])
async def read_lists_for_user(user_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    cursor = db.media_lists.find({"creatorId": user_id})
    lists = await cursor.to_list(length=1000)  # adjust the length as per your needs
    if not lists:
        raise HTTPException(status_code=404, detail="List not found")
    return lists


@router.delete("/{list_id}", response_model=MediaList)
async def delete_list(list_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_list = await db.media_lists.find_one({"mediaListId": list_id})
    if existing_list is None:
        raise HTTPException(status_code=404, detail="List not found")
    await db.media_lists.delete_one({"mediaListId": list_id})
    return existing_list


# OPTIONS =  CRUD operations for ListOptions
@router.post("options/", response_model=MediaListOptions)
async def create_list_options(list_option: MediaListOptions,
                              db: AsyncIOMotorDatabase = Depends(config.get_db)):
    if await db.listTypeOptions.find_one({"mediaListId": list_option.mediaListId}):
        raise HTTPException(status_code=400, detail="ListOption already exists")
    list_option_dict = list_option.dict()
    await db.listTypeOptions.insert_one(list_option_dict)
    return list_option_dict


@router.get("options/{list_option_id}", response_model=MediaListOptions)
async def read_list_options(list_option_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    list_option = await db.listTypeOptions.find_one({"listId": list_option_id})
    if list_option is None:
        raise HTTPException(status_code=404, detail="ListOption not found")
    return list_option


@router.put("options/{list_option_id}", response_model=MediaListOptions)
async def update_list_options(list_option_id: str, list_option: MediaListOptions,
                              db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_list_option = await db.listTypeOptions.find_one({"listId": list_option_id})
    if existing_list_option is None:
        raise HTTPException(status_code=404, detail="ListOption not found")

    list_option_dict = list_option.dict()
    await db.listTypeOptions.replace_one({"listId": list_option_id}, list_option_dict)
    return list_option_dict


@router.delete("options/{list_option_id}", response_model=MediaListOptions)
async def delete_list_options(list_option_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_list_option = await db.listTypeOptions.find_one({"listId": list_option_id})
    if existing_list_option is None:
        raise HTTPException(status_code=404, detail="ListOption not found")
    await db.listTypeOptions.delete_one({"listId": list_option_id})
    return existing_list_option


# ITEMS = CRUD operations for ListItems
@router.post("/item/", response_model=MediaListItem)
async def create_listitem(item: MediaListItem, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    if await db.media_list_items.find_one({"mediaListItemId": item.mediaListItemId}):
        raise HTTPException(status_code=400, detail="ListItem already exists")
    item_dict = item.dict()
    result = await db.media_list_items.insert_one(item_dict)
    return item_dict


# get all list items for a give listId
@router.get("/items/{list_id}", response_model=MediaList)
async def read_media_list_items(
        list_id: str,
        skip: int = Query(0, alias="skip", description="Number of records to skip"),
        limit: int = Query(10, alias="limit", description="Max number of records to return"),
        db: AsyncIOMotorDatabase = Depends(config.get_db)
):
    items = await media_list_queries.get_media_list_with_items(db, list_id, skip, limit)
    if not items:
        raise HTTPException(status_code=404, detail="ListItem not found")
    return items


@router.get("/item/{list_item_id}", response_model=MediaListItem)
async def read_listitem(list_item_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    listItem = await media_list_queries.get_media_list_item_with_media(db, list_item_id)
    if listItem is None:
        raise HTTPException(status_code=404, detail="ListItem not found")
    return listItem


@router.put("/item/{item_id}", response_model=MediaListItem)
async def update_listitem(list_item_id: str, item: MediaListItem, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_item = await db.media_list_items.find_one({"mediaListItemId": list_item_id})
    if existing_item is None:
        raise HTTPException(status_code=404, detail="ListItem not found")

    item_dict = item.dict()
    await db.media_list_items.replace_one({"mediaItemId": list_item_id}, item_dict)
    return item_dict


@router.delete("/item/{media_item_id}", response_model=MediaListItem)
async def delete_listitem(media_list_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_item = await db.media_list_items.find_one({"mediaListItemId": media_list_id})
    if existing_item is None:
        raise HTTPException(status_code=404, detail="ListItem not found")
    await db.media_list_items.delete_one({"mediaItemId": media_list_id})
    return existing_item


class MediaListInfo(BaseModel):
    listId: str
    name: str
    type: str
    poster: Optional[str]

class MediaItemResponse(BaseModel):
    mediaItemId: str
    title: str
    year: str
    containingLists: List[MediaListInfo]

class SingleMediaItemResponse(BaseModel):
    mediaItemId: str
    title: str
    year: str
    containingLists: List[MediaListInfo]

@router.get("/item/{media_item_id}/in", response_model=SingleMediaItemResponse)
async def find_lists_containing_item(media_item_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    mlq = await media_list_queries.find_lists_containing_item(db, media_item_id)
    print(mlq)
    return mlq

@router.get("/{media_list_id}/in", response_model=List[MediaItemResponse])
async def find_lists_containing_item(media_list_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    mlq = await media_list_queries.find_lists_containing_items(db, media_list_id=media_list_id)
    print(mlq)
    return mlq
