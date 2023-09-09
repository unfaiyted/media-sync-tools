
from dataclasses import field, dataclass
from enum import Enum
from pydantic import BaseModel, validator
from typing import List, Optional, ForwardRef, Tuple, Union


class FilterType(str, Enum):
    EMBY = "EMBY"
    PLEX = "PLEX"
    JELLYFIN = "JELLYFIN"
    TRAKT = "TRAKT"
    TMDB = "TMDB"
    TVDB = "TVDB"
    MDB = "MDB"

class BaseFilters(BaseModel):
    clientId: str
    filterType: FilterType
    filtersId: str

class EmbyFilters(BaseFilters):
    listId: Optional[str] = None
    library: Optional[str] = None
    search: Optional[str] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    sortBy: Optional[str] = None
    sortOrder: Optional[str] = None
    groupProgramsBySeries: Optional[bool] = None
    recursive: Optional[bool] = None
    includeItemTypes: Optional[str] = None
    studioIds: Optional[str] = None
    studioNames: Optional[str] = None
    is3d: Optional[bool] = None
    officialRatings: Optional[str] = None
    hasTrailer: Optional[bool] = None
    hasSpecialFeature: Optional[bool] = None
    hasThemeSong: Optional[bool] = None
    hasThemeVideo: Optional[bool] = None
    hasOverview: Optional[bool] = None
    hasImdbId: Optional[bool] = None
    hasTmdbId: Optional[bool] = None
    hasTvdbId: Optional[bool] = None
    audioLanguages: Optional[str] = None
    videoCodecs: Optional[str] = None
    audioCodecs: Optional[str] = None
    isPlayed: Optional[bool] = None
    isFavorite: Optional[bool] = None

class PlexFilters(BaseFilters):
    listId: Optional[str] = None
    library: Optional[str] = None
    type: Optional[str] = None
    year: Optional[int] = None
    decade: Optional[int] = None
    genre: Optional[str] = None
    country: Optional[str] = None
    studio: Optional[str] = None
    actor: Optional[str] = None
    director: Optional[str] = None
    contentRating: Optional[str] = None
    resolution: Optional[str] = None
    audioChannels: Optional[str] = None
    audioCodec: Optional[str] = None
    videoCodec: Optional[str] = None
    sort: Optional[str] = None
    title: Optional[str] = None
    limit: Optional[int] = None
    offset: Optional[int] = None


class JellyfinFilters(BaseFilters):
    listId: Optional[str] = None
    library: Optional[str] = None
    search: Optional[str] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    sortBy: Optional[str] = None
    sortOrder: Optional[str] = None
    groupProgramsBySeries: Optional[bool] = None
    recursive: Optional[bool] = None
    includeItemTypes: Optional[str] = None
    studioIds: Optional[str] = None
    studioNames: Optional[str] = None
    is3d: Optional[bool] = None
    officialRatings: Optional[str] = None
    hasTrailer: Optional[bool] = None
    hasSpecialFeature: Optional[bool] = None
    hasThemeSong: Optional[bool] = None
    hasThemeVideo: Optional[bool] = None
    hasOverview: Optional[bool] = None
    hasImdbId: Optional[bool] = None
    hasTmdbId: Optional[bool] = None
    hasTvdbId: Optional[bool] = None
    audioLanguages: Optional[str] = None
    videoCodecs: Optional[str] = None
    audioCodecs: Optional[str] = None
    isPlayed: Optional[bool] = None
    isFavorite: Optional[bool] = None

class TraktFilters(BaseFilters):
    listId: Optional[str] = None
    listSlug: Optional[str] = None
    username: Optional[str] = None


class TmdbFilters(BaseFilters):
    listId: Optional[str] = None
    page: Optional[int] = None
    language: Optional[str] = None
    primaryReleaseYear: Optional[int] = None
    region: Optional[str] = None
    releaseDateGte: Optional[str] = None
    releaseDateLte: Optional[str] = None
    sortBy: Optional[str] = None
    voteCountGte: Optional[int] = None
    voteCountLte: Optional[int] = None
    voteAverageGte: Optional[int] = None
    voteAverageLte: Optional[int] = None
    withCast: Optional[str] = None
    withCrew: Optional[str] = None
    withKeywords: Optional[str] = None
    withRuntimeGte: Optional[int] = None
    withRuntimeLte: Optional[int] = None
    withOriginalLanguage: Optional[str] = None
    withPeople: Optional[str] = None
    withCompanies: Optional[str] = None
    withGenres: Optional[str] = None
    withoutGenres: Optional[str] = None
    withoutKeywords: Optional[str] = None
    withoutCompanies: Optional[str] = None
    withWatchProviders: Optional[str] = None
    withoutWatchProviders: Optional[str] = None
    year: Optional[int] =    None

class TvdbFilters(TmdbFilters):
    listId: Optional[str] = None


class TmdbShowFilters(TmdbFilters):
    airDateGte: Optional[str] = None
    airDateLte: Optional[str] = None
    firstAirDateYear: Optional[int] = None
    firstAirDateGte: Optional[str] = None
    firstAirDateLte: Optional[str] = None
    withNetworks: Optional[str] = None
    includeAdult: Optional[bool] = None
    screenedTheatrically: Optional[bool] = None
    timezone: Optional[str] = None
    withStatus: Optional[str] = None
    withType: Optional[str] = None



class MdbFilter(BaseFilters):
    listId: Optional[str] = None
    library: Optional[str] = None


Filters = Optional[Union[PlexFilters, JellyfinFilters, TraktFilters, TmdbFilters, MdbFilter, TvdbFilters, TmdbShowFilters, EmbyFilters]]
