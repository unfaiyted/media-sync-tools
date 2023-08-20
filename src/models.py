from datetime import datetime
from enum import Enum

from PIL.Image import Image
from pydantic import BaseModel, validator
from typing import List, Optional, ForwardRef, Tuple
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


class FieldType(str, Enum):
    STRING = 'STRING'
    BOOLEAN = 'BOOLEAN'
    NUMBER = 'NUMBER'
    PASSWORD = 'PASSWORD'  # For sensitive data like passwords or API keys


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
    placeholderValue: Optional[str] = ''
    type: FieldType
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


class MediaPosterBorderOptions(BaseModel):
    enabled: bool = False
    width: int = 4
    height: int = 4
    color: Optional[Tuple[int, int, int]] = None


class MediaPosterGradientOptions(BaseModel):
    enabled: bool = False
    colors: Optional[List[Tuple[int, int, int]]] = None
    opacity: float = 0.5
    type: str = 'linear'
    angle: int = -160


class MediaPosterShadowOptions(BaseModel):
    enabled: bool = False
    color: Optional[Tuple[int, int, int]] = None
    offset: int = 5
    blur: int = 3
    transparency: int = 100


class MediaPosterTextOptions(BaseModel):
    enabled: bool = False
    text: Optional[str] = None
    font: Optional[str] = None
    position: Tuple[int, int] = (0, 0)
    color: Optional[Tuple[int, int, int]] = None
    border: Optional[MediaPosterBorderOptions] = None
    shadow: Optional[MediaPosterShadowOptions] = None


class MediaPosterBackground(BaseModel):
    enabled: bool = False
    url: Optional[str] = None
    # image: Optional[Image] = None
    color: Optional[Tuple[int, int, int]] = None
    position: Optional[Tuple[int, int]] = (0, 0)
    opacity: float = 1.0
    border: Optional[MediaPosterBorderOptions] = None
    shadow: Optional[MediaPosterShadowOptions] = None


class MediaPosterIconOptions(BaseModel):
    enabled: bool = False
    path: Optional[str] = None
    position: Tuple[int, int] = (0, 0)
    size: Tuple[int, int] = (100, 100)

class MediaPosterOverlayOptions(BaseModel):
    enabled: bool = False
    text: Optional[str] = None
    icon: Optional[str] = None
    position: str = 'bottom-left'
    textColor: Optional[Tuple[int, int, int]] = (255, 255, 255)
    backgroundColor: Optional[Tuple[int, int, int]] = (100, 100, 100)
    transparency: int = 100
    cornerRadius: int = 5
    border: Optional[MediaPosterBorderOptions] = None
    shadow: Optional[MediaPosterShadowOptions] = None


class MediaImageType(str, Enum):
    UNKNOWN = 'UNKNOWN'
    POSTER = 'POSTER'
    BACKGROUND = 'BACKGROUND'
    BANNER = 'BANNER'
    LOGO = 'LOGO'
    THUMB = 'THUMB'
    CLEARART = 'CLEARART'
    DISCART = 'DISCART'


class IconPosition(str, Enum):
        LEFT = 'LEFT',
        MIDDLE = 'MIDDLE',
        RIGHT = 'RIGHT',
        TOP = 'TOP',
        BOTTOM = 'BOTTOM'

class MediaPoster(BaseModel):
    mediaPosterID: Optional[str] = None
    mediaItemId: Optional[str] = None
    url: Optional[str] = None
    width: int
    height: int
    type: MediaImageType
    border: Optional[MediaPosterBorderOptions]
    text: Optional[MediaPosterTextOptions]
    gradient: Optional[MediaPosterGradientOptions]
    background: Optional[MediaPosterBackground]
    overlays: Optional[List[MediaPosterOverlayOptions]]
    icon: Optional[MediaPosterIconOptions]
    mediaItem: Optional[str]

class MediaPosterIconOptions(BaseModel):
    enabled: bool = False
    path: Optional[str] = None
    position: Tuple[int, int] = (0, 0)
    size: Tuple[int, int] = (100, 100)



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
