from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from src.models import Client, MediaList, MediaListItem, MediaListOptions
from src.config import ConfigManager
from fastapi import APIRouter, HTTPException, Depends

router = APIRouter()
config = ConfigManager.get_manager()


# Define models
# Define routes
# @router.post("/create", response_model=dict)
# async def create(list_data: ListData):
#     try:
#         config = list_data.config
#         list = list_data.list_type
#         data = list_data.list_data
#
#         list_builder = ListBuilder(config, list_type, data)
#         media = list_builder.build()
#
#         if media is not None:
#             response = {
#                 'message': 'List created successfully',
#                 'list_data': data,
#                 'media': media
#             }
#             return response
#         else:
#             raise HTTPException(status_code=500, detail='Unable to create list')
#
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
#


# CRUD operations for List
@router.post("/", response_model=MediaList)
async def create_list(list: MediaList, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    if await db.lists.find_one({"listId": list.listId}):
        raise HTTPException(status_code=400, detail="List already exists")
    list_dict = list.dict()
    await db.lists.insert_one(list_dict)
    return list_dict


@router.get("/{list_id}", response_model=MediaList)
async def read_list(list_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    list_item = await db.lists.find_one({"listId": list_id})
    if list_item is None:
        raise HTTPException(status_code=404, detail="List not found")
    return list_item


@router.put("/{list_id}", response_model=MediaList)
async def update_list(list_id: str, list: MediaList, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_list = await db.lists.find_one({"listId": list_id})
    if existing_list is None:
        raise HTTPException(status_code=404, detail="List not found")

    list_dict = list.dict()
    await db.lists.replace_one({"listId": list_id}, list_dict)
    return list_dict


@router.delete("/{list_id}", response_model=MediaList)
async def delete_list(list_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_list = await db.lists.find_one({"listId": list_id})
    if existing_list is None:
        raise HTTPException(status_code=404, detail="List not found")
    await db.lists.delete_one({"listId": list_id})
    return existing_list


# CRUD operations for ListOptions
@router.post("options/", response_model=MediaListOptions)
async def create_list_options(list_option: MediaListOptions,
                                   db: AsyncIOMotorDatabase = Depends(config.get_db)):
    if await db.listTypeOptions.find_one({"listId": list_option.listId}):
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


@router.post("/item/", response_model=MediaListItem)
async def create_listitem(item: MediaListItem, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    if await db.listitems.find_one({"itemId": item.itemId}):
        raise HTTPException(status_code=400, detail="ListItem already exists")
    item_dict = item.dict()
    result = await db.listitems.insert_one(item_dict)
    return item_dict


@router.get("/item/{item_id}", response_model=MediaListItem)
async def read_listitem(item_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    item = await db.listitems.find_one({"itemId": item_id})
    if item is None:
        raise HTTPException(status_code=404, detail="ListItem not found")
    return item


@router.put("/item/{item_id}", response_model=MediaListItem)
async def update_listitem(item_id: str, item: MediaListItem, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_item = await db.listitems.find_one({"itemId": item_id})
    if existing_item is None:
        raise HTTPException(status_code=404, detail="ListItem not found")

    item_dict = item.dict()
    await db.listitems.replace_one({"itemId": item_id}, item_dict)
    return item_dict


@router.delete("/item/{item_id}", response_model=MediaListItem)
async def delete_listitem(item_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_item = await db.listitems.find_one({"itemId": item_id})
    if existing_item is None:
        raise HTTPException(status_code=404, detail="ListItem not found")
    await db.listitems.delete_one({"itemId": item_id})
    return existing_item

# Get all list items by list id
# Get all lists by user Id
#