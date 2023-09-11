import uuid
from datetime import datetime
from typing import Optional

from src.config import ConfigManager
from src.create.providers.posters import TmdbPosterProvider
from src.models import TmdbFilters
from src.create.providers.base_provider import BaseMediaProvider
from src.models import MediaListType, MediaList, MediaItem, MediaType, MediaProviderIds, MediaListItem


class TmdbListProviderResult:
    def __init__(self, id, title, overview, release_date):
        self.id = id
        self.title = title
        self.overview = overview
        self.release_date = release_date

    def __str__(self):
        return f"ID: {self.id}, Title: {self.title}, Overview: {self.overview}, Release Date: {self.release_date}"


class TmdbProvider(BaseMediaProvider):

    def __init__(self, config: ConfigManager, filters: Optional[TmdbFilters] = None, details: Optional[dict] = None,
                 media_list: Optional[MediaList] = None, list_type: MediaListType = MediaListType.COLLECTION):
        """
        Initialize the TmdbProvider.
        :param config:
        :param filters:
        :param details:
        :param media_list:
        :param list_type:
        """
        super().__init__(config)
        self.client = config.get_client('tmdb')
        self.log = config.get_logger(__name__)
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

    @staticmethod
    def _map_tmdb_item_to_media_item(item):
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

    async def get_list(self):
        """
        Retrieve MediaList from TMDB.
        :return:
        """
        db = self.config.get_db()
        filter_query_params = self._convert_filters_to_query_params()

        movie_data = self.client.discover_movie(**filter_query_params)
        movie_results = movie_data.get("results", [])

        media_list = MediaList(
            mediaListId=str(uuid.uuid4()),
            name=self.media_list.name,
            type=self.list_type,
            description=self.media_list.description,
            sortName=self.media_list.sortName,
            filters=self.media_list.filters,
            clientId='tmdb',
            createdAt=datetime.now(),
            creatorId=self.config.get_user().userId
        )

        await db.media_lists.insert_one(media_list.dict())

        media_list.items = []

        for item in movie_results:
            self.log.debug("Creating media item", item=item, media_list=media_list)
            media_item = self._map_tmdb_item_to_media_item(item)
            media_list.items.append(
                await self.create_media_list_item(media_item, media_list, TmdbPosterProvider(config=self.config)))

        return media_list

