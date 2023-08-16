from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from src.models import Client, MediaList, ListItem, ListTypeOptions
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
#         list_type = list_data.list_type
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
    if await db.lists.find_one({"listId": ObjectId(list.listId)}):
        raise HTTPException(status_code=400, detail="List already exists")
    list_dict = list.dict()
    await db.lists.insert_one(list_dict)
    return list_dict

@router.get("/{list_id}", response_model=MediaList)
async def read_list(list_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    list_item = await db.lists.find_one({"listId": ObjectId(list_id)})
    if list_item is None:
        raise HTTPException(status_code=404, detail="List not found")
    return list_item

@router.put("/{list_id}", response_model=MediaList)
async def update_list(list_id: str, list: MediaList, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_list = await db.lists.find_one({"listId": ObjectId(list_id)})
    if existing_list is None:
        raise HTTPException(status_code=404, detail="List not found")

    list_dict = list.dict()
    await db.lists.replace_one({"listId": ObjectId(list_id)}, list_dict)
    return list_dict

@router.delete("/{list_id}", response_model=MediaList)
async def delete_list(list_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_list = await db.lists.find_one({"listId": ObjectId(list_id)})
    if existing_list is None:
        raise HTTPException(status_code=404, detail="List not found")
    await db.lists.delete_one({"listId": ObjectId(list_id)})
    return existing_list



# CRUD operations for ListTypeOptions
@router.post("/listtypeoptions/", response_model=ListTypeOptions)
async def create_list_type_options(list_type_option: ListTypeOptions, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    if await db.listTypeOptions.find_one({"listId": ObjectId(list_type_option.listId)}):
        raise HTTPException(status_code=400, detail="ListTypeOption already exists")
    list_type_option_dict = list_type_option.dict()
    await db.listTypeOptions.insert_one(list_type_option_dict)
    return list_type_option_dict

@router.get("/listtypeoptions/{list_type_option_id}", response_model=ListTypeOptions)
async def read_list_type_options(list_type_option_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    list_type_option = await db.listTypeOptions.find_one({"listId": ObjectId(list_type_option_id)})
    if list_type_option is None:
        raise HTTPException(status_code=404, detail="ListTypeOption not found")
    return list_type_option

@router.put("/listtypeoptions/{list_type_option_id}", response_model=ListTypeOptions)
async def update_list_type_options(list_type_option_id: str, list_type_option: ListTypeOptions, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_list_type_option = await db.listTypeOptions.find_one({"listId": ObjectId(list_type_option_id)})
    if existing_list_type_option is None:
        raise HTTPException(status_code=404, detail="ListTypeOption not found")

    list_type_option_dict = list_type_option.dict()
    await db.listTypeOptions.replace_one({"listId": ObjectId(list_type_option_id)}, list_type_option_dict)
    return list_type_option_dict

@router.delete("/listtypeoptions/{list_type_option_id}", response_model=ListTypeOptions)
async def delete_list_type_options(list_type_option_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_list_type_option = await db.listTypeOptions.find_one({"listId": ObjectId(list_type_option_id)})
    if existing_list_type_option is None:
        raise HTTPException(status_code=404, detail="ListTypeOption not found")
    await db.listTypeOptions.delete_one({"listId": ObjectId(list_type_option_id)})
    return existing_list_type_option

@router.post("/listitem/", response_model=ListItem)
async def create_listitem(item: ListItem, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    if await db.listitems.find_one({"itemId": ObjectId(item.itemId)}):
        raise HTTPException(status_code=400, detail="ListItem already exists")
    item_dict = item.dict()
    result = await db.listitems.insert_one(item_dict)
    return item_dict


@router.get("/listitem/{item_id}", response_model=ListItem)
async def read_listitem(item_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    item = await db.listitems.find_one({"itemId": ObjectId(item_id)})
    if item is None:
        raise HTTPException(status_code=404, detail="ListItem not found")
    return item


@router.put("/listitem/{item_id}", response_model=ListItem)
async def update_listitem(item_id: str, item: ListItem, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_item = await db.listitems.find_one({"itemId": ObjectId(item_id)})
    if existing_item is None:
        raise HTTPException(status_code=404, detail="ListItem not found")

    item_dict = item.dict()
    await db.listitems.replace_one({"itemId": ObjectId(item_id)}, item_dict)
    return item_dict


@router.delete("/listitem/{item_id}", response_model=ListItem)
async def delete_listitem(item_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_item = await db.listitems.find_one({"itemId": ObjectId(item_id)})
    if existing_item is None:
        raise HTTPException(status_code=404, detail="ListItem not found")
    await db.listitems.delete_one({"itemId": ObjectId(item_id)})
    return existing_item
