from __future__ import annotations  # Use this to enable postponed evaluation of type annotations

import uuid
from enum import Enum

from pydantic import BaseModel, validator, Field
from typing import List, Optional, ForwardRef, Tuple, Union


from .clients import Client, ClientField, FieldType, ClientType

from .filters import TmdbFilters, TraktFilters, JellyfinFilters, PlexFilters, EmbyFilters, \
    Filters, FilterType, MdbFilters

from .posters import (MediaPoster, MediaImageType,
                      MediaPosterIconOptions,
                      MediaPosterShadowOptions,
                      MediaPosterBorderOptions,
                      MediaPosterOverlayOptions,
                      MediaPosterTextOptions,
                      MediaPosterBackgroundOptions,
                      MediaPosterGradientOptions)

from .media_lists import (MediaProviderIds,
                          MediaList,
                          MediaListType,
                          MediaListItem,
                          MediaListOptions,
                          MediaItem,
                          MediaListItemType,
                          MediaItemType
                          )
from .libraries import Library, LibraryGroup, LibraryType


class Provider(str, Enum):
    OPENAI = "OPENAI"
    MDB = "MDB"
    TRAKT = "TRAKT"
    JELLYFIN = "JELLYFIN"
    PLEX = "PLEX"
    EMBY = "EMBY"
    TMDB = "TMDB"
    TVDB = "TVDB"
    # ... other types ...


class ProviderType(str, Enum):
    BASE = "BASE"
    LIST = "LIST"
    POSTER = "POSTER"
    LIBRARY = "LIBRARY"


class Config(BaseModel):
    configId: str = Field(default_factory=uuid.uuid4)
    user: Optional[ForwardRef('User')]
    userId: str
    clients: Optional[List[ForwardRef('ConfigClient')]]
    libraries: Optional[List[ForwardRef('Library')]]
    sync: Optional[ForwardRef('SyncOptions')]


class SyncOptions(BaseModel):
    syncOptionsId: str = Field(default_factory=uuid.uuid4)
    configId: str
    collections: bool
    playlists: bool
    lovedTracks: bool
    topLists: bool  # mdb lists
    trakt: bool
    watched: bool
    ratings: bool
    libraries: bool


class ConfigClient(BaseModel):
    configClientId: str = Field(default_factory=uuid.uuid4)
    label: str
    client: Optional[ForwardRef('Client')]
    clientId: str
    relatedConfig: Optional[Config]
    configId: str
    clientFields: Optional[List[ForwardRef('ClientField')]]
    clientFieldValues: Optional[List[ForwardRef('ConfigClientFieldsValue')]]


class ConfigClientFieldsValue(BaseModel):
    configClientFieldValueId: Optional[str] = Field(default_factory=uuid.uuid4)
    configClientFieldId: str
    clientField: Optional[ForwardRef('ClientField')]
    configClientId: str
    value: str


class User(BaseModel):
    userId: str = Field(default_factory=uuid.uuid4)
    email: str
    name: str
    password: str  # Remember to hash passwords before storing
    lists: Optional[List[ForwardRef('MediaList')]]
    relatedConfig: Optional[List[ForwardRef('Config')]]
    configId: Optional[str]


# Update the forward references
Config.update_forward_refs()
ConfigClient.update_forward_refs()
MediaPoster.update_forward_refs()
MediaList.update_forward_refs()
MediaListItem.update_forward_refs()
MediaListOptions.update_forward_refs()
Library.update_forward_refs()
LibraryGroup.update_forward_refs()
Client.update_forward_refs()
ClientField.update_forward_refs()
ConfigClientFieldsValue.update_forward_refs()
User.update_forward_refs()
