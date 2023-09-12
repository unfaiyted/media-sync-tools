import uuid
from datetime import datetime
from typing import List, Optional

from src.models.providers.trakt import TraktItem
from src.models import MediaItem
from src.clients.trakt import TraktClient
from src.create.providers.base_provider import BaseMediaProvider
from src.create.providers.managers import PosterProviderManager
from src.create.providers.posters import TmdbPosterProvider
from src.models import TraktFilters, MediaListType, MediaList, MediaItem, MediaProviderIds, MediaType, MediaListItem


class TraktProvider(BaseMediaProvider):
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
            media_item = self._map_trakt_item_to_media_item(item, self.log)
            media_list.items.append(
                await self.create_media_list_item(media_item, media_list, TmdbPosterProvider(config=self.config)))

        return media_list

    @staticmethod
    def _map_trakt_item_to_media_item(trakt_item: TraktItem, log) -> MediaItem | None:
        """
        Map a TraktItem to MediaItem object.

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
