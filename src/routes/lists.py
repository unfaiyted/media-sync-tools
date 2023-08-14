from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from src.create.list_builder import ListBuilder

router = APIRouter()

# Define models
class ListData(BaseModel):
    config: dict
    list_type: str = "Collection"
    list_data: dict = {}


class ListItemData(BaseModel):
    list_id: str
    media_id: str
# Define routes
@router.post("/create", response_model=dict)
async def create(list_data: ListData):
    try:
        config = list_data.config
        list_type = list_data.list_type
        data = list_data.list_data

        list_builder = ListBuilder(config, list_type, data)
        media = list_builder.build()

        if media is not None:
            response = {
                'message': 'List created successfully',
                'list_data': data,
                'media': media
            }
            return response
        else:
            raise HTTPException(status_code=500, detail='Unable to create list')

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.put("/update/{list_id}", response_model=dict)
async def update(list_id: str, list_data: ListData):
    # Implement your logic for updating an existing list
    # Use the list_id to identify the list to be updated
    # You can reuse some of the logic from the create endpoint

@router.delete("/delete/{list_id}", response_model=dict)
async def delete(list_id: str):
    # Implement your logic for deleting an existing list
    # Use the list_id to identify the list to be deleted
    # You might want to implement error handling if the list doesn't exist

@router.post("/add_item_to", response_model=dict)
async def add_item_to(item_data: ListItemData):
    try:
        list_id = item_data.list_id
        media_id = item_data.media_id

        # Implement your logic for adding an item to a list
        # Use list_id to identify the list and media_id to identify the item
        # You can reuse some of the logic from the create endpoint

        response = {
            'message': 'Item added to list successfully',
            'list_id': list_id,
            'media_id': media_id
        }
        return response

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
