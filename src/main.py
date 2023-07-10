from fastapi import FastAPI
from starlette.responses import JSONResponse
from starlette.requests import Request
from src.config import ConfigManager
from src.examples import examples
# Import your sync function here
from src.sync.watchlist import sync_watchlist
from src.sync.collections import sync_collection
from src.create.watchedlists import WatchedListCreator

app = FastAPI()
config_manager = ConfigManager()
@app.get("/sync/watchlist")
async def trigger_sync_watchlist():
    try:
        # Trigger your sync function here.
        # This function might need to be adjusted
        # to work with FastAPI's async functionality.
        sync_watchlist(config_manager)
        wlCreator = WatchedListCreator(config_manager)
        wlCreator.create_previously_watchedlist()


        return JSONResponse(status_code=200, content={"message": "Sync watchlist started successfully."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@app.get("/sync/collection")
async def trigger_sync_collection():
    try:
        sync_collection(config_manager)
        return JSONResponse(status_code=200, content={"message": "Sync collection started successfully."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@app.get("/examples")
async def trigger_examples():
    try:
        examples(config_manager)
        return JSONResponse(status_code=200, content={"message": "Examples started successfully."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@app.post('/webhook')
async def handle_webhook(request: Request):
    # Get the webhook payload from the request
    payload = await request.json()

    # Process the webhook payload and perform the desired operations
    # process_webhook_payload(payload)

    print(payload)
    # Return a response indicating successful processing of the webhook
    return {'message': 'Webhook received and processed successfully'}
