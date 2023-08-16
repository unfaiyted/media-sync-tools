export enum ListType {
    COLLECTION = "COLLECTION",
    PLAYLIST = "PLAYLIST",
    // ... other types ...
}

export  enum Provider {
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
    provider: Provider;
    label: string;
    type: string;
    value: string;
    List?: MediaList;
    listListId?: string;
}

export interface MediaList {
    listId?: string;
    name: string;
    type: string;
    sortName: string;
    provider: string;
    filters: Filter[];
    items: ListItem[];
    includeLibraries: Library[];
    userId: string;
    user: User;
}

export interface Library {
    libraryId?: string;
    name: string;
    clients: LibraryClient[];
    List?: MediaList;
}

export interface LibraryClient {
    libraryClientId?: string;
    library_name: string;
    client: Client;
    clientId: string;
    Library: Library;
}

export interface ListItem {
    itemId?: string;
    listId: string;
    name: string;
    poster: string;
    description: string;
    year: string;
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
    configClientFieldsId?: string;
    clientField: ClientField;
    configClientId: string;
    value: string;
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
