from __future__ import annotations  # Use this to enable postponed evaluation of type annotations

from enum import Enum
from pydantic import BaseModel, validator
from typing import List, Optional
from bson import ObjectId

from src.models.libraries import LibraryClient


class ClientType(str, Enum):
    UNKNOWN = 'UNKNOWN'
    MEDIA_SERVER = 'MEDIA_SERVER'
    LIST_PROVIDER = 'LIST_PROVIDER'
    UTILITY = 'UTILITY'
    # ... other types ...


class FieldType(str, Enum):
    STRING = 'STRING'
    BOOLEAN = 'BOOLEAN'
    NUMBER = 'NUMBER'
    PASSWORD = 'PASSWORD'  # For sensitive data like passwords or API keys


class ClientField(BaseModel):
    clientFieldId: str = None
    clientId: str
    name: str
    placeholderValue: Optional[str] = ''
    type: FieldType


class Client(BaseModel):
    clientId: Optional[str]
    label: str
    type: ClientType
    name: str
    LibraryClients: Optional[List[LibraryClient]]
    ConfigClient: Optional[List[ConfigClient]]

    @validator('clientId', pre=True, always=True)
    def validate_object_id(cls, value):
        id = value.__str__()
        if id is not None and not isinstance(id, str):
            raise ValueError(f"Invalid ObjectId: {id}")
        return str(value) if isinstance(value, ObjectId) else value
