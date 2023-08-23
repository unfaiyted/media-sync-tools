from __future__ import annotations
from pydantic import BaseModel
from typing import List, Optional

from src.models import ClientField, Client
from src.models import Library
from src.models import User

class Config(BaseModel):
    configId: str = None
    user: Optional[User]
    userId: str
    clients: Optional[List[ConfigClient]]
    libraries: Optional[List[Library]]
    sync: Optional[SyncOptions]

class ConfigClientFieldsValue(BaseModel):
    configClientFieldValueId: Optional[str] = None
    configClientFieldId: str
    clientField: Optional[ClientField]
    configClientId: str
    value: str

class SyncOptions(BaseModel):
    syncOptionsId: str = None
    configId: str
    collections: bool
    playlists: bool
    lovedTracks: bool
    topLists: bool
    watched: bool
    ratings: bool
    relatedConfig: Optional[Config]

class ConfigClient(BaseModel):
    configClientId: str = None
    label: str
    client: Optional[Client]
    clientId: str
    relatedConfig: Optional[Config]
    configId: str
    clientFields: Optional[List[ClientField]]
    clientFieldValues: Optional[List[ConfigClientFieldsValue]]
