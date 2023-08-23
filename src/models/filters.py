from __future__ import annotations
from enum import Enum

from pydantic import BaseModel, validator
from typing import List, Optional, ForwardRef, Tuple



class FilterType(str, Enum):
    UNKNOWN = 'UNKNOWN'
    STRING = 'STRING'
    NUMBER = 'NUMBER'
    BOOLEAN = 'BOOLEAN'
    DATE = 'DATE'
    # ... other types ...

class Filter(BaseModel):
    filterId: str = None
    filterTypeId: str
    mediaListId: str
    label: str
    type: str
    value: str
    List: Optional[ForwardRef('List')]
    listListId: Optional[str]


class FilterTypes(BaseModel):
    filterTypeId: str = None
    clientId: str
    name: str
    label: str
    type: FilterType

