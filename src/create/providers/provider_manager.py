from src.create.providers.poster.emby import EmbyPosterProvider
from src.create.providers.poster.jellyfin import JellyfinPosterProvider
from src.create.providers.poster.plex import PlexPosterProvider
from src.create.providers.poster.tmdb import TmdbPosterProvider
from src.create.providers.poster.trakt import TraktPosterProvider
from src.create.providers.poster import PosterProvider

from src.models import MediaItem


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

