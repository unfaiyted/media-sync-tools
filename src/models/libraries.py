from __future__ import annotations

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
    name: str
    type: LibraryType
    clients: Optional[List[LibraryClient]]
    configId: str


class LibraryClient(BaseModel):
    libraryClientId: Optional[str] = None
    libraryId: str
    libraryName: str
    clientId: str
    mediaListId: Optional[str]
