from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.models import User
from src.config import ConfigManager

router = APIRouter()


@router.post("/", response_model=User)
async def create_user(user: User):
    db = (await ConfigManager.get_manager()).get_db()
    print('user', user)
    if await db.users.find_one({"userId": user.userId}):
        raise HTTPException(status_code=400, detail="User already registered")
    user_dict = user.dict()
    result = await db.users.insert_one(user_dict)

    # also create a config for this user
    config_dict = {
        "userId": user.userId,
        "configId": user.userId,
        "clients": [],

    }

    config_record = await db.configs.insert_one(config_dict)

    sync_dict = {
            "syncOptionsId": user.userId,
            "configId": user.userId,
            "collections": False,
            "playlists": False,
            "lovedTracks": False,
            "topLists": False,
            "watched": False,
            "ratings": False,
            "relatedConfig": None
        }

    await db.sync_options.insert_one(sync_dict)

    return user_dict

# Get all users
@router.get("/", response_model=list[User])
async def read_all_users():
    db = (await ConfigManager.get_manager()).get_db()
    users = []
    async for user_doc in db.users.find({}):
        # Create a User instance from the retrieved document
        users.append(user_doc)
    if users is None:
        raise HTTPException(status_code=404, detail="User not found")
    return users


@router.get("/{user_id}", response_model=User)
async def read_user(user_id: str):
    db = (await ConfigManager.get_manager()).get_db()
    user = await db.users.find_one({"userId": user_id})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: str, user: User):
    db = (await ConfigManager.get_manager()).get_db()
    existing_user = await db.users.find_one({"userId": user_id})
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_dict = user.dict()
    await db.users.replace_one({"userId": user_id}, user_dict)
    return user_dict


@router.delete("/{user_id}", response_model=User)
async def delete_user(user_id: str):
    db = (await ConfigManager.get_manager()).get_db()
    existing_user = await db.users.find_one({"userId": user_id})
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await db.users.delete_one({"userId": user_id})
    return existing_user
