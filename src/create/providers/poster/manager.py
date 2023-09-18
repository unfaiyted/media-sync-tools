from abc import ABC

from src.create.providers.base_provider import BaseMediaProvider
from src.create.providers.poster.self import MediaPosterProvider
from src.create.providers.provider_manager import ProviderManager
from src.create.providers.poster import PosterProvider
from src.create.providers.poster.emby import EmbyPosterProvider
from src.create.providers.poster.jellyfin import JellyfinPosterProvider
from src.create.providers.poster.plex import PlexPosterProvider
from src.create.providers.poster.tmdb import TmdbPosterProvider
from src.create.providers.poster.trakt import TraktPosterProvider
from src.models import MediaItem


class PosterProviderManager(BaseMediaProvider, ABC):

    def __init__(self, config):
        """
        Initialize the PosterManager.
        :param config:
        """
        self.config = config
        self.log = config.get_logger(__name__)
        emby = EmbyPosterProvider(config=config)
        self = MediaPosterProvider(config=config)
        tmdb = TmdbPosterProvider(config=config)
        jellyfin = JellyfinPosterProvider(config=config)
        plex = PlexPosterProvider(config=config)
        trakt = TraktPosterProvider(config=config)

        # Add any other providers you have
        self.provider_manager = ProviderManager(tmdb, emby, jellyfin, plex, trakt)
        self.log.debug("PosterProviderManager initialized", provider_manager=self.provider_manager)

    def get_poster(self, media_item: MediaItem, preferred_provider: PosterProvider):
        self.log.debug("Getting poster for MediaItem", media_item=media_item)
        head = self.provider_manager.prioritize_provider(preferred_provider)
        return head.get_poster(self.config, media_item)
