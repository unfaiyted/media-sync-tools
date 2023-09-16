from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
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
    libraryId: str = Field(default_factory=uuid.uuid4)
    configId: str
    name: str
    createdAt: datetime
    clientId: str
    sourceId: Optional[str]
    mediaListId: Optional[str]
    type: LibraryType

    @classmethod
    def from_plex(cls, provider_library, config_id):
        return cls(
            name=provider_library.title,
            type=LibraryType.from_plex(provider_library.type),
            sourceId=provider_library.key,
            createdAt=datetime.now(),
            configId=config_id,
            clientId='plex',
        )

    @classmethod
    def from_emby(cls, provider_library, config_id):
        return cls(
            name=provider_library['Name'],
            type=LibraryType.from_emby(provider_library.get('CollectionType', LibraryType.UNKNOWN)),
            sourceId=provider_library['Id'],
            createdAt=datetime.now(),
            configId=config_id,
            clientId='emby',
        )

    @classmethod
    def from_jellyfin(cls, provider_library, config_id):
        return cls(
            name=provider_library['Name'],
            type=LibraryType.from_jellyfin(provider_library.get('CollectionType', LibraryType.UNKNOWN)),
            sourceId=provider_library['Id'],
            createdAt=datetime.now(),
            configId=config_id,
            clientId='jellyfin',
        )


# old library model refactors to this
class LibraryGroup(BaseModel):
    libraryGroupId: str = Field(default_factory=uuid.uuid4)
    configId: str
    name: str
    type: LibraryType
    libraries: Optional[List[Library]]

