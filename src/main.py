from fastapi import FastAPI, UploadFile, File
import sys
import os
from src.routes import images, sync, utils, config, client, lists, users, library
# Get the absolute path of the 'src' folder
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))

# Add the 'src' folder to the sys.path list
sys.path.append(src_path)

from fastapi.middleware.cors import CORSMiddleware
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


print("Config Manager Loaded. Waiting for Requests...")

app.include_router(images.router, prefix="/image", tags=["images"])
app.include_router(sync.router, prefix="/sync", tags=["sync"])
app.include_router(utils.router, prefix="/util", tags=["utils"])
app.include_router(utils.router, prefix="/list", tags=["lists"])
app.include_router(config.router, prefix="/config", tags=["config"])
app.include_router(client.router, prefix="/client", tags=["client"])
app.include_router(users.router, prefix="/user", tags=["users"])
app.include_router(library.router, prefix="/library", tags=["library"])
# app.include_router(filter.router, prefix="/filter", tags=["filter"])

# app.include_router(collections.router, prefix="/collection", tags=["collections"])
# app.include_router(playlists.router, prefix="/playlist", tags=["playlists"])



#... rest of your FastAPI routes ...
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

