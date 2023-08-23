export type Color = string | [number, number, number];

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

export enum MediaImageType {
    UNKNOWN = 'UNKNOWN',
    POSTER = 'POSTER',
    BACKGROUND = 'BACKGROUND',
    BANNER = 'BANNER',
    LOGO = 'LOGO',
    THUMB = 'THUMB',
    CLEARART = 'CLEARART',
    DISCART = 'DISCART',
}

export interface Config {
    configId?: string;
    user: User;
    userId: string;
    clients?: ConfigClient[];
    libraries?: Library[];

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
    syncLibraryId: string;
    sync: boolean;
    updateImages: boolean;
    deleteExisting: boolean;
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


export enum LibraryType {
    UNKNOWN = 'UNKNOWN',
    MOVIES = 'MOVIES',
    SHOWS = 'SHOWS',
    MUSIC = 'MUSIC',
    BOOKS = 'BOOKS',
    GAMES = 'GAMES',
    AUDIOBOOKS = 'AUDIOBOOKS',
    ANIME = 'ANIME',

}

export interface Library {
    libraryId?: string;
    configId: string;
    name: string;
    type: LibraryType;
    clients?: LibraryClient[];
    List?: MediaList;
}

export interface LibraryClient {
    libraryClientId?: string;
    libraryId: string;
    libraryName: string;
    client?: Client;
    clientId: string;
    mediaListId?: string;
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
    color?: Color;
}

export interface MediaPosterGradientOptions {
    enabled: boolean;
    colors?: Color[];
    opacity: number;
    type: string;
    angle: number;
}

export interface MediaPosterShadowOptions {
    enabled: boolean;
    color?: Color;
    offset: number;
    blur: number;
    transparency: number;
}

export interface MediaPosterTextOptions {
    enabled: boolean;
    text?: string;
    position: [number, number];
    color?: Color;
    border?: MediaPosterBorderOptions;
    shadow?: MediaPosterShadowOptions;
}

export interface MediaPosterBackgroundOptions {
    enabled: boolean;
    url?: string;
    color?: Color;
    position?: [number, number];
    size?: [number, number];
    opacity: number;
    border?: MediaPosterBorderOptions;
    shadow?: MediaPosterShadowOptions;
}


export interface MediaPosterOverlayOptions {
    enabled: boolean;
    text?: string;
    position: string;
    textColor?: Color;
    backgroundColor?: Color;
    transparency: number;
    cornerRadius: number;
    icon?: MediaPosterIconOptions;
    border?: MediaPosterBorderOptions;
    shadow?: MediaPosterShadowOptions;
}

export interface ProviderPoster {
    providerPosterId?: string;
    providerId: string; // configClientID
    url: string;
    width?: number;
    height?: number;
    type: MediaImageType;

}

export interface MediaPoster {
    mediaPosterId?: string;
    mediaItemId?: string;
    url?: string;
    width: number;
    height: number;
    type: MediaImageType;
    border?: MediaPosterBorderOptions;
    text?: MediaPosterTextOptions;
    gradient?: MediaPosterGradientOptions;
    background?: MediaPosterBackgroundOptions;
    icon?: MediaPosterIconOptions;
    overlays?: MediaPosterOverlayOptions[];
    mediaItem?: string;
}


export enum IconPosition {
    LEFT = 'LEFT',
    MIDDLE = 'MIDDLE',
    RIGHT = 'RIGHT',
    TOP = 'TOP',
    BOTTOM = 'BOTTOM'
}


export interface MediaPosterIconOptions {
    enabled: boolean;
    path?: string;
    position: IconPosition;
    size: [number, number];
}
