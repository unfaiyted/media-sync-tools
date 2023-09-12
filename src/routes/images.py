from src.config import ConfigManager
from fastapi import  UploadFile, File, APIRouter
import os

router = APIRouter()


# @router.post("/poster/create")
# async def create_poster(q: PosterCreationQuery):
#     config_manager = await ConfigManager.get_manager()
#     # print(q)
#
#     try:
#         # Create a new PosterImage
#
#         if q.gradientColor1 is not None and q.gradientColor2 is not None:
#             poster = PosterImageCreator(400, 600, (q.gradientColor1, q.gradientColor2), q.angle)
#         else:
#             poster = PosterImageCreator(400, 600, q.selectedGradient, q.angle)
#
#         poster.create_gradient()
#
#         if (q.bgImage is not None):
#             poster_path = config_manager.get_config_path() + '/uploads/' + q.bgImage
#             print('Adding poster image')
#             poster.add_background_image_from_path(poster_path)
#         if (q.icon is not None and q.query is not None):
#             icon_path = config_manager.get_root_path() + '/resources/icons/' + q.icon
#             print('Adding icon with text')
#             poster.add_icon_with_text(icon_path, q.query, (250, 200), q.textColor)
#         elif (q.icon is not None and q.query is None):
#             print('Adding icon')
#             icon_path = config_manager.get_root_path() + '/resources/icons/' + q.icon
#             poster.add_icon(icon_path, (250, 200))
#         elif (q.icon is None and q.query is not None):
#             print('Adding text')
#             border = [2, (0, 0, 0)]
#             shadow = [5, (0, 0, 0), 3, 100]
#             poster.draw_text(q.query, q.textColor, (0, 0), border=border, shadow=shadow)
#
#         poster.add_overlay_with_text('TRAILER', 'bottom-left', (100, 100, 100), (255, 255, 255), 100, 5)
#
#         print('Adding border')
#         poster.add_border(q.borderHeight, q.borderWidth, q.borderColor)
#
#         # Convert the final image to bytes and send it as a response
#         print('Converting to bytes')
#         img_byte_arr = BytesIO()
#         poster.image.save(img_byte_arr, format='JPEG')
#         print('Sending response')
#
#         return StreamingResponse(BytesIO(img_byte_arr.getvalue()), media_type="image/jpeg")
#     except Exception as e:
#         return JSONResponse(status_code=500, content={"message": str(e)})
#

@router.get("/icons/filenames")
async def list_files():
    config_manager = await ConfigManager.get_manager()
    log = config_manager.get_logger(__name__)
    root_path = config_manager.get_root_path()
    log.debug("Listing files", root_path=root_path)
    try:
        files = os.listdir(f"{root_path}/resources/icons")
        log.debug("Files listed", files=files)
        return {"filenames": files}
    except Exception as e:
        log.error("Error listing files", error=str(e))
        return {"error": str(e)}


@router.get("/uploads/filenames")
async def list_uploads_files():
    config_manager = await ConfigManager.get_manager()
    log = config_manager.get_logger(__name__)
    config_path = config_manager.get_config_path()
    try:
        files = os.listdir(f"{config_path}/uploads")
        log.debug('List of files', config_path=config_path)
        return {"files": files}
    except Exception as e:
        return {"error": str(e)}


@router.post("/poster/upload-file")
async def upload_file(file: UploadFile = File(...)):
    config_manager = await ConfigManager.get_manager()
    config_path = config_manager.get_config_path()
    log = config_manager.get_logger(__name__)
    with open(f"{config_path}/uploads/{file.filename}", "wb") as buffer:
        log.debug('Saving file', fileName=file.filename)
        buffer.write(file.file.read())
        log.debug('Save completed', fileName=file.filename)
    return {"filename": file.filename}
