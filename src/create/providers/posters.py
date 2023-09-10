from abc import ABC, abstractmethod
from typing import Optional

from src.create.providers.provider_manager import ProviderManager
from src.models import MediaItem


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


class PosterManager:

    def __init__(self, config):
        self.config = config
        emby = EmbyPosterProvider(config=config)
        plex = PlexPosterProvider(config=config)
        trakt = TraktPosterProvider(config=config)

        # Add any other providers you have
        self.provider_manager = ProviderManager(emby, plex, trakt)

    def get_poster(self, preferred_provider: PosterProvider, media_item: MediaItem):
        head = self.provider_manager.prioritize_provider(preferred_provider)
        return head.get_poster(self.config, media_item)


