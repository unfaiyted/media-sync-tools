from __future__ import annotations  # Use this to enable postponed evaluation of type annotations

import uuid
from enum import Enum
from pydantic import BaseModel, validator, Field
from typing import List, Optional, ForwardRef
from bson import ObjectId


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
    clientFieldId: str = Field(default_factory=uuid.uuid4)
    clientId: str
    name: str
    placeholderValue: Optional[str] = ''
    type: FieldType


class Client(BaseModel):
    clientId: str = Field(default_factory=uuid.uuid4)
    label: str
    type: ClientType
    name: str
    description: Optional[str] = 'A client'
    libraries: Optional[List[ForwardRef('Library')]]

    @validator('clientId', pre=True, always=True)
    def validate_object_id(cls, value):
        id = value.__str__()
        if id is not None and not isinstance(id, str):
            raise ValueError(f"Invalid ObjectId: {id}")
        return str(value) if isinstance(value, ObjectId) else value
