import uuid
from abc import ABC
from datetime import datetime
from typing import List, Optional

from src.create.providers.list import ListProvider
from src.models.providers.trakt import TraktItem
from src.clients.trakt import TraktClient
from src.create.providers.poster.manager import PosterProviderManager
from src.create.providers.poster.tmdb import TmdbPosterProvider
from src.models import TraktFilters, MediaListType, MediaList, MediaItem, MediaProviderIds, MediaType, MediaListItem


class TraktListProvider(ListProvider, ABC):
    def __init__(self, config, filters: Optional[TraktFilters] = None, details: Optional[dict] = None,
                 media_list: Optional[MediaList] = None, list_type: MediaListType = MediaListType.COLLECTION):
        """
        Initialize the TraktProvider.

        :param config: Configuration for the provider.
        :param filters: Optional filters to apply.
        :param details: Optional details for media list.
        :param media_list: Optional existing MediaList.
        :param list_type: Type of media list. Default is COLLECTION.
        """
        super().__init__(config)
        self.log = config.get_logger(__name__)
        self.list_type = list_type
        self.client: TraktClient = config.get_client('trakt')
        self.poster_manager = PosterProviderManager(config=config)
        self.username = None
        self.details = details
        self.list_slug_or_id = None
        self.filters = filters

        if media_list and not filters:
            self.log.debug("Using existing MediaList", media_list=media_list)
            self.filters = media_list.filters

        if self.filters is not None:
            if isinstance(self.filters, TraktFilters):
                self.log.debug("Using TraktFilters", filters=filters)
                self.username = self.filters.username
                self.list_slug_or_id = self.filters.listSlug or self.filters.listId
            else:
                self.log.warn("Invalid filters provided", filters=filters)

        self.log.info("TraktProvider initialized", user=self.username, list_slug_or_id=self.list_slug_or_id)

    async def get_list(self) -> MediaList or None:
        """
        Retrieve MediaList from Trakt.

        :return: MediaList containing items fetched from Trakt.
        """
        if self.list_slug_or_id is None:
            self.log.error('No list id provided. Cannot get list.')
            return None

        list_items = self.client.get_list_items(username=self.username,
                                                list_id_or_slug=self.list_slug_or_id) if self.username else self.client.get_list_items_by_id(
            list_id=self.list_slug_or_id)

        if not self.details:
            list_info = self.client.get_list(username=self.username,
                                             list_id_or_slug=self.list_slug_or_id) if self.username else self.client.get_list_by_id(
                list_id=self.list_slug_or_id)

            self.details = {
                'title': list_info['name'],
                'description': list_info['description'],
                'sort_title': list_info['name'],
                'sourceListId': list_info['ids']['trakt']
            }

        media_list = MediaList(
            mediaListId=str(uuid.uuid4()),

            name=self.details['title'],
            type=self.list_type,
            sourceListId=self.list_slug_or_id,
            items=[],
            description=self.details['description'],
            sortName=self.details['sort_title'],
            filters=self.filters.dict(),
            clientId='trakt',
            createdAt=datetime.now(),
            creatorId=self.config.get_user().userId
        )

        db = self.config.get_db()
        self.log.debug('Filters',  filters=self.filters)
        self.log.debug('MediaList', media_list=media_list)
        await db.media_lists.insert_one(media_list.dict())

        for item in list_items:
            self.log.debug("Appending media item", item=item)
            item = TraktItem(**item)
            self.log.debug("TraktItem to be mapped", item=item)
            media_item = MediaItem.from_trakt(item, self.log)
            self.log.debug("MediaItem after mapping", media_item=media_item)
            media_list.items.append(
                await self.create_media_list_item(media_item, media_list, TmdbPosterProvider(config=self.config)))

        return media_list


