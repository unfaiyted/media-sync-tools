import asyncio
import httpx
from pydantic import BaseModel
from fastapi import HTTPException
from bson import ObjectId
# import os
# import sys
from create import PosterImageCreator
from src.create.list_builder import ListBuilder
from src.create.lists import Lists
from src.config import ConfigManager


# src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))

# Add the 'src' folder to the sys.path list
# sys.path.append(src_path)

async def examples(config):
    mdb_list_api = config.get_client('mdb')

    emby = config.get_client('emby')

    # emby_movies = emby.get_media(external_id='imdb.tt6718170')

    # print(emby_movies)

    # poster = emby.get_item_image(emby_movies[0]['Id'])
    # print(f'poster: {poster}')

    # Get list information by list ID

    # mdb_list_api = config.get_client('mdb')

    db = config.get_db()

    class UserBase(BaseModel):
        email: str
        name: str
        password: str

    user = UserBase(email="aaaa", name="asdfasdf", password="asdfasdf")

    async def create_user(user: UserBase):
        user_data = user.dict()
        # Remember to hash the password before inserting
        new_user = await db["users"].insert_one(user_data)
        created_user = await db["users"].find_one({"_id": new_user.inserted_id})
        return created_user

    async def read_user(user_id: str):
        user = await db["users"].find_one({"_id": ObjectId(user_id)})
        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")

    print(await create_user(user))
    print(await read_user("64dbea634299714e95648a0a"))


def main():
    config = ConfigManager()
    # url = "https://www.example.com"
    result = asyncio.run(examples(config))
    # print(result)


if __name__ == "__main__":
    main()
