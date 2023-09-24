from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Union

from src.models import Filters
from src.create.providers.app_provider_manager import MediaProviderManager
from src.create.providers.poster import PosterProvider
from src.config import ConfigManager

router = APIRouter()


# Assuming ConfigManager and other classes have been imported.


class Provider(BaseModel):
    client_id: str
    client_details: dict


class UpdateProvider(BaseModel):
    client_details: Optional[dict]


@router.post("/")
async def add_provider(provider: Provider):
    config = await ConfigManager.get_manager()
    app_manager = MediaProviderManager(config)

    if app_manager.add_provider(
        provider.client_id, provider.client_details
    ):
        return {"status": "success", "message": "Provider added."}
    raise HTTPException(status_code=400, detail="Failed to add provider.")


@router.get("/")
async def get_all_providers():
    config = await ConfigManager.get_manager()
    app_manager = MediaProviderManager(config)
    return app_manager.get_providers()


# @router.delete("/{client_id}")
# async def delete_provider(client_id: str):
#     config = await ConfigManager.get_manager()
#     app_manager = AppProviderManager(config)
#     if app_manager.remove_provider(client_id):
#         return {"status": "success", "message": "Provider removed."}
#     raise HTTPException(status_code=404, detail="Provider not found.")
#
#
# @router.put("/{client_id}")
# async def update_provider(client_id: str, updated_provider: UpdateProvider):
#     config = await ConfigManager.get_manager()
#     app_manager = AppProviderManager(config)
#     if app_manager.add_provider(
#         client_id, updated_provider.client_details
#     ):
#         return {"status": "success", "message": "Provider updated."}
#     raise HTTPException(status_code=404, detail="Provider not found or update failed.")
#
#
# @router.get("/{client_id}/list")
# async def get_list_from_provider(client_id: str, filters: Filters):
#     config = await ConfigManager.get_manager()
#     app_manager = AppProviderManager(config)
#     return app_manager.get_list(client_id, filters)
#
#
# @router.get("/{client_id}/list_with_posters")
# async def get_list_with_posters(client_id: str, filters: Filters,
#                                 preferred_poster_provider: Optional[PosterProvider] = None):
#     config = await ConfigManager.get_manager()
#     app_manager = AppProviderManager(config)
#     return app_manager.get_list_with_posters(client_id, filters, preferred_poster_provider)
#
#
# @router.post("/{client_id}/sync/{library_name}")
# async def sync_library(client_id: str, library_name: str):
#     config = await ConfigManager.get_manager()
#     app_manager = AppProviderManager(config)
#     return app_manager.sync_library(client_id, library_name)
