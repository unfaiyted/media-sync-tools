import json

from src.config import ConfigManager
from src.sync.events import sync_event
from src.create.lists import Lists
from starlette.responses import JSONResponse
from starlette.requests import Request
from fastapi import APIRouter
router = APIRouter()


@router.get("/examples")

async def trigger_examples():
    config_manager = ConfigManager.get_manager()
    try:
        list = Lists(config_manager)

        list.create_emby_ai_recommended_by_genre("AI Recommended (Prev. Watched)", "Previously Watched")

        return JSONResponse(status_code=200, content={"message": "Examples started successfully."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@router.post("/webhook")
async def handle_webhook(request: Request):
    content_type = request.headers.get("Content-Type")

    if content_type.startswith("multipart/form-data"):
        # Handle multipart/form-data request
        boundary = request.headers.get("Content-Type").split("boundary=")[1]
        # Access the parts of the multipart request using the boundary
        parts = await request.form()
        # Process the parts as needed
        data = parts.get("data")

        # Process the form field data as needed,
        # For example, if it contains JSON data, you can parse it
        event = json.loads(data)

        print('Event received')
        sync_event(event, config_manager)
        # Process the extracted data as needed

    return {"message": "Webhook processed successfully"}


@router.get('/recommendations')
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



@router.get('/healthcheck')
async def handle_healthcheck():
    return JSONResponse(status_code=200, content={"message": "Healthy."})


@router.get('/get/command')
async def handle_voice_command():
    return JSONResponse(status_code=200, content={"message": "Healthy."})
