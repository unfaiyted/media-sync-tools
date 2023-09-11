from src.models import MediaItem
from src.create.providers.posters import EmbyPosterProvider, PlexPosterProvider, TraktPosterProvider, PosterProvider, \
    JellyfinPosterProvider, TmdbPosterProvider


class ProviderManager:

    def __init__(self, *providers ):
        """
        Initialize the ProviderManager.
        :param providers:
        """
        self.providers = providers

    def prioritize_provider(self, preferred_provider):
        """ Prioritize a specific provider and chain the rest as fallbacks. """
        remaining_providers = [p for p in self.providers if p != preferred_provider]
        head = preferred_provider
        current = head

        for provider in remaining_providers:
            current = current.set_next(provider)

        return head


class PosterProviderManager:

    def __init__(self, config):
        """
        Initialize the PosterManager.
        :param config:
        """
        self.config = config
        self.log = config.get_logger(__name__)
        emby = EmbyPosterProvider(config=config)
        tmdb = TmdbPosterProvider(config=config)
        jellyfin = JellyfinPosterProvider(config=config)
        plex = PlexPosterProvider(config=config)
        trakt = TraktPosterProvider(config=config)

        # Add any other providers you have
        self.provider_manager = ProviderManager(tmdb, emby, jellyfin, plex, trakt)
        self.log.debug("PosterProviderManager initialized", provider_manager=self.provider_manager)

    def get_poster(self, preferred_provider: PosterProvider, media_item: MediaItem):
        self.log.debug("Getting poster for MediaItem", media_item=media_item)
        head = self.provider_manager.prioritize_provider(preferred_provider)
        return head.get_poster(self.config, media_item)
