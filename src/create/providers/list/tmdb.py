import uuid
from abc import ABC
from datetime import datetime
from typing import Optional

from src.models.providers.tmdb import TmdbList, TmdbSearchResult, TmdbMovieDetails
from src.create.providers.list import ListProvider
from src.config import ConfigManager
from src.create.providers.poster.tmdb import TmdbPosterProvider, PosterProvider
from src.models import TmdbFilters, Provider
from src.models import MediaListType, MediaList, MediaItem


class TmdbListProvider(ListProvider, PosterProvider, ABC):

    def __init__(self, config: ConfigManager, filters: Optional[TmdbFilters] = None, details: Optional[dict] = None,
                 media_list: Optional[MediaList] = None, list_type: MediaListType = MediaListType.COLLECTION,
                 client_id='tmdb'):
        """
        Initialize the TmdbProvider.
        :param config:
        :param filters:
        :param details:
        :param media_list:
        :param list_type:
        """
        super().__init__(config)
        self.client = config.get_client(client_id)
        self.client_id = client_id
        self.name = Provider.TMDB
        self.creator_id = config.get_user().userId
        self.log = config.get_logger(__name__)
        self.db = config.get_db()
        self.details = details
        self.filters = filters
        self.list_type = list_type

        if media_list:
            self.media_list = media_list
            self.log.debug("Using existing MediaList", media_list=media_list)
            self.filters = media_list.filters

        if filters is not None:
            self.log.debug("Using filters", filters=filters)
            self.id = filters.listId

    def _convert_filters_to_query_params(self):
        self.log.debug("Converting filters to query params", filters=self.filters)
        return {filter_item['type']: filter_item['value'] for filter_item in self.filters}

    async def get_media_list_with_items_by_id(self):
        """
        Retrieve MediaList from TMDB by ID.
        :return:
        """
        if self.filters.listId is None:
            self.log.error("No filter provided. Cannot get list by id")

        self.log.info("Getting TMDB list by id", list_id=self.filters.listId)
        provider_list = self.fetch_provider_list_with_items_by_id()
        return MediaList.from_tmdb(self.log, tmdb_list=provider_list,
                                   client_id=self.client_id,
                                   creator_id=self.creator_id,
                                   filters=self.filters), provider_list.results

    def get_media_list_by_filter(self):
        """
        Retrieve MediaList from TMDB by filter.
        :return:
        """
        if self.filters is None:
            self.log.error("No filter provided. Cannot get list by filter")

        self.log.info("Getting TMDB list by filter", filters=self.filters)
        return self.media_list

    def fetch_provider_list_with_items_by_id(self):
        """
        Retrieve MediaList from TMDB by ID.
        :return:
        """
        if self.filters.listId is None:
            self.log.error("No filter provided. Cannot get list by id")

        self.log.info("Getting TMDB list by id", list_id=self.filters.listId)
        provider_list = self.client.get_list_by_id(self.filters.listId)
        return TmdbList(**provider_list)

    def fetch_provider_items_by_filter(self):
        """
        Retrieve MediaList from TMDB by filter.
        :return:
        """
        if self.filters is None:
            self.log.error("No filter provided. Cannot get list by filter")

        self.log.info("Getting TMDB list by filter", filters=self.filters)
        filter_query_params = self.filters.to_query_params()
        movie_data = self.client.discover_movie(**filter_query_params)
        self.log.debug('Found movies', movie_data=movie_data)
        return TmdbSearchResult(**movie_data).results

    def search_list_by_id(self):
        """
        Search for a MediaList by ID.
        :return:
        """
        if self.filters.listId is None:
            self.log.error("No filter provided. Cannot search list by id")

        self.log.info("Searching TMDB list by id", list_id=self.filters.listId)
        provider_list = self.client.get_list_by_id(self.filters.listId)
        return TmdbList(**provider_list)

    async def get_list(self):
        """
        Retrieve MediaList from TMDB.
        :return:
        """
        media_list = None
        provider_items: list[TmdbMovieDetails] | None = None

        if self.filters.listId is not None:
            self.log.debug("Getting list by id", list_id=self.filters.listId)
            media_list, provider_items = await self.get_media_list_with_items_by_id()
        elif self.filters is not None:
            self.log.debug("Getting list by filter", filters=self.filters)
            media_list = self.get_media_list_by_filter()
            provider_items = self.fetch_provider_items_by_filter()

        if media_list is None:
            self.log.error("Error creating or no list found", media_list=media_list)
            return None

        self.log.debug("Inserting MediaList in database", media_list=media_list)
        await self.db.media_lists.insert_one(media_list.dict())

        return await self.add_items_to_media_list(media_list, 'tmdb', provider_items,
                                                  TmdbPosterProvider(config=self.config))
