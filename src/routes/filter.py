from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from src.models import Filter
from src.config import ConfigManager

router = APIRouter()
config = ConfigManager.get_manager()

# CRUD operations for Filter
@router.post("/", response_model=Filter)
async def create_filter(filter_item: Filter, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    if await db.filters.find_one({"filterId": ObjectId(filter_item.filterId)}):
        raise HTTPException(status_code=400, detail="Filter already exists")
    filter_dict = filter_item.dict()
    await db.filters.insert_one(filter_dict)
    return filter_dict

@router.get("/{filter_id}", response_model=Filter)
async def read_filter(filter_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    filter_item = await db.filters.find_one({"filterId": ObjectId(filter_id)})
    if filter_item is None:
        raise HTTPException(status_code=404, detail="Filter not found")
    return filter_item

@router.put("/{filter_id}", response_model=Filter)
async def update_filter(filter_id: str, filter_item: Filter, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_filter = await db.filters.find_one({"filterId": ObjectId(filter_id)})
    if existing_filter is None:
        raise HTTPException(status_code=404, detail="Filter not found")

    filter_dict = filter_item.dict()
    await db.filters.replace_one({"filterId": ObjectId(filter_id)}, filter_dict)
    return filter_dict

@router.delete("/{filter_id}", response_model=Filter)
async def delete_filter(filter_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_filter = await db.filters.find_one({"filterId": ObjectId(filter_id)})
    if existing_filter is None:
        raise HTTPException(status_code=404, detail="Filter not found")
    await db.filters.delete_one({"filterId": ObjectId(filter_id)})
    return existing_filter
