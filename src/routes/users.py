from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.models import User
from src.config import ConfigManager

router = APIRouter()
config = ConfigManager.get_manager()


@router.post("/", response_model=User)
async def create_user(user: User, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    if await db.users.find_one({"userId": ObjectId(user.userId)}):
        raise HTTPException(status_code=400, detail="User already registered")
    user_dict = user.dict()
    result = await db.users.insert_one(user_dict)
    return user_dict


@router.get("/{user_id}", response_model=User)
async def read_user(user_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    user = await db.users.find_one({"userId": ObjectId(user_id)})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: str, user: User, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_user = await db.users.find_one({"userId": ObjectId(user_id)})
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_dict = user.dict()
    await db.users.replace_one({"userId": ObjectId(user_id)}, user_dict)
    return user_dict


@router.delete("/{user_id}", response_model=User)
async def delete_user(user_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_user = await db.users.find_one({"userId": ObjectId(user_id)})
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await db.users.delete_one({"userId": ObjectId(user_id)})
    return existing_user
