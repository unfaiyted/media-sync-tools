# Let's call this base_provider.py
import uuid
from abc import ABC
from datetime import datetime
from typing import Optional

from src.create.providers.posters import TmdbPosterProvider, PosterProvider
from src.create.providers.managers import PosterProviderManager
from src.models import MediaItem, MediaProviderIds, MediaList, MediaListItem


class BaseMediaProvider(ABC):  # ABC means it's an abstract base class
    def __init__(self, config):
        """
        Initialize the BaseMediaProvider.
        This is responsible for fetching items from a provider and creating MediaListItems/MediaItems.
        :param config:
        """
        self.config = config
        self.poster_manager = PosterProviderManager(config=config)
        self.log = config.get_logger(__name__)

    async def get_existing_media_item(self, media_item: MediaItem) -> Optional[MediaItem]:
        """
        Get an existing media item from the database.
        :param media_item:
        :return:
        """
        db = self.config.get_db()
        for field in MediaProviderIds.__fields__:
            if provider_id := getattr(media_item.providers, field, None):
                existing_media_item = await db.media_items.find_one(
                    {f"providers.{field}": provider_id}
                )
                if existing_media_item:
                    return MediaItem.parse_obj(existing_media_item)

        # If not found by provider ID, check by title and year
        if media_item.title and media_item.year:
            self.log.info('No existing media item found by provider ID. Checking by title and year.',
                          media_item=media_item.dict())
            existing_item = await db.media_items.find_one({"title": media_item.title, "year": media_item.year})
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

    async def create_media_list_item(self, media_item: MediaItem, media_list: MediaList,
                                     preferred_poster_provider: PosterProvider = None,
                                     ) -> MediaListItem:
        """
        Create a MediaListItem from a provider item.

        :param preferred_poster_provider: Preferred poster provider to use.
        :param media_item: Item fetched from provider.
        :param media_list: The MediaList item belongs to.
        :return: MediaItem object.
        """
        db = self.config.get_db()

        if preferred_poster_provider is None:
            preferred_poster_provider = TmdbPosterProvider(config=self.config)

        self.log.info('Creating MediaListItem from MediaItem', media_item=media_item)

        if existing_media_item := await self.get_existing_media_item(media_item):
            self.log.debug("Found existing media_item", media_item=existing_media_item)
            media_item = await self.merge_and_update_media_item(media_item, existing_media_item)

        if media_item.poster is None:
            self.log.info('Fetching poster for MediaItem', media_item=media_item)
            media_item.poster = await self.poster_manager.get_poster(preferred_provider=preferred_poster_provider,
                                                                     media_item=media_item)
            self.log.info('Fetched poster for MediaItem', media_item=media_item)

        media_list_item = MediaListItem(
            mediaListItemId=str(uuid.uuid4()),
            mediaItemId=media_item.mediaItemId,
            mediaListId=media_list.mediaListId,
            item=media_item,
            dateAdded=datetime.now(),
        )

        self.log.debug("Adding media_list_items", media_item=media_item)
        db.media_list_items.insert_one(media_list_item.dict())
        self.log.debug("Inserted media_list_item", media_list_item=media_list_item)
        self.log.debug('Created MediaListItem from MediaItem', media_item=media_item.dict())
        return media_list_item
