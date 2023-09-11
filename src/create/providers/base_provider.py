# Let's call this base_provider.py
from abc import ABC
from typing import Optional
from src.models import MediaItem, MediaProviderIds


class BaseMediaProvider(ABC):  # ABC means it's an abstract base class
    def __init__(self, config):
        self.config = config
        self.log = config.get_logger(__name__)

    async def get_existing_media_item(self, media_item: MediaItem) -> Optional[MediaItem]:
        db = self.config.get_db()
        for field in MediaProviderIds.__fields__:
            provider_id = getattr(media_item.providers, field, None)
            if provider_id:
                existing_media_item = await db.media_items.find_one({"providers." + field: provider_id})
                if existing_media_item:
                    return MediaItem.parse_obj(existing_media_item)

        # If not found by provider ID, check by title and year
        if media_item.title and media_item.year:
            self.log.info('No existing media item found by provider ID. Checking by title and year.', media_item=media_item.dict())
            existing_item = await db.media_items.find_one({"title": media_item.title, "year": media_item.year})
            if existing_item:
                return MediaItem.parse_obj(existing_item)

        self.log.info('No existing media item found', media_item=media_item.dict())
        return None

    @staticmethod
    async def merge_media_items(media_item: MediaItem, existing_media_item: MediaItem) -> MediaItem:
        for field in MediaItem.__fields__:
            if field == 'mediaItemId':
                continue
            existing_value = getattr(existing_media_item, field, None)
            if existing_value is None:
                setattr(existing_media_item, field, getattr(media_item, field))
        return existing_media_item

    async def merge_and_update_media_item(self, media_item: MediaItem, existing_media_item: MediaItem) -> MediaItem:
        db = self.config.get_db()
        merged_media_item = await self.merge_media_items(media_item, existing_media_item)
        db.media_items.update_one(
            {"mediaItemId": existing_media_item.mediaItemId},
            {"$set": merged_media_item.dict()}
        )
        self.log.info('Merged media item saved.', media_item=merged_media_item.dict())
        return merged_media_item
