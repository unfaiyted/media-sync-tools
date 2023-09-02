from fastapi import FastAPI, UploadFile, File
import sys
import os

from src.routes import poster, images, sync, utils, config, client, lists, users, library, tasks
from src.tasks.scheduler import start_scheduler, stop_scheduler
from src.utils.db_init import DatabaseInitializer
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
app.include_router(lists.router, prefix="/list", tags=["lists"])
app.include_router(config.router, prefix="/config", tags=["config"])
app.include_router(client.router, prefix="/client", tags=["client"])
app.include_router(users.router, prefix="/user", tags=["users"])
app.include_router(library.router, prefix="/library", tags=["library"])
app.include_router(poster.router, prefix="/poster", tags=["poster"])
app.include_router(tasks.router, prefix="/task", tags=["tasks"])
# app.include_router(filter.router, prefix="/filter", tags=["filter"])

# app.include_router(collections.router, prefix="/collection", tags=["collections"])
# app.include_router(playlists.router, prefix="/playlist", tags=["playlists"])

@app.on_event("startup")
async def on_startup():
    start_scheduler()
    # get root path to src
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','config'))
    await DatabaseInitializer(f'{root_path}/config.yml').run()
    print("Database Initialized..")


@app.on_event("shutdown")
async def on_shutdown():
    stop_scheduler()

#... rest of your FastAPI routes ...
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

