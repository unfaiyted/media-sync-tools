export enum ListType {
    COLLECTION = "COLLECTION",
    PLAYLIST = "PLAYLIST",
    // ... other types ...
}

export  enum Provider {
    UNKNOWN = "UNKNOWN",
    OPENAI = "OPENAI",
    MDB = "MDB",
    TRAKT = "TRAKT",
    // ... other types ...
}

export enum ClientType {
    UNKNOWN = 'UNKNOWN',
    MEDIA_SERVER = 'MEDIA_SERVER',
    LIST_PROVIDER = 'LIST_PROVIDER',
    UTILITY = 'UTILITY'
    // ... other types ...
}

export enum FilterType {
    UNKNOWN = 'UNKNOWN',
    TEXT = 'TEXT',
    NUMBER = 'NUMBER',
    BOOLEAN = 'BOOLEAN',
    DATE = 'DATE',
    // ... other types ...
}

export enum MediaType {
    UNKNOWN = 'UNKNOWN',
    MOVIE = 'MOVIE',
    EPISODE = 'EPISODE',
    SEASON = 'SEASON',
    SHOW = 'SHOW',
}

export interface Config {
    configId?: string;
    user: User;
    userId: string;
    clients?: ConfigClient[];
    sync?: SyncOptions;
}

export interface SyncOptions {
    syncOptionsId?: string;
    configId: string;
    collections: boolean;
    playlists: boolean;
    lovedTracks: boolean;
    topLists: boolean;
    watched: boolean;
    ratings: boolean;
    relatedConfig?: Config;
}

export interface ListTypeOptions {
    listId?: string;
    type: ListType;
    sync: boolean;
    primaryLibrary: string;
    updateImages: boolean;
    deleteExisting: boolean;
    deleteWatchlist: boolean;
}

export interface Filter {
    filterId?: string;
    mediaListId: string;
    filterTypeId: string;
    value: string;
}

export interface FilterTypes {
    filterTypeId: string;
    clientId: string;
    label: string;
    name: string;
    type: FilterType;
}

export interface MediaList {
    listId?: string;
    name: string;
    type: ListType;
    sortName: string;
    configClientId: string;
    filters?: Filter[];
    items?: MediaListItem[];
    includeLibraries?: Library[];
    userId: string;
    user?: User;
}

export interface Library {
    libraryId?: string;
    name: string;
    clients?: LibraryClient[];
    List?: MediaList;
}

export interface LibraryClient {
    libraryClientId?: string;
    libraryId: string;
    libraryName: string;
    client?: Client;
    clientId: string;
    Library?: Library;
}

export interface MediaListItem {
    itemId?: string;
    listId: string;
    name: string;
    poster?: string;
    description?: string;
    year: string;
    sourceId?: string;
    releaseDate?: string;
    dateAdded?: string;
    imdbId?: string;
    tvdbId?: string;
    tmdbId?: string;
    traktId?: string;
    aniList?: string;
    type: MediaType;
    list: any[]; // Adjust this type accordingly
}

export interface ConfigClient {
    configClientId?: string;
    label: string;
    client: Client;
    clientId: string;
    relatedConfig: Config;
    configId: string;
    clientFields: ConfigClientFieldsValue[];
}

export interface ClientField {
    clientFieldId?: string;
    clientId: string;
    name: string;
    defaultValue?: string;
    ConfigClientFieldsValues?: ConfigClientFieldsValue[];
}

export interface ConfigClientFieldsValue {
    configClientFieldValueId?: string; // This is the ID of the value, not the field
    configClientFieldId?: string; // This is the ID of the field, not the value (ClientField)
    clientField?: ClientField; // This is the field object
    configClientId: string; // This is the ID of the client config (ConfigClient)
    value: string; // This is the value of the field
}

export interface Client {
    clientId?: string;
    label: string;
    type: ClientType;
    name: string;
    LibraryClients?: LibraryClient[];
    ConfigClient?: ConfigClient[];
}

export interface User {
    userId?: string;
    email: string;
    name: string;
    password: string; // Remember to hash passwords before storing
    lists?: MediaList[];
    relatedConfig?: Config;
}
