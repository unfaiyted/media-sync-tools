from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.config import ConfigManager
from src.models import MediaListItem,  MediaPoster
from typing import List

router = APIRouter()
config = ConfigManager.get_manager()

# Sample data for demonstration purposes
sample_posters_db = {}

@router.get("/posters/{media_list_item_id}", response_model=List[MediaPoster])
async def get_posters_by_media_list_item_id(media_list_item_id: str):
    # TODO: Retrieve posters by MediaListItemId from the database or external service
    if media_list_item_id in sample_posters_db:
        return sample_posters_db[media_list_item_id]
    else:
        return []

@router.get("/from/{provider}/{identifier}", response_model=List[MediaPoster])
async def get_posters_by_provider(provider: str, identifier: str):
    # TODO: Retrieve posters by Provider and Identifier from the database or external service
    # Example: Fetch posters from an external service like TMDB or IMDB
    # Replace the logic below with actual API calls to the provider
    if provider == "tmdb" or provider == "imdb":
        # Fetch posters based on the provider and identifier
        # This is a sample response, replace it with actual data
        sample_posters = [
            Poster(poster_url="https://example.com/poster1.jpg"),
            Poster(poster_url="https://example.com/poster2.jpg")
        ]
        return sample_posters
    else:
        return []


# MediaPoster CRUD operations
@router.post("/", response_model=MediaPoster)
async def create_media_poster(media_poster: MediaPoster, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    if await db.media_posters.find_one({"mediaPosterId": media_poster.mediaPosterID}):
        raise HTTPException(status_code=400, detail="MediaPoster already exists")
    media_poster_dict = media_poster.dict()
    await db.media_posters.insert_one(media_poster_dict)
    return media_poster_dict

@router.get("/", response_model=List[MediaPoster])
async def read_media_posters(db: AsyncIOMotorDatabase = Depends(config.get_db)):
    posters = await db.media_posters.find().to_list(length=None)
    if not posters:
        raise HTTPException(status_code=404, detail="MediaPosters not found")
    return posters

@router.get("/{media_poster_id}", response_model=MediaPoster)
async def read_media_poster(media_poster_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    poster = await db.media_posters.find_one({"mediaPosterId": media_poster_id})
    if poster is None:
        raise HTTPException(status_code=404, detail="MediaPoster not found")
    return poster

@router.put("/{media_poster_id}", response_model=MediaPoster)
async def update_media_poster(media_poster_id: str, media_poster: MediaPoster, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    existing_poster = await db.media_posters.find_one({"mediaPosterId": media_poster_id})
    if existing_poster is None:
        raise HTTPException(status_code=404, detail="MediaPoster not found")

    poster_dict = media_poster.dict()
    await db.media_posters.replace_one({"mediaPosterId": media_poster_id}, poster_dict)
    return poster_dict

@router.delete("/{media_poster_id}", response_model=MediaPoster)
async def delete_media_poster(media_poster_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    poster = await db.media_posters.find_one({"mediaPosterId": media_poster_id})
    if poster is None:
        raise HTTPException(status_code=404, detail="MediaPoster not found")
    await db.media_posters.delete_one({"mediaPosterId": media_poster_id})
    return poster
