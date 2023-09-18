from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Union

from src.config import ConfigManager

router = APIRouter()

# Assuming ConfigManager and other classes have been imported.
config = ConfigManager()
app_manager = AppProviderManager(config)

class Provider(BaseModel):
    client_id: str
    client_details: dict

class UpdateProvider(BaseModel):
    client_details: Optional[dict]

class Filter(BaseModel):
    # Define fields based on your Filters class
    ...

@router.post("/")
async def add_provider(provider: Provider):
    if app_manager.add_provider(
        provider.client_id, provider.client_details
    ):
        return {"status": "success", "message": "Provider added."}
    raise HTTPException(status_code=400, detail="Failed to add provider.")

@router.get("/")
async def get_all_providers():
    return app_manager.get_providers()

@router.delete("/{client_id}")
async def delete_provider(client_id: str):
    if app_manager.remove_provider(client_id):
        return {"status": "success", "message": "Provider removed."}
    raise HTTPException(status_code=404, detail="Provider not found.")

@router.put("/{client_id}")
async def update_provider(client_id: str, updated_provider: UpdateProvider):
    if success := app_manager.add_provider(
        client_id, updated_provider.client_details
    ):
        return {"status": "success", "message": "Provider updated."}
    raise HTTPException(status_code=404, detail="Provider not found or update failed.")

@router.get("/{client_id}/list")
async def get_list_from_provider(client_id: str, filters: Filter):
    return app_manager.get_list(client_id, filters)

@router.get("/{client_id}/list_with_posters")
async def get_list_with_posters(client_id: str, filters: Filter, preferred_poster_provider: Optional[PosterProvider] = None):
    return app_manager.get_list_with_posters(client_id, filters, preferred_poster_provider)

@router.post("/{client_id}/sync/{library_name}")
async def sync_library(client_id: str, library_name: str):
    return app_manager.sync_library(client_id, library_name)
