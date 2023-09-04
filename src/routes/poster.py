import os
from io import BytesIO

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from starlette.responses import StreamingResponse

from src.config import ConfigManager
from src.create.posters import MediaPosterImageCreator
from src.models import MediaListItem, MediaPoster
from typing import List

router = APIRouter()

# Sample data for demonstration purposes
sample_posters_db = {}
async def get_database():
    config_manager = await ConfigManager.get_manager()
    return config_manager.get_db()

@router.get("/posters/{media_list_item_id}", response_model=List[MediaPoster])
async def get_posters_by_media_list_item_id(media_list_item_id: str):
    # TODO: Retrieve posters by MediaListItemId from the database or external service
    if media_list_item_id in sample_posters_db:
        return sample_posters_db[media_list_item_id]
    else:
        return []


@router.get("/item/{mediaListItemId}", response_model=MediaListItem)
async def get_posters_by_provider(mediaListItemId: str ):
    # Get ConfigManager instance
    config_manager = await ConfigManager.get_manager()
    # Get the database instance
    db = config_manager.get_db()
    tmdb = config_manager.get_client('tmdb')

    list_item = await db.media_list_items.find_one({"mediaListItemId": mediaListItemId})

    if list_item is None:
        raise HTTPException(status_code=404, detail="MediaListItem not found")

    # TODO: Retrieve posters by Provider and Identifier from the database or external service
    # Example: Fetch posters from an external service like TMDB or IMDB
    # Replace the logic below with actual API calls to the provider
    print(list_item)

    if list_item['tmdbId'] is not None:
        poster = tmdb.get_movie_poster_path(list_item['tmdbId'])

        await db.media_list_items.replace_one({"mediaListItemId": mediaListItemId}, list_item)

        item = await db.media_items.find_one({"mediaItemId": list_item.mediaItemId})
        item.poster = poster
        await db.media_items.replace_one({"mediaItemId": list_item.mediaItemId}, item)

        list_item.item = item

        return list_item

    movie = tmdb.get_movie_by_name_and_year(list_item['name'], list_item['year'])
    print(movie)

    if movie['total_results'] > 0:
        TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/original"
        poster = tmdb.get_movie_poster_path(movie['results'][0]['id'])

        item = await db.media_items.find_one({"mediaItemId": list_item.mediaItemId})
        item["poster"] = f'{TMDB_IMAGE_URL}{poster}'
        await db.media_items.replace_one({"mediaItemId": list_item.mediaItemId}, item)
        list_item.item = item
        return list_item

    raise HTTPException(status_code=404, detail="Unable to identify poster, not found")


# MediaPoster CRUD operations
@router.post("/", response_model=MediaPoster)
async def create_media_poster(media_poster: MediaPoster):
    db = await get_database()
    # if await db.media_posters.find_one({"mediaPosterId": media_poster.mediaPosterID}):

    # raise HTTPException(status_code=400, detail="MediaPoster already exists")
    media_poster_dict = media_poster.dict()

    poster = MediaPosterImageCreator(media_poster)

    image = poster.create()
    byteArr = BytesIO()
    image.save(byteArr, format='JPEG')
    await db.media_posters.insert_one(media_poster_dict)
    print('Converting to bytes')
    return StreamingResponse(BytesIO(byteArr.getvalue()), media_type="image/jpeg")


@router.get("/", response_model=List[MediaPoster])
async def read_media_posters():
    db = await get_database()
    posters = await db.media_posters.find().to_list(length=None)
    if not posters:
        raise HTTPException(status_code=404, detail="MediaPosters not found")
    return posters


@router.get("/{media_poster_id}", response_model=MediaPoster)
async def read_media_poster(media_poster_id: str):
    db = await get_database()
    poster = await db.media_posters.find_one({"mediaPosterId": media_poster_id})
    if poster is None:
        raise HTTPException(status_code=404, detail="MediaPoster not found")
    return poster


@router.put("/{media_poster_id}", response_model=MediaPoster)
async def update_media_poster(media_poster_id: str, media_poster: MediaPoster):
    db = await get_database()
    existing_poster = await db.media_posters.find_one({"mediaPosterId": media_poster_id})
    if existing_poster is None:
        raise HTTPException(status_code=404, detail="MediaPoster not found")

    poster_dict = media_poster.dict()
    await db.media_posters.replace_one({"mediaPosterId": media_poster_id}, poster_dict)
    return poster_dict


@router.delete("/{media_poster_id}", response_model=MediaPoster)
async def delete_media_poster(media_poster_id: str ):
    db = await get_database()
    poster = await db.media_posters.find_one({"mediaPosterId": media_poster_id})
    if poster is None:
        raise HTTPException(status_code=404, detail="MediaPoster not found")
    await db.media_posters.delete_one({"mediaPosterId": media_poster_id})
    return poster



@router.get("/icons/")
async def list_icons(root_path: str):
    config = await ConfigManager.get_manager()
    if root_path is None:
        root_path = config.get_root_path()

    try:
        files = os.listdir(f"{root_path}/resources/icons")
        return {"filenames": files}
    except Exception as e:
        return {"error": str(e)}

@router.get("/backgrounds/")
async def list_uploads(config_path: str = None):
    config = await ConfigManager.get_manager()
    if config_path is None:
        config_path = config.get_root_path()
    try:

        path = f"{config_path}/uploads"
        files = os.listdir(path)


        # loop over files and map them to text and value objects
        files = list(map(lambda x: {"text": x, "value": f"{path}/{x}"}, files))

        return {"files": files}
    except Exception as e:
        return {"error": str(e)}

@router.post("/background/")
async def upload_file(file: UploadFile = File(...), config_path: str = None):
    if config_path is None:
        config = await ConfigManager.get_manager()
        config_path = config.get_config_path()

    with open(f"{config_path}/uploads/{file.filename}", "wb") as buffer:
        buffer.write(file.file.read())
    return {"filename": file.filename}
