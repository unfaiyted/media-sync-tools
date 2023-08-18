from enum import Enum
from pydantic import BaseModel, validator
from typing import List, Optional, ForwardRef
from bson import ObjectId


class MediaListType(str, Enum):
    COLLECTION = "COLLECTION"
    PLAYLIST = "PLAYLIST"
    # ... other types ...


class Provider(str, Enum):
    OPENAI = "OPENAI"
    MDB = "MDB"
    TRAKT = "TRAKT"
    # ... other types ...


class MediaType(str, Enum):
    MOVIE = "MOVIE"
    EPISODE = "EPISODE"
    UNKNOWN = "UNKNOWN"
    SEASON = "SEASON"
    SHOW = "SHOW"
    # ... other types ...


class ClientType(str, Enum):
    UNKNOWN = 'UNKNOWN'
    MEDIA_SERVER = 'MEDIA_SERVER'
    LIST_PROVIDER = 'LIST_PROVIDER'
    UTILITY = 'UTILITY'
    # ... other types ...


class FilterType(str, Enum):
    UNKNOWN = 'UNKNOWN'
    STRING = 'STRING'
    NUMBER = 'NUMBER'
    BOOLEAN = 'BOOLEAN'
    DATE = 'DATE'
    # ... other types ...


class Config(BaseModel):
    configId: str = None
    user: Optional[ForwardRef('User')]
    userId: str
    clients: Optional[List[ForwardRef('ConfigClient')]]
    sync: Optional[ForwardRef('SyncOptions')]


class SyncOptions(BaseModel):
    syncOptionsId: str = None
    configId: str
    collections: bool
    playlists: bool
    lovedTracks: bool
    topLists: bool
    watched: bool
    ratings: bool
    relatedConfig: Optional[ForwardRef('Config')]


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


class MediaListOptions(BaseModel):
    mediaListOptionsId: str
    mediaListId: str
    sync: bool
    configClientId: str
    updateImages: bool
    includeLibraries: Optional[List[ForwardRef('Library')]]
    deleteExisting: bool
    deleteWatchlist: bool


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
    creator: Optional[ForwardRef('User')]
    options: MediaListOptions



class Library(BaseModel):
    libraryId: str = None
    name: str
    clients: Optional[List[ForwardRef('LibraryClient')]]
    Lists: Optional[ForwardRef('MediaList')]


class LibraryClient(BaseModel):
    libraryClientId: Optional[str] = None
    libraryId: str
    libraryName: str
    client: Optional[ForwardRef('Client')]
    clientId: str
    Library: Optional[ForwardRef('Library')]


class MediaListItem(BaseModel):
    mediaItemId: str = None
    mediaListId: str
    name: str
    poster: Optional[str]
    description: Optional[str]
    year: str
    releaseDate: Optional[str]
    dateAdded: Optional[str]
    sourceId: Optional[str]
    imdbId: Optional[str]
    tvdbId: Optional[str]
    tmdbId: Optional[str]
    traktId: Optional[str]
    aniList: Optional[str]
    type: MediaType


class ConfigClient(BaseModel):
    configClientId: str = None
    label: str
    client: Optional[ForwardRef('Client')]
    clientId: str
    relatedConfig: Optional[Config]
    configId: str
    clientFields: Optional[List[ForwardRef('ConfigClientFieldsValue')]]


class ClientField(BaseModel):
    clientFieldId: str = None
    clientId: str
    name: str
    defaultValue: Optional[str] = ''
    ConfigClientFieldsValues: Optional[List[ForwardRef('ConfigClientFieldsValue')]]


class ConfigClientFieldsValue(BaseModel):
    configClientFieldValueId: Optional[str] = None
    configClientFieldId: str
    clientField: Optional[ForwardRef('ClientField')]
    configClientId: str
    value: str


class Client(BaseModel):
    clientId: Optional[str]
    label: str
    type: ClientType
    name: str
    LibraryClients: Optional[List[ForwardRef('LibraryClient')]]
    ConfigClient: Optional[List[ForwardRef('ConfigClient')]]

    @validator('clientId', pre=True, always=True)
    def validate_object_id(cls, value):
        id = value.__str__()
        if id is not None and not isinstance(id, str):
            raise ValueError(f"Invalid ObjectId: {id}")
        return str(value) if isinstance(value, ObjectId) else value


class User(BaseModel):
    userId: str
    email: str
    name: str
    password: str  # Remember to hash passwords before storing
    lists: Optional[List[ForwardRef('MediaList')]]
    relatedConfig: Optional[Config]


# Update the forward references
Config.update_forward_refs()
ConfigClient.update_forward_refs()
MediaList.update_forward_refs()
MediaListItem.update_forward_refs()
MediaListOptions.update_forward_refs()
Library.update_forward_refs()
LibraryClient.update_forward_refs()
Client.update_forward_refs()
ClientField.update_forward_refs()
User.update_forward_refs()
ConfigClientFieldsValue.update_forward_refs()
