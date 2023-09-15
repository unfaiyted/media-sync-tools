from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import List, ForwardRef, Optional, Union

from pydantic import BaseModel, validator

from src.models.providers.mdb import MdbItem
from src.models.providers.trakt import TraktMovie, TraktShow, TraktItem
from src.models.providers.jellyfin import JellyfinItemType

from src.models import Filters, FilterType, TraktFilters, PlexFilters, JellyfinFilters, \
    TmdbFilters, EmbyFilters, MdbFilters


class MediaType(str, Enum):
    MOVIE = "MOVIE"
    EPISODE = "EPISODE"
    UNKNOWN = "UNKNOWN"
    SEASON = "SEASON"
    SHOW = "SHOW"
    CO
    # ... other types ...


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
            return MediaListType.PLAYLIST
        elif list_type == JellyfinItemType.SERIES:


        pass


class MediaListOptions(BaseModel):
    mediaListOptionsId: str
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
    mediaListId: str = None
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
    def from_emby(cls, emby_list: dict, log) -> MediaList:
        """
        Map an Emby list to a MediaList.
        :param emby_list:
        :param log:
        :return:
        """
        log.info("Mapping Emby list to MediaList", emby_list=emby_list)
        return MediaList(
            mediaListId=str(uuid.uuid4()),
            name=emby_list['Name'],
            type=MediaListType.COLLECTION if emby_list['Type'] == 'Collection' else MediaListType.PLAYLIST,
            sourceListId=emby_list['Id'],
            filters=EmbyFilters(
                clientId=emby_list['CollectionType'],
                library=emby_list['Name']).dict(),
            sortName=emby_list['SortName'],
            clientId='emby',
            createdAt=datetime.now(),
            creatorId='emby'
        )

    @classmethod
    def from_jellyfin(cls, jellyfin_list: dict, log) -> MediaList:
        """
        Map a Jellyfin list to a MediaList.
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
            filters=JellyfinFilters(
                clientId=jellyfin_list['CollectionType'],
                library=jellyfin_list['Name']).dict(),
            sortName=jellyfin_list['SortName'],
            clientId='jellyfin',
            createdAt=datetime.now(),
            creatorId='jellyfin'
        )

    @classmethod
    def from_plex(cls, plex_list, log) -> MediaList:
        """
        Map a Plex list to a MediaList.
        :param plex_list:
        :param log:
        :return:
        """
        log.info("Mapping Plex list to MediaList", plex_list=plex_list)
        return MediaList(
            mediaListId=str(uuid.uuid4()),
            name=plex_list.title,
            type=MediaListType.COLLECTION if plex_list.TYPE == 'collection' else MediaListType.PLAYLIST,
            sourceListId=plex_list.ratingKey,
            filters=PlexFilters(
                clientId=plex_list.TYPE,
                library=plex_list.title).dict(),
            sortName=plex_list.title,
            clientId='plex',
            createdAt=datetime.now(),
            creatorId='plex'
        )

    @classmethod
    def from_trakt(cls, trakt_list: dict, log) -> MediaList:
        """
        Map a Trakt list to a MediaList.
        :param trakt_list:
        :param log:
        :return:
        """
        log.info("Mapping Trakt list to MediaList", trakt_list=trakt_list)
        return MediaList(
            mediaListId=str(uuid.uuid4()),
            name=trakt_list['name'],
            type=MediaListType.COLLECTION if trakt_list['list_type'] == 'official' else MediaListType.PLAYLIST,
            sourceListId=trakt_list['ids']['trakt'],
            filters=TraktFilters(
                clientId=trakt_list['list_type'],
                library=trakt_list['name']).dict(),
            sortName=trakt_list['name'],
            clientId='trakt',
            createdAt=datetime.now(),
            creatorId='trakt'
        )

    @classmethod
    def from_tmdb(cls, tmdb_list: dict, log) -> MediaList:
        """
        Map a TMDB list to a MediaList.
        :param tmdb_list:
        :param log:
        :return:
        """
        log.info("Mapping TMDB list to MediaList", tmdb_list=tmdb_list)
        return MediaList(
            mediaListId=str(uuid.uuid4()),
            name=tmdb_list['name'],
            type=MediaListType.COLLECTION if tmdb_list['list_type'] == 'official' else MediaListType.PLAYLIST,
            sourceListId=tmdb_list['id'],
            filters=TmdbFilters(
                clientId=tmdb_list['list_type'],
                library=tmdb_list['name']).dict(),
            sortName=tmdb_list['name'],
            clientId='tmdb',
            createdAt=datetime.now(),
            creatorId='tmdb'
        )

    @classmethod
    def from_mdb(cls, mdb_list: dict, log) -> MediaList:
        """
        Map a MDB list to a MediaList.
        :param mdb_list:
        :param log:
        :return:
        """
        log.info("Mapping MDB list to MediaList", mdb_list=mdb_list)
        return MediaList(
            mediaListId=str(uuid.uuid4()),
            name=mdb_list['name'],
            type=MediaListType.COLLECTION if mdb_list['list_type'] == 'official' else MediaListType.PLAYLIST,
            sourceListId=mdb_list['id'],
            filters=MdbFilters(
                clientId=mdb_list['list_type'],
                library=mdb_list['name']).dict(),
            sortName=mdb_list['name'],
            clientId='mdb',
            createdAt=datetime.now(),
            creatorId='mdb'
        )


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
    mediaItemId: str = None
    title: str
    year: Optional[str]
    type: MediaType
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

    @staticmethod
    def from_emby(provider_item: dict, log) -> MediaItem:
        """
        Map an Emby item to a MediaItem.
        :param provider_item:
        :param log:
        :return:
        """
        log.info(f"Mapping Emby item to MediaItem", provider_item=provider_item)
        return MediaItem(
            mediaItemId=str(uuid.uuid4()),
            title=provider_item.get('Name', 'TITLE MISSING'),
            year=provider_item.get('ProductionYear', None),
            description=provider_item.get('Overview', None),
            type=MediaType.MOVIE if provider_item['Type'] == 'Movie' else MediaType.SHOW,
            providers=MediaProviderIds(
                imdbId=provider_item['ProviderIds'].get('IMDB', None),
                tvdbId=provider_item['ProviderIds'].get('Tvdb', None)
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
            type=MediaType.MOVIE if provider_item['Type'] == 'Movie' else MediaType.SHOW,
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
            mediaItemId=str(uuid.uuid4()),
            title=item.title,
            year=item.year,
            type=MediaType.MOVIE if item.TYPE == 'movie' else MediaType.SHOW,
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
            mediaItemId=str(uuid.uuid4()),
            title=item.title,
            year=item.release_year,
            type=MediaType.MOVIE if item.mediatype == 'movie' else MediaType.SHOW,
            providers=MediaProviderIds(
                imdbId=item.imdb_id,
                tvdbId=item.tvdb_id,
            ),
        )

    @staticmethod
    def from_tmdb(item, log):
        """
        Map a TMDB item to a MediaItem.
        :param item:
        :return:
        """
        return MediaItem(
            mediaItemId=str(uuid.uuid4()),
            title=item['title'],
            year=item['release_date'].split('-')[0],
            description=item['overview'],
            releaseDate=item['release_date'],
            type=MediaType.MOVIE,
            providers=MediaProviderIds(
                tmdbId=item['id'],
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
            mediaItemId=str(uuid.uuid4()),
            title=item.title,
            year=item.year,
            type=MediaType.MOVIE if trakt_item.type == 'movie' else MediaType.SHOW,
            providers=MediaProviderIds(
                imdbId=item.ids.imdb,
                tvdbId=item.ids.tvdb,
                traktId=item.ids.trakt,
                tmdbId=item.ids.tmdb,
                tvRageId=item.ids.tvrage,
            ))


class MediaListItem(BaseModel):
    mediaListItemId: str = None
    mediaListId: str
    mediaItemId: str
    poster: Optional[str]
    mediaPosterId: Optional[str]
    item: Optional[ForwardRef('MediaItem')]
    dateAdded: Optional[datetime]
