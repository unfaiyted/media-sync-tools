from src.models import MediaItem
from src.create.providers.posters import EmbyPosterProvider, PlexPosterProvider, TraktPosterProvider, PosterProvider


class ProviderManager:

    def __init__(self, *providers ):
        self.providers = providers

    def prioritize_provider(self, preferred_provider):
        """ Prioritize a specific provider and chain the rest as fallbacks. """
        remaining_providers = [p for p in self.providers if p != preferred_provider]
        head = preferred_provider
        current = head

        for provider in remaining_providers:
            current = current.set_next(provider)

        return head


class PosterManager:

    def __init__(self, config):
        self.config = config
        self.log = config.get_logger(__name__)
        emby = EmbyPosterProvider(config=config)
        plex = PlexPosterProvider(config=config)
        trakt = TraktPosterProvider(config=config)

        # Add any other providers you have
        self.provider_manager = ProviderManager(emby, plex, trakt)

    def get_poster(self, preferred_provider: PosterProvider, media_item: MediaItem):
        head = self.provider_manager.prioritize_provider(preferred_provider)
        return head.get_poster(self.config, media_item)
