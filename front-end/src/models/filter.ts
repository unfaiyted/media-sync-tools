// FilterType Enum
export enum FilterType {
    EMBY = "EMBY",
    PLEX = "PLEX",
    JELLYFIN = "JELLYFIN",
    TRAKT = "TRAKT",
    TMDB = "TMDB",
    MDB = "MDB"
}

export class BaseFilters {
    filtersId: string;
    clientId: string;
    filterType: FilterType;

    constructor(filtersId: string, clientId: string, filterType: FilterType) {
        this.filtersId = filtersId;
        this.clientId = clientId;
        this.filterType = filterType;
    }

}

export class EmbyFilters extends BaseFilters {
    listId?: string;
    library?: string;
    search?: string;
    limit?: number;
    offset?: number;
    sortBy?: string;
    sortOrder?: string;
    groupProgramsBySeries?: boolean;
    recursive?: boolean;
    includeItemTypes?: string;
    studioIds?: string;
    studioNames?: string;
    is3d?: boolean;
    officialRatings?: string;
    hasTrailer?: boolean;
    hasSpecialFeature?: boolean;
    hasThemeSong?: boolean;
    hasThemeVideo?: boolean;
    hasOverview?: boolean;
    hasImdbId?: boolean;
    hasTmdbId?: boolean;
    hasTvdbId?: boolean;
    audioLanguages?: string;
    videoCodecs?: string;
    audioCodecs?: string;
    isPlayed?: boolean;
    isFavorite?: boolean;
}

export const mockEmbyFilter: EmbyFilters = {
    filtersId: crypto.randomUUID(),
    clientId: 'EMBYCLIENTID',
    filterType: FilterType.EMBY,
    listId: '',
    library: '',
    search: '',
    limit: 0,
    offset: 0,
    sortBy: '',
    sortOrder: '',
    groupProgramsBySeries: false,
    recursive: false,
    includeItemTypes: '',
    studioIds: '',
    studioNames: '',
    is3d: false,
    officialRatings: '',
    hasTrailer: false,
    hasSpecialFeature: false,
    hasThemeSong: false,
    hasThemeVideo: false,
    hasOverview: false,
    hasImdbId: false,
    hasTmdbId: false,
    hasTvdbId: false,
    audioLanguages: '',
    videoCodecs: '',
    audioCodecs: '',
    isPlayed: false,
    isFavorite: false,
};

export class PlexFilters extends BaseFilters {
    listId?: string;
    library?: string;
    listType?: string;
}

export const mockPlexFilter: PlexFilters = {
    filtersId: crypto.randomUUID(),
    clientId: 'PLEXCLIENTID',
    filterType: FilterType.PLEX,
    listId: '',
    library: '',
    listType: '',
}

export class JellyfinFilters extends BaseFilters {
    listId?: string;
    library?: string;
}

export class TraktFilters extends BaseFilters {
    listId?: string;
    listSlug?: string;
}

export class TmdbFilters extends BaseFilters {
    listId?: string;
    page?: number;
    language?: string;
    primaryReleaseYear?: number;
    region?: string;
    releaseDateGte?: string;
    releaseDateLte?: string;
    sortBy?: string;
    voteCountGte?: number;
    voteCountLte?: number;
    voteAverageGte?: number;
    voteAverageLte?: number;
    withCast?: string;
    withCrew?: string;
    withKeywords?: string;
    withRuntimeGte?: number;
    withRuntimeLte?: number;
    withOriginalLanguage?: string;
    withPeople?: string;
    withCompanies?: string;
    withGenres?: string;
    withoutGenres?: string;
    withoutKeywords?: string;
    withoutCompanies?: string;
    withWatchProviders?: string;
    withoutWatchProviders?: string;
    year?: number;
}

export class TmdbShowFilters extends TmdbFilters {
    airDateGte?: string;
    airDateLte?: string;
    firstAirDateYear?: number;
    firstAirDateGte?: string;
    firstAirDateLte?: string;
    withNetworks?: string;
    includeAdult?: boolean;
    screenedTheatrically?: boolean;
    timezone?: string;
    withStatus?: string;
    withType?: string;
}

export class MdbFilters extends BaseFilters {
    listId?: string;
    library?: string;
}

export type Filters = EmbyFilters | PlexFilters | JellyfinFilters | TraktFilters | TmdbFilters | MdbFilters;

type MockFilter = {
    [key in FilterType]: any;  // you can replace `any` with the type of your mock data if you have one
};

export const mockFilter: MockFilter = {
    [FilterType.PLEX]: mockPlexFilter,
    [FilterType.EMBY]: mockEmbyFilter,
    [FilterType.JELLYFIN]: new JellyfinFilters(crypto.randomUUID(), 'JELLYFINCLIENTID', FilterType.JELLYFIN),
    [FilterType.TRAKT]: new TraktFilters(crypto.randomUUID(), 'TRAKTCLIENTID', FilterType.TRAKT),
    [FilterType.TMDB]: new TmdbFilters(crypto.randomUUID(), 'TMDBCLIENTID', FilterType.TMDB),
    [FilterType.MDB]: new MdbFilters(crypto.randomUUID(), 'MDBCLIENTID', FilterType.MDB),
}
