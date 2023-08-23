from __future__ import annotations

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, validator
from typing import List, Optional, ForwardRef, Tuple


class MediaListType(str, Enum):
    COLLECTION = "COLLECTION"
    PLAYLIST = "PLAYLIST"
    # ... other types ...

class MediaType(str, Enum):
    MOVIE = "MOVIE"
    EPISODE = "EPISODE"
    UNKNOWN = "UNKNOWN"
    SEASON = "SEASON"
    SHOW = "SHOW"
    # ... other types ...


class MediaListOptions(BaseModel):
    mediaListOptionsId: str
    mediaListId: str
    syncLibraryId: str
    sync: bool
    updateImages: bool
    deleteExisting: bool


class MediaList(BaseModel):
    mediaListId: str = None
    name: str
    type: MediaListType
    sortName: str
    clientId: str  # client provider
    filters: Optional[List[ForwardRef('Filter')]]
    items: Optional[List[ForwardRef('MediaListItem')]]
    includeLibraries: Optional[ForwardRef('Library')]
    creatorId: str
    createdAt: datetime
    creator: Optional[ForwardRef('User')]


class MediaListItem(BaseModel):
    mediaItemId: str = None
    mediaListId: str
    sourceId: Optional[str]
    name: str
    poster: Optional[str]
    description: Optional[str]
    year: str
    releaseDate: Optional[str]
    dateAdded: Optional[datetime]
    imdbId: Optional[str]
    tvdbId: Optional[str]
    tmdbId: Optional[str]
    traktId: Optional[str]
    aniList: Optional[str]
    type: MediaType

