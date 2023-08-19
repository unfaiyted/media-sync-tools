
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


export enum FieldType {
    STRING = 'STRING',
    BOOLEAN = 'BOOLEAN',
    NUMBER = 'NUMBER',
    PASSWORD = 'PASSWORD'

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

export interface MediaList {
    mediaListId?: string;
    name: string;
    type: ListType;
    createdAt: Date;
    sortName: string;
    clientId: string;
    filters?: Filter[];
    items?: MediaListItem[];
    userId: string;
    user?: User;
}

export interface MediaListItem {
    mediaItemId?: string;
    mediaListId: string;
    name: string;
    poster?: string;
    description?: string;
    year: string;
    sourceId?: string;
    releaseDate?: string;
    dateAdded?: Date;
    imdbId?: string;
    tvdbId?: string;
    tmdbId?: string;
    traktId?: string;
    aniList?: string;
    type: MediaType;
    list: any[]; // Adjust this type accordingly
}

export interface MediaListOptions {
    mediaListOptionsId: string;
    mediaListId: string;
    sync: boolean;
    updateImages: boolean;
    configClientId: string;
    includeLibraries?: Library[];
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
    placeholderValue?: string;
    type: FieldType;
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


export interface MediaPosterBorderOptions {
    enabled: boolean;
    width: number;
    height: number;
    color?: [number, number, number];
}

export interface MediaPosterGradientOptions {
    enabled: boolean;
    colors?: [number, number, number][];
    opacity: number;
    type: string;
    angle: number;
}

export interface MediaPosterShadowOptions {
    enabled: boolean;
    color?: [number, number, number];
    offset: number;
    blur: number;
    transparency: number;
}

export interface MediaPosterTextOptions {
    enabled: boolean;
    text?: string;
    position: [number, number];
    color?: [number, number, number];
    border?: MediaPosterBorderOptions;
    shadow?: MediaPosterShadowOptions;
}

export interface MediaPosterBackground {
    enabled: boolean;
    url?: string;
    color?: [number, number, number];
    position: [number, number];
    size: [number, number];
    opacity: number;
    border?: MediaPosterBorderOptions;
    shadow?: MediaPosterShadowOptions;
}

export interface MediaPosterOverlayOptions {
    enabled: boolean;
    text?: string;
    position: string;
    textColor?: [number, number, number];
    backgroundColor?: [number, number, number];
    transparency: number;
    cornerRadius: number;
    border?: MediaPosterBorderOptions;
    shadow?: MediaPosterShadowOptions;
}

export interface MediaPoster {
    mediaPosterID?: string;
    mediaItemId: string;
    url: string;
    width: number;
    height: number;
    type: string;
    border?: MediaPosterBorderOptions;
    text?: MediaPosterTextOptions;
    gradient?: MediaPosterGradientOptions;
    background?: MediaPosterBackground;
    overlays?: MediaPosterOverlayOptions[];
    mediaItem?: string;
}
