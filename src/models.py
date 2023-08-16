from enum import Enum
from pydantic import BaseModel, validator
from typing import List, Optional, ForwardRef
from bson import ObjectId


class ListType(str, Enum):
    COLLECTION = "COLLECTION"
    PLAYLIST = "PLAYLIST"
    # ... other types ...


class Provider(str, Enum):
    OPENAI = "OPENAI"
    MDB = "MDB"
    TRAKT = "TRAKT"
    # ... other types ...


class ClientType(str, Enum):
    UNKNOWN = 'UNKNOWN'
    MEDIA_SERVER = 'MEDIA_SERVER'
    LIST_PROVIDER = 'LIST_PROVIDER'
    UTILITY = 'UTILITY'
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


class ListTypeOptions(BaseModel):
    listId: str = None
    type: ListType
    sync: bool
    primaryLibrary: str
    updateImages: bool
    deleteExisting: bool
    deleteWatchlist: bool


class Filter(BaseModel):
    filterId: str = None
    provider: Provider
    label: str
    type: str
    value: str
    List: Optional[ForwardRef('List')]
    listListId: Optional[str]


class MediaList(BaseModel):
    listId: str = None
    name: str
    type: str
    sortName: str
    provider: str
    filters: List[ForwardRef('Filter')]
    items: List[ForwardRef('ListItem')]
    includeLibraries: List[ForwardRef('Library')]
    userId: str
    user: ForwardRef('User')


class Library(BaseModel):
    libraryId: str = None
    name: str
    clients: List[ForwardRef('LibraryClient')]
    List: Optional[ForwardRef('MediaList')]


class LibraryClient(BaseModel):
    libraryClientId: str = None
    library_name: str
    client: ForwardRef('Client')
    clientId: str
    Library: Library


class ListItem(BaseModel):
    itemId: str = None
    listId: str
    name: str
    poster: str
    description: str
    year: str
    list: List


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
    configClientFieldsId: str = None
    clientField: ClientField
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
ListItem.update_forward_refs()
Library.update_forward_refs()
LibraryClient.update_forward_refs()
Client.update_forward_refs()
ClientField.update_forward_refs()
User.update_forward_refs()
ConfigClientFieldsValue.update_forward_refs()
