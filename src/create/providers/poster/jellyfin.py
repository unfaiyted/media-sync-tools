from abc import ABC
from typing import Optional

from src.clients.jellyfin import JellyfinClient
from src.create.providers.poster import PosterProvider
from src.models import MediaItem


class JellyfinPosterProvider(PosterProvider, ABC):
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.log = config.get_logger(__name__)

    async def get_poster_from_source(self, config, media_item: MediaItem) -> Optional[str]:
        jellyfin: JellyfinClient = self.config.get_client('jellyfin')

        # Attempt to fetch from Emby
        poster = await jellyfin.get_poster_from_emby_by_media_item(media_item)
        if not poster and self.next_provider:
            self.log.info('Poster not found in Jellyfin! Attempting to fetch from next provider.')
            return await self.next_provider.get_poster(media_item)  # Ensure this is awaited if it's async
        return poster

