
from dataclasses import field, dataclass
from enum import Enum

import structlog
from pydantic import BaseModel, validator, Field
from typing import List, Optional, ForwardRef, Tuple, Union, Dict, Annotated
import re



class FilterType(str, Enum):
    EMBY = "EMBY"
    PLEX = "PLEX"
    JELLYFIN = "JELLYFIN"
    TRAKT = "TRAKT"
    TMDB = "TMDB"
    TVDB = "TVDB"
    MDB = "MDB"


class BaseFilters(BaseModel):
    _log = structlog.get_logger(__name__)
    clientId: str
    filterType: FilterType
    filtersId: str
    _invalid_keys: List[str] = ["clientId", "filterType", "filtersId"]  # Blocklist items, get rid of
    _valid_keys: List[str] = []  # Pass-list Items, keep

    _key_remapping = {}


    class Config:
        json_exclude = {'log'}
        json_exclude_unset = True
        allow_population_by_field_name = True

    def to_query_params(self) -> Dict:
        """Convert object attributes to a dictionary of non-None values."""
        return {k: v for k, v in self.__dict__.items() if v is not None}

    def remove_invalid_keys(self, filters: Dict[str, str]) -> Dict[str, str]:
        """Remove invalid keys from the filters dict."""
        for key in self._invalid_keys:
            self._log.debug("Removing invalid key", key=key)
            filters.pop(key, None)
        return filters

    def filter_invalid_keys(self, filters: Dict[str, str]) -> Dict[str, str]:
        """Filter to ensure only valid keys are in the filters dict."""
        if not self._valid_keys:
            self._log.debug("No valid keys set. Returning filters as-is.")
            return filters

        for key in self._valid_keys:
            self._log.debug("Filtering invalid key", key=key)
            filters.pop(key, None)
        return filters

    @staticmethod
    def to_snake_case(string: str) -> str:
        """Convert camelCase to snake_case."""
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def parse_filters(self) -> Dict[str, str]:
        """Parse the filter's dict."""
        parsed_filters = {}
        self._log.info("Parsing filters", filters=self.dict())

        filters = self.dict()
        filters = self.remove_invalid_keys(filters)  # Remove invalid keys
        filters = self.filter_invalid_keys(filters)  # Pass-list to ensure only valid keys

        for key, value in filters.items():
            self._log.debug("Parsing filter", key=key, value=value)
            # Rename keys if needed
            new_key = self._key_remapping.get(key, key)
            # Convert camelCase to snake_case
            new_key = self.to_snake_case(new_key)
            parsed_filters[new_key] = value

        self._log.debug("Parsed filters", parsed_filters=parsed_filters)
        return parsed_filters


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

    # Keys that shouldn't be passed to Plex
    _invalid_keys: List[str] = ["clientId", "filterType", "filtersId"]

    # Keys that need to be renamed for Plex
    _key_remapping = {
        'offset': 'container_start',
        'limit': 'maxresults',
        'type': 'libtype',
    }

    # Passlist to ensure only these keys are passed to Plex
    _valid_filters = {
        'title', 'studio', 'genre', 'contentRating', 'decade',
        'genre', 'actor', 'country', 'studio', 'actor', 'libtype'
        'director', 'resolution', 'producer', 'actor', 'country',
        'addedAt', 'sort', 'year', 'maxresults', 'libtype'
    }


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



class MdbFilters(BaseFilters):
    listId: Optional[str] = None
    library: Optional[str] = None


Filters = Annotated[Union[BaseFilters, PlexFilters, JellyfinFilters, TraktFilters, TmdbFilters, MdbFilters, TvdbFilters, TmdbShowFilters, EmbyFilters], Field(discriminator='filterType')]
