from abc import ABC, abstractmethod
from typing import Optional, Union

from plexapi.server import PlexServer

from src.clients.jellyfin import JellyfinClient
from src.clients.tmdb import TmdbClient
from src.models import MediaItem, MediaProviderIds


class PosterProvider(ABC):

    def __init__(self):
        self.next_provider = None

    def set_next(self, provider: 'PosterProvider'):
        """
        Set the next provider in the chain.
        """
        self.next_provider = provider
        return provider  # This allows for method chaining

    @abstractmethod
    async def get_poster_from_source(self, config, media_item: MediaItem) -> Optional[str]:
        """
        Retrieve poster from specific provider's source. To be implemented by each derived provider.
        """
        pass

    async def get_poster(self, config, media_item: MediaItem) -> Optional[str]:
        """
        Attempt to get the poster using the current provider.
        If not available, delegate to the next provider in the chain.
        """
        poster = await self.get_poster_from_source(config, media_item)
        if not poster and self.next_provider:
            return await self.next_provider.get_poster(config, media_item)
        return poster

