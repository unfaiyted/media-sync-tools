import {ConfigClient, Filters, ListType, MediaPoster, User} from "@/models";

export enum MediaType {
    UNKNOWN = 'UNKNOWN',
    MOVIE = 'MOVIE',
    EPISODE = 'EPISODE',
    SEASON = 'SEASON',
    SHOW = 'SHOW',
}

export enum MediaListType {
    COLLECTION = "COLLECTION",
    PLAYLIST = "PLAYLIST",
    LIBRARY = "LIBRARY",
}

export interface MediaList {
    mediaListId?: string;
    name: string;
    poster?: string | MediaPoster;
    description?: string;
    type: ListType;
    createdAt: Date;
    sortName: string;
    clientId: string;
    filters?: Filters;
    items?: MediaListItem[];
    userId: string;
    user?: User;
}

export interface MediaItem {
    mediaItemId?: string;
    title: string;
    year: string;
    type: MediaType;
    sortTitle: string;
    originalTitle?: string;
    tagline?: string;
    poster?: string;
    description?: string;
    parentalRating?: string;
    genres?: string[];
    releaseDate?: Date;
    dateAdded?: Date;
    providers?: MediaProviderIds;
    ratings?: MediaItemRatings;

}


class MediaItemRatings {
    tmdb?: number;
    imdb?: number;
    trakt?: number;
    metacritic?: number;
    rottenTomatoes?: number;
    tvdb?: number;
    tvRage?: number;
    aniList?: number;
}


export interface MediaProviderIds {
    imdbId?: string;
    tvdbId?: string;
    tmdbId?: string;
    traktId?: string;
    aniList?: string;
}


export interface MediaListItem {
    mediaItemId?: string;
    mediaListId: string;
    type: MediaType;
    name: string;
    sortName: string;
    poster?: string;
    description?: string;
    year: string;
    sourceId?: string;
    createdAt: Date;
    item?: MediaItem;
    dateAdded?: Date;
}

export interface MediaListOptions {
    mediaListOptionsId: string;
    mediaListId: string;
    userId: string;
    type: MediaListType;
    syncLibraryId: string;
    sync: boolean;
    clients: ConfigClient[];
    updateImages: boolean;
    deleteExisting: boolean;
}
