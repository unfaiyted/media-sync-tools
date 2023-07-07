from fastapi import FastAPI
from starlette.responses import JSONResponse
from src.config import ConfigManager
# Import your sync function here
from sync.watchlist import sync_watchlist

app = FastAPI()
config_manager = ConfigManager()

print(config_manager.get_config_path())

@app.get("/sync")
async def trigger_sync():
    try:
        # Trigger your sync function here.
        # This function might need to be adjusted
        # to work with FastAPI's async functionality.
        sync_watchlist(config_manager)
        return JSONResponse(status_code=200, content={"message": "Sync started successfully."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
