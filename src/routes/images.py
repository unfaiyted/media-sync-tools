from io import BytesIO
from typing import Optional, Tuple

from src.config import ConfigManager
from src.create.posters import PosterImageCreator
from pydantic import BaseModel
from starlette.responses import JSONResponse, StreamingResponse
from fastapi import FastAPI, UploadFile, File, APIRouter
import os

router = APIRouter()

config_manager = ConfigManager.get_manager()

class PosterCreationQuery(BaseModel):
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


@router.post("/poster/create")
async def create_poster(q: PosterCreationQuery):
    print(q)

    try:
        # Create a new PosterImage

        if q.gradientColor1 is not None and q.gradientColor2 is not None:
            poster = PosterImageCreator(400, 600, (q.gradientColor1, q.gradientColor2), q.angle)
        else:
            poster = PosterImageCreator(400, 600, q.selectedGradient, q.angle)

        poster.create_gradient()

        if (q.bgImage is not None):
            poster_path = config_manager.get_config_path() + '/uploads/' + q.bgImage
            print('Adding poster image')
            poster.add_background_image_from_path(poster_path)
        if (q.icon is not None and q.query is not None):
            icon_path = config_manager.get_root_path() + '/resources/icons/' + q.icon
            print('Adding icon with text')
            poster.add_icon_with_text(icon_path, q.query, (250, 200), q.textColor)
        elif (q.icon is not None and q.query is None):
            print('Adding icon')
            icon_path = config_manager.get_root_path() + '/resources/icons/' + q.icon
            poster.add_icon(icon_path, (250, 200))
        elif (q.icon is None and q.query is not None):
            print('Adding text')
            border = [2, (0, 0, 0)]
            shadow = [5, (0, 0, 0), 3, 100]
            poster.draw_text(q.query, q.textColor, (0, 0), border=border, shadow=shadow)

        poster.add_overlay_with_text('TRAILER', 'bottom-left', (100, 100, 100), (255, 255, 255), 100, 5)

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


@router.get("/icons/filenames")
def list_files():
    root_path = config_manager.get_root_path()
    print(root_path)

    try:
        files = os.listdir(root_path + "/resources/icons")
        return {"filenames": files}
    except Exception as e:
        return {"error": str(e)}


@router.get("/uploads/filenames")
def list_uploads_files():
    config_path = config_manager.get_config_path()
    print(config_path)

    try:
        files = os.listdir(config_path + "/uploads")
        return {"files": files}
    except Exception as e:
        return {"error": str(e)}


@router.post("/poster/upload-file")
async def upload_file(file: UploadFile = File(...)):
    config_path = config_manager.get_config_path()
    with open(f"{config_path}/uploads/{file.filename}", "wb") as buffer:
        buffer.write(file.file.read())
    return {"filename": file.filename}
