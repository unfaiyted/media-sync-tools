from abc import ABC
from typing import Optional

from src.create.providers.poster import PosterProvider
from src.models import MediaItem


class TraktPosterProvider(PosterProvider, ABC):
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.log = config.get_logger(__name__)

    async def get_poster_from_source(self, config, media_item: MediaItem) -> Optional[str]:
        self.log.info('Skipping fetch poster from Trakt', media_item=media_item.dict())
        # Not implemented for Trakt
        poster = None
        # Attempt to fetch from Next Provider
        if not poster and self.next_provider:
            return await self.next_provider.get_poster(media_item)  # Ensure this is awaited if it's async
        return poster


