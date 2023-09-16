from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import List, ForwardRef, Optional

from pydantic import BaseModel, validator, Field

from src.models.providers.tmdb import TmdbList, TmdbMovieDetails
from src.models import Filters, FilterType, TraktFilters, PlexFilters, JellyfinFilters, \
    TmdbFilters, EmbyFilters, MdbFilters
from src.models.providers.jellyfin import JellyfinItemType
from src.models.providers.mdb import MdbItem
from src.models.providers.trakt import TraktMovie, TraktShow, TraktItem


class MediaItemType(str, Enum):
    MOVIE = "MOVIE"
    EPISODE = "EPISODE"
    UNKNOWN = "UNKNOWN"
    # sublists
    SEASON = "SEASON"
    SHOW = "SHOW"
    LIST = "LIST"

    # ... other types ...

    @classmethod
    def is_list(cls, item_type: MediaItemType):
        return (item_type == MediaItemType.LIST or
                item_type == MediaItemType.SHOW or
                item_type == MediaItemType.SEASON)

    @classmethod
    def from_plex(cls, TYPE):
        pass

    @classmethod
    def from_emby(cls, emby_type):
        if emby_type == 'Movie':
            return MediaItemType.MOVIE
        elif emby_type == 'BoxSet':
            return MediaItemType.LIST
        elif emby_type == 'Season':
            return MediaItemType.SEASON
        elif emby_type == 'Series':
            return MediaItemType.SHOW
        elif emby_type == 'Episode':
            return MediaItemType.EPISODE
        else:
            print('unknown emby type', emby_type)
            return MediaItemType.UNKNOWN

    @classmethod
    def from_trakt(cls, type):
        pass


class MediaListType(str, Enum):
    COLLECTION = "COLLECTION"
    PLAYLIST = "PLAYLIST"
    LIBRARY = "LIBRARY"

    # ... other types ...

    @classmethod
    def from_jellyfin(cls, list_type):

        if list_type == JellyfinItemType.BOX_SET:
            return MediaListType.COLLECTION
        elif list_type == JellyfinItemType.SEASON:
            return MediaListType.LIBRARY
        elif list_type == JellyfinItemType.SERIES:
            return MediaListType.LIBRARY

    @classmethod
    def from_plex(cls, TYPE):
        pass

    @classmethod
    def from_emby(cls, param):
        pass

    @classmethod
    def from_trakt(cls, param):
        pass

    @classmethod
    def from_tmdb(cls, param):
        pass

    @classmethod
    def from_mdb(cls, param):
        pass


class MediaListOptions(BaseModel):
    mediaListOptionsId: str = Field(default_factory=uuid.uuid4)
    userId: str
    type: MediaListType
    clients: List[ForwardRef('ConfigClient')]
    mediaListId: str
    syncLibraryId: str
    sync: bool
    updateImages: bool
    deleteExisting: bool


class MediaList(BaseModel):
    sourceListId: Optional[str]
    mediaListId: str = Field(default_factory=uuid.uuid4)
    clientId: str  # client provider
    creatorId: str
    sourceListId: Optional[str]
    name: str
    poster: Optional[str]
    mediaPosterId: Optional[str]
    type: MediaListType
    sortName: str
    description: Optional[str] = None
    filters: Optional[Filters]
    items: Optional[List[ForwardRef('MediaListItem')]]
    createdAt: datetime
    creator: Optional[ForwardRef('User')]

    @validator('filters', pre=True, always=True)
    # Filters were picking the wrong time on serialization
    def set_correct_filter_type(cls, filters):
        if filters is None:
            return None

        filter_type = filters['filterType']

        if filter_type == FilterType.TRAKT:
            return TraktFilters(**filters)
        elif filter_type == FilterType.PLEX:
            return PlexFilters(**filters)
        elif filter_type == FilterType.JELLYFIN:
            return JellyfinFilters(**filters)
        elif filter_type == FilterType.TMDB:
            return TmdbFilters(**filters)
        elif filter_type == FilterType.EMBY:
            return EmbyFilters(**filters)
        elif filter_type == FilterType.MDB:
            return MdbFilters(**filters)

        raise ValueError(f"Unknown filter type: {filter_type}")

    @classmethod
    def from_emby(cls, log, emby_list: dict, client_id: str, creator_id: str, filters: EmbyFilters = None) -> MediaList:
        """
        Map an Emby list to a MediaList.
        :param client_id:
        :param filters:
        :param creator_id:
        :param emby_list:
        :param log:
        :return:
        """
        log.info("Mapping Emby list to MediaList", emby_list=emby_list)
        return MediaList(
            mediaListId=str(uuid.uuid4()),
            name=emby_list['Name'],
            type=MediaListType.from_emby(['Type']),  # == 'Collection' else MediaListType.PLAYLIST,
            sourceListId=emby_list['Id'],
            filters=filters.dict(),
            sortName=emby_list['SortName'],
            clientId=client_id,
            createdAt=datetime.now(),
            creatorId=creator_id
        )

    @classmethod
    def from_jellyfin(cls, log, jellyfin_list: dict, client_id: str, creator_id: str,
                      filters: JellyfinFilters = None) -> MediaList:
        """
        Map a Jellyfin list to a MediaList.
        :param client_id:
        :param filters:
        :param creator_id:
        :param jellyfin_list:
        :param log:
        :return:
        """
        log.info("Mapping Jellyfin list to MediaList", jellyfin_list=jellyfin_list)
        return MediaList(
            mediaListId=str(uuid.uuid4()),
            name=jellyfin_list['Name'],
            type=MediaListType.from_jellyfin(jellyfin_list['Type']),
            # type=MediaListType.COLLECTION if jellyfin_list['Type'] == 'Collection' else MediaListType.PLAYLIST,
            sourceListId=jellyfin_list['Id'],
            filters=filters.dict(),
            sortName=jellyfin_list['SortName'],
            clientId=client_id,
            createdAt=datetime.now(),
            creatorId=creator_id
        )

    @classmethod
    def from_plex(cls, log, plex_list, creator_id, client_id: str, filters: PlexFilters = None) -> MediaList:
        """
        Map a Plex list to a MediaList.
        :param client_id:
        :param filters:
        :param creator_id:
        :param plex_list:
        :param log:
        :return:
        """
        log.info("Mapping Plex list to MediaList", plex_list=plex_list)
        return MediaList(
            mediaListId=str(uuid.uuid4()),
            name=plex_list.title,
            type=MediaListType.from_plex(plex_list.TYPE),
            description=plex_list.summary,
            sourceListId=plex_list.ratingKey,
            filters=filters.dict(),
            sortName=plex_list.titleStort,
            clientId=client_id,
            createdAt=datetime.now(),
            creatorId=creator_id
        )

    @classmethod
    def from_trakt(cls, log, trakt_list: dict, client_id: str, creator_id, filters: TraktFilters = None) -> MediaList:
        """
        Map a Trakt list to a MediaList.
        :param client_id:
        :param filters:
        :param creator_id:
        :param trakt_list:
        :param log:
        :return:
        """
        log.info("Mapping Trakt list to MediaList", trakt_list=trakt_list)
        return MediaList(
            mediaListId=str(uuid.uuid4()),
            name=trakt_list['name'],
            type=MediaListType.from_trakt(trakt_list['list_type']),
            sourceListId=trakt_list['ids']['trakt'],
            description=trakt_list['description'],
            filters=filters.dict(),
            sortName=trakt_list['name'],
            clientId=client_id,
            createdAt=datetime.now(),
            creatorId=creator_id
        )

    @classmethod
    def from_tmdb(cls, log, tmdb_list: TmdbList, client_id: str, creator_id: str, filters: TmdbFilters = None) -> MediaList:
        """
        Map a TMDB list to a MediaList.
        :param client_id:
        :param filters:
        :param creator_id:
        :param tmdb_list:
        :param log:
        :return:
        """
        log.info("Mapping TMDB list to MediaList", tmdb_list=tmdb_list)
        return MediaList(
            mediaListId=str(uuid.uuid4()),
            name=tmdb_list.name,
            type=MediaListType.COLLECTION,
            sourceListId=tmdb_list.id,
            filters=filters.dict(),
            sortName=tmdb_list.name,
            clientId=client_id,
            createdAt=datetime.now(),
            creatorId=creator_id
        )

    @classmethod
    def from_mdb(cls, log, mdb_list: dict, client_id: str, creator_id: str, filters: MdbFilters) -> MediaList:
        """
        Map an MDB list to a MediaList.
        :param client_id:
        :param filters:
        :param creator_id:
        :param mdb_list:
        :param log:
        :return:
        """
        log.info("Mapping MDB list to MediaList", creator_id, mdb_list=mdb_list)
        return MediaList(
            mediaListId=str(uuid.uuid4()),
            name=mdb_list['name'],
            type=MediaListType.from_mdb(mdb_list['list_type']),  # official?
            sourceListId=mdb_list['id'],
            filters=filters.dict(),
            sortName=mdb_list['name'],
            clientId=client_id,
            createdAt=datetime.now(),
            creatorId=creator_id
        )

    @classmethod
    def merge_media_lists(cls, media_lists: List[MediaList]) -> MediaList | None:
        """
        Merge multiple MediaLists into one.
        :param media_lists:
        :return:
        """
        if len(media_lists) == 0:
            return None

        merged_media_list = media_lists[0]
        merged_media_list.items = []

        for media_list in media_lists:
            merged_media_list.items.extend(media_list.items)

        return merged_media_list

    @classmethod
    def update_details(cls, media_list: MediaList, details: dict) -> MediaList:
        """
        Update details of a MediaList.
        :param media_list:
        :param details:
        :return:
        """
        media_list.name = details.get('name', media_list.name)
        media_list.description = details.get('description', media_list.description)
        media_list.sortName = details.get('sortName', media_list.sortName)
        media_list.poster = details.get('poster', media_list.poster)
        media_list.mediaPosterId = details.get('mediaPosterId', media_list.mediaPosterId)
        media_list.filters = details.get('filters', media_list.filters)

        return media_list


class MediaProviderIds(BaseModel):
    imdbId: Optional[str]
    tvdbId: Optional[str]
    tmdbId: Optional[str]
    traktId: Optional[str]
    tvRageId: Optional[str]
    rottenTomatoesId: Optional[str]
    aniListId: Optional[str]


class MediaItemRatings(BaseModel):
    tmdb: Optional[float]
    imdb: Optional[float]
    trakt: Optional[float]
    metacritic: Optional[float]
    rottenTomatoes: Optional[float]
    tvdb: Optional[float]
    aniList: Optional[float]


class MediaItem(BaseModel):
    mediaItemId: str = Field(default_factory=uuid.uuid4)
    title: str
    year: Optional[str]
    type: MediaItemType
    sortTitle: Optional[str]
    originalTitle: Optional[str]
    tagline: Optional[str]
    poster: Optional[str]
    description: Optional[str]
    parentalRating: Optional[str]
    genres: Optional[List[str]]
    releaseDate: Optional[str]
    dateAdded: Optional[datetime]
    providers: Optional[MediaProviderIds]
    ratings: Optional[MediaItemRatings]
    importId: Optional[str]

    @staticmethod
    def from_provider_type(provider: str, item, log) -> MediaItem:
        """
        Map an item from a provider to a MediaItem.
        :param provider:
        :param item:
        :param log:
        :return:
        """
        if provider == 'jellyfin':
            return MediaItem.from_jellyfin(item, log)
        elif provider == 'plex':
            return MediaItem.from_plex(item, log)
        elif provider == 'trakt':
            return MediaItem.from_trakt(item, log)
        elif provider == 'tmdb':
            return MediaItem.from_tmdb(item, log)
        elif provider == 'emby':
            return MediaItem.from_emby(item, log)
        elif provider == 'mdb':
            return MediaItem.from_mdb(item, log)

        raise ValueError(f"Unknown provider: {provider}")

    @staticmethod
    def from_emby(provider_item, log) -> MediaItem:
        """
        Map an Emby item to a MediaItem.
        :param provider_item:
        :param log:
        :return:
        """
        log.info(f"Mapping Emby item to MediaItem", provider_item=provider_item)
        return MediaItem(
            mediaItemId=str(uuid.uuid4()),
            title=provider_item.Name,
            year=provider_item.ProductionYear,
            description='',
            type=MediaItemType.from_emby(provider_item.Type),
            providers=MediaProviderIds(
                imdbId=provider_item.ProviderIds.IMDB,
                tvdbId=provider_item.ProviderIds.Tvdb
            )
        )

    @staticmethod
    def from_jellyfin(provider_item: dict, log) -> MediaItem:
        """
        Map a Jellyfin item to a MediaItem.
        :param provider_item:
        :param log:
        :return:
        """
        log.info(f"Mapping Jellyfin item to MediaItem", provider_item=provider_item)
        return MediaItem(
            mediaItemId=str(uuid.uuid4()),
            title=provider_item.get('Name', 'TITLE MISSING'),
            year=provider_item.get('ProductionYear', None),
            description=provider_item.get('Overview', None),
            type=MediaItemType.MOVIE if provider_item['Type'] == 'Movie' else MediaItemType.SHOW,
            providers=MediaProviderIds(
                imdbId=provider_item['ProviderIds'].get('IMDB', None),
                tvdbId=provider_item['ProviderIds'].get('Tvdb', None)
            ),
        )

    @staticmethod
    def extract_external_ids(plex_item):
        ids = {}

        if not plex_item.guid:
            return ids

            # Check for IMDb
        if "imdb://" in plex_item.guid:
            ids['imdb'] = plex_item.guid.split('imdb://')[1].split('?')[0]

            # Check for TheMovieDB
        if "themoviedb://" in plex_item.guid:
            ids['tmdb'] = plex_item.guid.split('themoviedb://')[1].split('?')[0]

            # You can continue adding checks for other ID types in a similar manner...
            # Check for TVDB
        if "thetvdb://" in plex_item.guid:
            ids['tvdb'] = plex_item.guid.split('thetvdb://')[1].split('?')[0]

        return ids

    @staticmethod
    def from_plex(item: TraktMovie or TraktShow, log) -> MediaItem:
        """
        Map a Plex item to a MediaItem.
        :param log:
        :param item:
        :return:
        """
        log.debug("Mapping Plex item to MediaItem", item=item)
        external_ids = MediaItem.extract_external_ids(item)

        media_item = MediaItem(
            title=item.title,
            year=item.year,
            type=MediaItemType.from_plex(item.TYPE),
            providers=MediaProviderIds(
                imdbId=external_ids.get('imdb', None),
                tvdbId=external_ids.get('tvdb', None),
                tmdbId=external_ids.get('tmdb', None),
            ),
        )

        return media_item

    @staticmethod
    def from_mdb(item: MdbItem, log) -> MediaItem:
        return MediaItem(
            title=item.title,
            year=item.release_year,
            type=MediaItemType.MOVIE if item.mediatype == 'movie' else MediaItemType.SHOW,
            providers=MediaProviderIds(
                imdbId=item.imdb_id,
                tvdbId=item.tvdb_id,
            ),
        )

    @staticmethod
    def from_tmdb(item: TmdbMovieDetails, log):
        """
        Map a TMDB item to a MediaItem.
        :param item:
        :return:
        """
        return MediaItem(
            title=item.title,
            year=item.release_date.split('-')[0],
            description=item.overview,
            releaseDate=item.release_date,
            type=MediaItemType.MOVIE,
            providers=MediaProviderIds(
                tmdbId=item.id,
            ),
        )

    @staticmethod
    def from_trakt(trakt_item: TraktItem, log) -> MediaItem | None:
        """
        Map a TraktItem to MediaItem object.

        :param log:
        :param trakt_item: Item fetched from Trakt.
        :return: Mapped MediaItem object.
        """
        log.info("Mapping TraktItem to MediaItem", provider_item=trakt_item)
        item_type = trakt_item.type
        log.debug("Mapped item", item=trakt_item, item_type=item_type)

        if trakt_item is None:
            log.error("Error processing item", item=trakt_item)
            return None

        item = trakt_item.get_item()

        return MediaItem(
            title=item.title,
            year=item.year,
            type=MediaItemType.from_trakt(trakt_item.type),
            providers=MediaProviderIds(
                imdbId=item.ids.imdb,
                tvdbId=item.ids.tvdb,
                traktId=item.ids.trakt,
                tmdbId=item.ids.tmdb,
                tvRageId=item.ids.tvrage,
            ))


class MediaListItemType(str, Enum):
    LIST = "LIST"
    ITEM = "ITEM"



class MediaListItem(BaseModel):
    mediaListItemId: str = Field(default_factory=uuid.uuid4)
    type: MediaListItemType
    mediaListId: str
    mediaItemId: str
    poster: Optional[str]
    mediaPosterId: Optional[str]
    item: Optional[ForwardRef('MediaItem') or ForwardRef('MediaList')]
    dateAdded: Optional[datetime]
