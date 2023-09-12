from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import List, ForwardRef, Optional, Union

from pydantic import BaseModel, validator

from src.models.posters import MediaPoster

from src.models import Filters, FilterType, TraktFilters, PlexFilters, JellyfinFilters, \
    TmdbFilters, EmbyFilters, MdbFilters


class MediaType(str, Enum):
    MOVIE = "MOVIE"
    EPISODE = "EPISODE"
    UNKNOWN = "UNKNOWN"
    SEASON = "SEASON"
    SHOW = "SHOW"
    # ... other types ...


class MediaListType(str, Enum):
    COLLECTION = "COLLECTION"
    PLAYLIST = "PLAYLIST"
    LIBRARY = "LIBRARY"
    # ... other types ...


class MediaListOptions(BaseModel):
    mediaListOptionsId: str
    userId: str
    type: MediaListType
    clients: List[ForwardRef('ConfigClient')]
    mediaListId: str
    syncLibraryId: str
    sync: bool
    updateImages: bool
    deleteExisting: bool


class MediaList(BaseModel):
    sourceListId: Optional[str]
    mediaListId: str = None
    clientId: str  # client provider
    creatorId: str
    sourceListId: Optional[str]
    name: str
    poster: Optional[Union[str, ForwardRef('MediaPoster')]]
    type: MediaListType
    sortName: str
    description: Optional[str] = None
    filters: Optional[Filters]
    items: Optional[List[ForwardRef('MediaListItem')]]
    createdAt: datetime
    creator: Optional[ForwardRef('User')]

    @validator('filters', pre=True, always=True)
    # Filters were picking the wrong time on serialization
    def set_correct_filter_type(cls, filters):
        if filters is None:
            return None

        filter_type = filters['filterType']

        if filter_type == FilterType.TRAKT:
            return TraktFilters(**filters)
        elif filter_type == FilterType.PLEX:
            return PlexFilters(**filters)
        elif filter_type == FilterType.JELLYFIN:
            return JellyfinFilters(**filters)
        elif filter_type == FilterType.TMDB:
            return TmdbFilters(**filters)
        elif filter_type == FilterType.EMBY:
            return EmbyFilters(**filters)
        elif filter_type == FilterType.MDB:
            return MdbFilters(**filters)

        raise ValueError(f"Unknown filter type: {filter_type}")


class MediaProviderIds(BaseModel):
    imdbId: Optional[str]
    tvdbId: Optional[str]
    tmdbId: Optional[str]
    traktId: Optional[str]
    tvRageId: Optional[str]
    rottenTomatoesId: Optional[str]
    aniListId: Optional[str]


class MediaItemRatings(BaseModel):
    tmdb: Optional[float]
    imdb: Optional[float]
    trakt: Optional[float]
    metacritic: Optional[float]
    rottenTomatoes: Optional[float]
    tvdb: Optional[float]
    aniList: Optional[float]


class MediaItem(BaseModel):
    mediaItemId: str = None
    title: str
    year: Optional[str]
    type: MediaType
    sortTitle: Optional[str]
    originalTitle: Optional[str]
    tagline: Optional[str]
    poster: Optional[str]
    description: Optional[str]
    parentalRating: Optional[str]
    genres: Optional[List[str]]
    releaseDate: Optional[str]
    dateAdded: Optional[datetime]
    providers: Optional[MediaProviderIds]
    ratings: Optional[MediaItemRatings]


class MediaListItem(BaseModel):
    mediaListItemId: str = None
    mediaListId: str
    mediaItemId: str
    poster: Optional[ForwardRef('MediaPoster')]
    mediaPosterId: Optional[str]
    item: Optional[ForwardRef('MediaItem')]
    dateAdded: Optional[datetime]
