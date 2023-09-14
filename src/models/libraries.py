from __future__ import annotations

from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import List, Optional, ForwardRef


class LibraryType(str, Enum):
    UNKNOWN = 'UNKNOWN'
    MOVIES = 'MOVIES'
    SHOWS = 'SHOWS'
    MUSIC = 'MUSIC'
    GAMES = 'GAMES'
    BOOKS = 'BOOKS'
    AUDIOBOOKS = 'AUDIOBOOKS'
    ANIME = 'ANIME'

    # ... other types ...


class Library(BaseModel):
    libraryId: str = None
    configId: str
    name: str
    createdAt: datetime
    clientId: str
    sourceId: Optional[str]
    mediaListId: Optional[str]
    type: LibraryType


# old library model refactors to this
class LibraryGroup(BaseModel):
    libraryGroupId: str = None
    configId: str
    name: str
    type: LibraryType
    libraries: Optional[List[Library]]

