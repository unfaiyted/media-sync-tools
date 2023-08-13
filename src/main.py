from io import BytesIO
from typing import Optional, Tuple

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from starlette.responses import JSONResponse, StreamingResponse
from starlette.requests import Request

import sys
import os

from src.create.posters import PosterImageCreator
from src.create.list_builder import ListBuilder

# Get the absolute path of the 'src' folder
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))

# Add the 'src' folder to the sys.path list
sys.path.append(src_path)
# from create.list_builder import ListBuilder
from src.config import ConfigManager
# from src.examples import examples
from src.create.toplists import sync_top_lists
# Import your sync function here
from src.sync.watchlist import sync_watchlist
from src.sync.collections import sync_collections
from src.sync.events import sync_event
from src.create.lists import Lists
from src.create.trakt import sync_trakt_user_lists
from src.create.playlists import create_emby_playlist
from fastapi.middleware.cors import CORSMiddleware
import json
import uvicorn

app = FastAPI(debug=True)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#... rest of your FastAPI routes ...
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

config_manager = ConfigManager()
print("Config Manager Loaded. Waiting for Requests...")


@app.get("/sync/watchlist")
async def trigger_sync_watchlist():
    try:
        # Trigger your sync function here.
        # This function might need to be adjusted
        # to work with FastAPI's async functionality.
        sync_watchlist(config_manager)
        list_maker = Lists(config_manager)
        list_maker.create_previously_watchedlist()

        return JSONResponse(status_code=200, content={"message": "Sync watchlist started successfully."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@app.get("/sync/playlist")
async def trigger_sync_playlist():
    try:

        name = 'Sleeping Shows'

        shows = [
                 'How I Met Your Mother',
                 'Ancient Aliens',
                 'Bob\'s Burgers',
                 'Bojack Horseman',
                 'Forensic Files',
                 'Downton Abbey',
                 'Parks and Recreation',
                 '30 Rock',
                 'Daria',
                 'Better Off Ted',
                 'The Good Place',
                 'The Office (US)',
                 'Friends',
                 'Rick and Morty'
                    ]

        create_emby_playlist(config_manager, name, shows)



        return JSONResponse(status_code=200, content={"message": "Sync watchlist started successfully."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
@app.get("/sync/top-lists")
async def trigger_sync_toplist():
    try:
        sync_top_lists(config_manager)


        return JSONResponse(status_code=200, content={"message": "Sync watchlist started successfully."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})



@app.get("/sync/collections")
async def trigger_sync_collection():
    settings = config_manager.get_collection_settings()

    try:

        print('Syncing Collections', settings['sync'])
        if settings['sync']:
            print("Sync collection is enabled.")
            sync_collections(config_manager)
        else:
            print("Sync collection is disabled.")


        return JSONResponse(status_code=200, content={"message": "Sync collections successfully."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@app.get("/examples")
async def trigger_examples():
    try:
        # examples(config_manager)

        #
        #        list1 = ListBuilder(config_manager)
        #
        #        list1\
        #            .type('collection')\
        #            .name('AI Recommended (Prev. Watched)')\
        #            .source('Previously Watched')\
        #            .build()
        #
        #        list2 = ListBuilder(config_manager)
        #
        #        list2\
        #            .type('collection')\
        #            .name('AI Recommended (Watchlist)')\
        #            .source('Watchlist')\
        #            .build()
        #
        #
        #
        #        list3 = ListBuilder(config_manager, list)

        list = Lists(config_manager)

        list.create_emby_ai_recommended_by_genre("AI Recommended (Prev. Watched)", "Previously Watched")

        return JSONResponse(status_code=200, content={"message": "Examples started successfully."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@app.post("/webhook")
async def handle_webhook(request: Request):
    content_type = request.headers.get("Content-Type")

    if content_type.startswith("multipart/form-data"):
        # Handle multipart/form-data request
        boundary = request.headers.get("Content-Type").split("boundary=")[1]
        # Access the parts of the multipart request using the boundary
        parts = await request.form()
        # Process the parts as needed
        data = parts.get("data")

        # Process the form field data as needed
        # For example, if it contains JSON data, you can parse it
        event = json.loads(data)

        print('Event received')
        sync_event(event, config_manager)
        # Process the extracted data as needed

    return {"message": "Webhook processed successfully"}


@app.get('/recommendations')
async def handle_recommendations():
    list_maker = Lists(config_manager)

    # list_maker.create_emby_ai_recommended_by_collection("AI Recommended (Prev. Watched)", "Previously Watched")
    # list_maker.create_emby_ai_recommended_by_watched("AI Recommended (All Watched)")
    # list_maker.create_emby_ai_recommended_by_favorites("AI Recommended (Favorites)")
    # list_maker.create_emby_ai_recommended_by_genre("AI Recommended (Action)", "Action")
    # collection = list_maker.create_emby_ai_recommended_by_prompt("AI Recommended (Cult Classics)", prompt="Cult Classic Movies")
    # collection = list_maker.create_emby_ai_recommended_by_genre("AI Recommended (Thriller)", "Thriller")
    print("Creating collection")
    # collection = list_maker.create_emby_ai_recommended_by_watched("AI (Prev. Watched)", 50)
    collection = list_maker.create_emby_ai_recommended_by_favorites("AI (Favorites)", 50)
    collection = list_maker.create_emby_ai_recommended_by_prompt("AI Recommended (Dark)",
                                                                 prompt="Movies with a really dark and twisted theme.")
    collection = list_maker.create_emby_ai_recommended_by_prompt("AI Recommended (Thriller)",
                                                                 prompt="Thriller movies that will keep you on the edge of your seat.")
    collection = list_maker.create_emby_ai_recommended_by_prompt("AI Recommended (Action)",
                                                                 prompt="Action movies that will keep you on the edge of your seat.")
    collection = list_maker.create_emby_ai_recommended_by_prompt("AI Recommended (Cult Classics)",
                                                                 prompt="Cult Classic Movies")
    collection = list_maker.create_emby_ai_recommended_by_prompt("AI Recommended (Weird Kids)",
                                                                 prompt="Kids movies that have a weird and twisted theme.")

    # collection = list_maker.create_emby_ai_recommended_by_prompt("AI (Weird Kids)", prompt="Kids movies that have a weird and twisted theme.")

    return JSONResponse(status_code=200, content={"message": f"Recommendations started successfully",
                                                  "collection": collection})
    # find the movies from the json_data
    # add the movies to the collection


@app.get('/sync/trakt')
async def handle_trakt():
    try:

        sync_trakt_user_lists(config_manager, 'faiyt')

        return JSONResponse(status_code=200, content={"message": "User lists synced from Trakt",})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@app.get('/sync/config')
async def handle_config():
    # get playlist from config

    # get collections from config
    collections = config_manager.collections.get('lists', {})

    playlists = config_manager.playlists.get('lists', {})

    # for collection in collections:
    #     print(collections[collection])
    #     list = ListBuilder(config_manager, "Collection", collections[collection])
    #     list.build()

    # for playlist in playlists:

    # list = ListBuilder(config_manager, "Playlist", playlists[playlist])
    # list.build()

    return JSONResponse(status_code=200, content={"message": "Config started successfully.", "collections": collections,
                                                  "playlists": playlists})


@app.get('/healthcheck')
async def handle_healthcheck():
    return JSONResponse(status_code=200, content={"message": "Healthy."})


@app.get('/get/command')
async def handle_voice_command():
    return JSONResponse(status_code=200, content={"message": "Healthy."})


from pydantic import BaseModel

class SearchQuery(BaseModel):
    query: str = None

    borderWidth: int = 4
    borderHeight: int = 4
    selectedGradient: str = 'random'
    angle: int = -160
    bgImage: str = None
    icon: str = None
    gradientColor1: Optional[Tuple[int, int, int]] = None
    gradientColor2: Optional[Tuple[int, int, int]] = None
    textColor: tuple = (255, 255, 255)
    borderColor: tuple = (0, 0, 0)


@app.post("/poster/create")
async def create_poster(q: SearchQuery):
    print(q)
    try:
        # Create a new PosterImage

        if q.gradientColor1 is not None and q.gradientColor2 is not None:
            poster = PosterImageCreator(400, 600, (q.gradientColor1, q.gradientColor2), q.angle)
        else:
            poster = PosterImageCreator(400, 600, q.selectedGradient, q.angle)

        poster.create_gradient()


        if(q.bgImage is not None):
             poster_path = config_manager.get_config_path() +'/uploads/' + q.bgImage
             print('Adding poster image')
             poster.add_background_image_from_path(poster_path)
        if(q.icon is not None and q.query is not None):
            icon_path = config_manager.get_root_path() +'/resources/icons/' + q.icon
            print('Adding icon with text')
            poster.add_icon_with_text(icon_path, q.query, (250,200), q.textColor)
        elif(q.icon is not None and q.query is None):
            print('Adding icon')
            icon_path = config_manager.get_root_path() +'/resources/icons/' + q.icon
            poster.add_icon(icon_path, (250,200))
        elif(q.icon is None and q.query is not None):
            print('Adding text')
            border= [2,(0,0,0)]
            poster.draw_text(q.query,  q.textColor, (0,0), border=border)


        print('Adding border')
        poster.add_border(q.borderHeight, q.borderWidth, q.borderColor)

        # Convert the final image to bytes and send it as a response
        print('Converting to bytes')
        img_byte_arr = BytesIO()
        poster.image.save(img_byte_arr, format='JPEG')
        print('Sending response')

        return StreamingResponse(BytesIO(img_byte_arr.getvalue()), media_type="image/jpeg")
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@app.get("/icons/filenames")
def list_files():

    root_path = config_manager.get_root_path()
    print(root_path)

    try:
        files = os.listdir(root_path + "/resources/icons")
        return {"filenames": files}
    except Exception as e:
        return {"error": str(e)}


@app.get("/uploads/filenames")
def list_uploads_files():

    config_path = config_manager.get_config_path()
    print(config_path)

    try:
        files = os.listdir(config_path + "/uploads")
        return {"files": files}
    except Exception as e:
        return {"error": str(e)}
@app.post("/poster/upload-file")
async def upload_file(file: UploadFile = File(...)):
    config_path = config_manager.get_config_path()
    with open(f"{config_path}/uploads/{file.filename}", "wb") as buffer:
        buffer.write(file.file.read())
    return {"filename": file.filename}
