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
    COLLECTIONS = 'COLLECTIONS'
    PLAYLISTS = 'PLAYLISTS'
    AUDIOBOOKS = 'AUDIOBOOKS'
    ANIME = 'ANIME'

    # ... other types ...
    @classmethod
    def from_emby(cls, provider_type: str):
        # print(provider_type, 'from_emby')
        if provider_type == 'movies':
            return cls.MOVIES
        elif provider_type == 'tvshows':
            return cls.SHOWS
        elif provider_type == 'music':
            return cls.MUSIC
        elif provider_type == 'playlists':
            return cls.PLAYLISTS
        elif provider_type == 'boxsets':
            return cls.COLLECTIONS
        else:
            return cls.UNKNOWN

    @classmethod
    def from_jellyfin(cls, provider_type: str):
        # print(provider_type, 'from_jellyfin')
        if provider_type == 'movies':
            return cls.MOVIES
        elif provider_type == 'tvshows':
            return cls.SHOWS
        elif provider_type == 'music':
            return cls.MUSIC
        elif provider_type == 'playlists':
            return cls.PLAYLISTS
        elif provider_type == 'boxsets':
            return cls.COLLECTIONS
        else:
            return cls.UNKNOWN

    @classmethod
    def from_plex(cls, type):
        # print(type, 'from_plex')
        if type == 'movie':
            return cls.MOVIES
        elif type == 'show':
            return cls.SHOWS
        elif type == 'artist':
            return cls.MUSIC

        return cls.UNKNOWN

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

