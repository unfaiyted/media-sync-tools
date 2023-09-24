# Let's call this media_provider.py
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from src.models import MediaItemType, ProviderType
from src.models import MediaListItemType
from src.create.providers.poster.tmdb import TmdbPosterProvider, PosterProvider
from src.models import MediaItem, MediaProviderIds, MediaList, MediaListItem

# This is the base media provider. It's an abstract class, so it can't be instantiated.
class MediaProvider(ABC):  # ABC means it's an abstract base class
    def __init__(self, config, client_id: str):
        """
        Initialize the BaseMediaProvider.
        This is responsible for fetching items from a provider and creating MediaListItems/MediaItems.
        :param config:
        """
        self.config = config
        self.client_id = client_id
        self.type = ProviderType.BASE
        self.db = self.config.get_db()
        # self.poster_manager = PosterProviderManager(config=config)
        self.log = config.get_logger(__name__)

    @abstractmethod
    def get_client(self):
        """
        Retrieve client for provider.
        :return:
        """
        pass

    async def get_existing_media_item(self, media_item: MediaItem) -> Optional[MediaItem]:
        """
        Get an existing media item from the database.
        :param media_item:
        :return:
        """
        if media_item.providers is None:
            self.log.debug('No providers found for media item', media_item=media_item.dict())
            return None

        if media_item.type == MediaItemType.LIST:
            self.log.debug('Media item is a list. Skipping.')
            return None

        if media_item.providers:
            for field in MediaProviderIds.__fields__:
                self.log.debug('Checking for existing media item by provider ID', field=field)
                if provider_id := getattr(media_item.providers, field, None):
                    self.log.debug('Checking for existing media item by provider ID', field=field,
                                   provider_id=provider_id)
                    existing_media_item = await self.db.media_items.find_one(
                        {f"providers.{field}": provider_id}
                    )
                    if existing_media_item:
                        return MediaItem.parse_obj(existing_media_item)

        # If not found by provider ID, check by title and year
        if media_item.title and media_item.year:
            self.log.info('No existing media item found by provider ID. Checking by title and year.',
                          media_item=media_item.dict())
            existing_item = await self.db.media_items.find_one({"title": media_item.title, "year": media_item.year})
            if existing_item:
                return MediaItem.parse_obj(existing_item)

        self.log.info('No existing media item found', media_item=media_item.dict())
        return None

    @staticmethod
    async def merge_media_items(media_item: MediaItem, existing_media_item: MediaItem) -> MediaItem:
        """
        Merge two MediaItems together.
        :param media_item:
        :param existing_media_item:
        :return:
        """
        for field in MediaItem.__fields__:
            if field == 'mediaItemId':
                continue
            existing_value = getattr(existing_media_item, field, None)
            if existing_value is None:
                setattr(existing_media_item, field, getattr(media_item, field))
        return existing_media_item

    async def merge_and_update_media_item(self, media_item: MediaItem, existing_media_item: MediaItem) -> MediaItem:
        """
        Merge two MediaItems together and update the existing item in the database.
        :param media_item:
        :param existing_media_item:
        :return:
        """
        db = self.config.get_db()
        merged_media_item = await self.merge_media_items(media_item, existing_media_item)
        db.media_items.update_one(
            {"mediaItemId": existing_media_item.mediaItemId},
            {"$set": merged_media_item.dict()}
        )
        self.log.info('Merged media item saved.', media_item=merged_media_item.dict())
        return merged_media_item

    async def create_media_list_item(self, media_item: MediaItem, media_list: MediaList) -> MediaListItem:
        """
        Create a MediaListItem from a provider item.

        :param media_item: Item fetched from provider.
        :param media_list: The MediaList item belongs to.
        :return: MediaItem object.
        """
        # if preferred_poster_provider is None:
        #     self.log.debug('No preferred poster provider provided. Using TMDb.')
        #     preferred_poster_provider = TmdbPosterProvider(config=self.config)

        self.log.info('Creating MediaListItem from MediaItem', media_item=media_item)

        if existing_media_item := await self.get_existing_media_item(media_item):
            self.log.debug("Found existing media_item", media_item=existing_media_item)
            media_item = await self.merge_and_update_media_item(media_item, existing_media_item)

        media_list_item = MediaListItem(
            type=MediaListItemType.ITEM,
            mediaItemId=media_item.mediaItemId,
            mediaListId=media_list.mediaListId,
            dateAdded=datetime.now(),
        )

        if media_item.type == MediaItemType.LIST:
            self.log.debug('Media item is a list. Adding list to item.')
            # media_list_item.item = self.list_manager.get_list_by_id(self.client_id, media_item.importId)

        # if media_item.poster is None:
        # self.log.info('Fetching poster for MediaItem', media_item=media_item)
        # media_item.poster = await self.poster_manager.get_poster(preferred_provider=preferred_poster_provider,
        #                                                          media_item=media_item)
        # self.log.info('Fetched poster for MediaItem', media_item=media_item)

        self.log.debug("Adding media_list_items", media_item=media_item)
        self.db.media_list_items.insert_one(media_list_item.dict())
        self.log.debug("Inserted media_list_item", media_list_item=media_list_item)
        self.log.debug('Created MediaListItem from MediaItem', media_item=media_item.dict())
        return media_list_item
