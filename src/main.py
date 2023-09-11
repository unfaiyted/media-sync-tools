import sys
import os
# Get the absolute path of the 'src' folder
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(src_path)

from fastapi import FastAPI

from src.config import ConfigManager
from src.routes import poster, images, sync, utils, config, client, lists, users, library, tasks
from src.tasks.scheduler import start_scheduler, stop_scheduler
from src.utils.db_init import DatabaseInitializer


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


@app.on_event("startup")
async def on_startup():
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','config'))
    await DatabaseInitializer(f'{root_path}/config.yml', ConfigManager.get_db()).run()
    start_scheduler()


@app.on_event("shutdown")
async def on_shutdown():
    stop_scheduler()



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

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

