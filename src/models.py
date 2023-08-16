from enum import Enum
from pydantic import BaseModel
from typing import List, Optional, ForwardRef


class ListType(str, Enum):
    COLLECTION = "COLLECTION"
    PLAYLIST = "PLAYLIST"
    # ... other types ...


class Provider(str, Enum):
    PROVIDER1 = "PROVIDER1"
    PROVIDER2 = "PROVIDER2"
    # ... other types ...


class ClientType(str, Enum):
    TYPE1 = "TYPE1"
    TYPE2 = "TYPE2"
    # ... other types ...


class Config(BaseModel):
    configId: str
    user: ForwardRef('User')
    userId: str
    clients: List[ForwardRef('ConfigClient')]
    sync: ForwardRef('SyncOptions')
    syncOptionsId: str


class SyncOptions(BaseModel):
    syncOptionsId: str
    configId: str
    collections: bool
    playlists: bool
    lovedTracks: bool
    topLists: bool
    watched: bool
    ratings: bool
    relatedConfig: Optional[Config]


class ListTypeOptions(BaseModel):
    listId: str
    type: ListType
    sync: bool
    primaryLibrary: str
    updateImages: bool
    deleteExisting: bool
    deleteWatchlist: bool


class Filter(BaseModel):
    filterId: str
    provider: Provider
    label: str
    type: str
    value: str
    List: Optional[ForwardRef('List')]
    listListId: Optional[str]


class MediaList(BaseModel):
    listId: str
    name: str
    type: str
    sortName: str
    provider: str
    filters: List[Filter]
    items: List[ForwardRef('ListItem')]
    includeLibraries: List[ForwardRef('Library')]
    userId: str
    user: ForwardRef('User')


class Library(BaseModel):
    libraryId: str
    name: str
    clients: List[ForwardRef('LibraryClient')]
    List: Optional[List]


class LibraryClient(BaseModel):
    libraryClientId: str
    library_name: str
    client: ForwardRef('Client')
    clientId: str
    Library: Library


class ListItem(BaseModel):
    itemId: str
    listId: str
    name: str
    poster: str
    description: str
    year: str
    list: List


class ConfigClient(BaseModel):
    configClientId: str
    label: str
    client: ForwardRef('Client')
    clientId: str
    relatedConfig: Config
    configId: str
    clientFields: List[ForwardRef('ConfigClientFieldsValue')]


class ClientField(BaseModel):
    clientFieldId: str
    name: str
    default_value: str
    ConfigClientFieldsValues: List[ForwardRef('ConfigClientFieldsValue')]


class ConfigClientFieldsValue(BaseModel):
    configClientFieldsId: str
    clientField: ClientField
    configClientId: str
    value: str


class Client(BaseModel):
    clientId: str
    label: str
    type: ClientType
    name: str
    LibraryClients: List[LibraryClient]
    ConfigClient: List[ConfigClient]


class User(BaseModel):
    userId: str
    email: str
    name: str
    password: str  # Remember to hash passwords before storing
    lists: List[List]
    relatedConfig: Optional[Config]


# Update the forward references
Config.update_forward_refs()
ConfigClient.update_forward_refs()
MediaList.update_forward_refs()
ListItem.update_forward_refs()
Library.update_forward_refs()
LibraryClient.update_forward_refs()
Client.update_forward_refs()
User.update_forward_refs()
ConfigClientFieldsValue.update_forward_refs()
