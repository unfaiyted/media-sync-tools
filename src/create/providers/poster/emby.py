from abc import ABC
from typing import Optional

from src.create.providers.poster import PosterProvider
from src.models import MediaItem


class EmbyPosterProvider(PosterProvider, ABC):
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.log = config.get_logger(__name__)

    async def get_poster_from_source(self, config, media_item: MediaItem) -> Optional[str]:
        self.log.info('Skipping fetch poster from Emby', media_item=media_item.dict())
        emby = self.config.get_client('emby')

        # Attempt to fetch from Emby
        poster = await emby.get_poster_from_emby_by_media_item(media_item, emby)
        if not poster and self.next_provider:
            self.log.debug('Poster not found in Emby! Attempting to fetch from next provider.', media_item=media_item.dict())
            return await self.next_provider.get_poster(media_item)  # Ensure this is awaited if it's async
        return poster

