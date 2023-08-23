import {Filter, ListType,  User} from "@/models";

export enum MediaType {
    UNKNOWN = 'UNKNOWN',
    MOVIE = 'MOVIE',
    EPISODE = 'EPISODE',
    SEASON = 'SEASON',
    SHOW = 'SHOW',
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
