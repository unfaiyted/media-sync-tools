import uuid
from datetime import datetime
from typing import List, Optional

from src.clients.trakt import TraktClient
from src.create.providers.base_provider import BaseMediaProvider
from src.create.providers.managers import PosterManager
from src.create.providers.posters import TmdbPosterProvider
from src.models import TraktFilters, MediaListType, MediaList, MediaItem, MediaProviderIds, MediaType, MediaListItem


class TraktProvider(BaseMediaProvider):
    def __init__(self, config, filters: Optional[TraktFilters] = None, details: Optional[dict] = None,
                 media_list: Optional[MediaList] = None, listType: MediaListType = MediaListType.COLLECTION):
        """
        Initialize the TraktProvider.

        :param config: Configuration for the provider.
        :param filters: Optional filters to apply.
        :param details: Optional details for media list.
        :param media_list: Optional existing media list.
        :param listType: Type of media list. Default is COLLECTION.
        """
        super().__init__(config)
        self.listType = listType
        self.client: TraktClient = config.get_client('trakt')
        self.poster_manager = PosterManager(config=config)
        self.username = None
        self.details = details
        self.list_slug_or_id = None

        if filters:
            for filter_item in filters:
                if filter_item['type'] == 'username':
                    self.username = filter_item['value']
                elif filter_item['type'] in ['list_slug', 'list_id']:
                    self.list_slug_or_id = filter_item['value']

        if media_list:
            self.filters = media_list.filters
            self.username = self.filters.username
            self.list_slug_or_id = self.filters.listSlug or self.filters.listId

        self.log = config.get_logger(__name__)
        self.log.info("TraktProvider initialized", user=self.username, list_slug_or_id=self.list_slug_or_id)

    async def get_list(self) -> MediaList or None:
        """
        Retrieve MediaList from Trakt.

        :return: MediaList containing items fetched from Trakt.
        """
        if self.list_slug_or_id is None:
            self.log.error('No list id provided. Cannot get list.')
            return None

        list_items = self.client.get_list_items(username=self.username, list_id_or_slug=self.list_slug_or_id) if self.username else self.client.get_list_items_by_id(list_id=self.list_slug_or_id)

        if not self.details:
            list_info = self.client.get_list(username=self.username, list_id_or_slug=self.list_slug_or_id) if self.username else self.client.get_list_by_id(list_id=self.list_slug_or_id)

            self.details = {
                'title': list_info['name'],
                'description': list_info['description'],
                'sort_title': list_info['name'],
                'sourceListId': list_info['ids']['trakt']
            }

        media_list = MediaList(
            mediaListId=str(uuid.uuid4()),
            name=self.details['title'],
            type=self.listType,
            sourceListId=self.list_slug_or_id,
            items=[],
            description=self.details['description'],
            sortName=self.details['sort_title'],
            clientId='trakt',
            createdAt=datetime.now(),
            creatorId=self.config.get_user().userId
        )

        db = self.config.get_db()
        await db.media_lists.insert_one(media_list.dict())

        for item in list_items:
            media_item = self._map_trakt_item_to_media_item(item, self.log)
            media_list.items.append(await self.create_media_list_item(media_item, media_list, provider_list_id=item['ids']['trakt']))

        return media_list

    @staticmethod
    def _map_trakt_item_to_media_item(provider_item: dict, log) -> MediaItem:
        log.info("Mapping Trakt item to MediaItem", provider_item=provider_item)
        """
        Map a TraktItem to MediaItem object.

        :param provider_item: Item fetched from Trakt.
        :return: Mapped MediaItem object.
        """
        item = provider_item.get('show', provider_item['movie'])
        return MediaItem(
            title=item['title'],
            year=item['year'],
            type=MediaType.MOVIE if provider_item['type'] == 'movie' else MediaType.SHOW,
            providers=MediaProviderIds(
                imdbId=item['ids'].get('imdb'),
                tvdbId=item['ids'].get('tvdb'),
                traktId=item['ids'].get('trakt'),
                tmdbId=item['ids'].get('tmdb'),
                tvRageId=item['ids'].get('tvrage'),
            ))

