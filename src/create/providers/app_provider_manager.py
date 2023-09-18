from config import ConfigManager
from create.providers.library.manager import LibraryProviderManager
from create.providers.list.manager import ListProviderManager
from create.providers.poster import PosterProvider
from create.providers.poster.manager import PosterProviderManager
from create.providers.poster.tmdb import TmdbPosterProvider
from models import MediaItem, Filters, MediaList


class AppProviderManager:

    def __init__(self, config):
        """
        Initialize the AppProviderManager.
        :param config: Configuration settings
        """
        self.config: ConfigManager = config
        self.log = config.get_logger(__name__)

        # Each provider manager is responsible for a specific type of provider, and will add the providers
        # that are configured from the applications the user config.
        self.list_provider_manager = ListProviderManager(config)
        self.poster_provider_manager = PosterProviderManager(config)
        self.library_provider_manager = LibraryProviderManager(config)

    def get_poster(self, media_item: MediaItem, preferred_provider: PosterProvider = None):
        """
        Get a poster for a specific media item.
        :param preferred_provider: Preferred poster provider
        :param media_item: Media item for which the poster is required
        :return: The poster
        """
        return self.poster_provider_manager.get_poster(media_item, preferred_provider)

    def get_list(self, client_id, filters: Filters) -> MediaList:
        """
        Get a list based on query parameters.
        :param filters:
        :param client_id:
        :return: The media list
        """
        return self.list_provider_manager.get_list(client_id, filters)

    def sync_library(self, client_id, library_name):
        """
        Sync a specific library.
        :param client_id:
        :param library_name: Name of the library
        :return: Sync status
        """
        return self.library_provider_manager.sync_library(client_id, library_name)

    def get_providers(self):
        """
        Get all configured clients details providers.
        :return: All providers
        """
        return self.config.get_client_details()

    def remove_provider(self, client_id):
        """
        Remove a provider.
        :param client_id:
        :return: True if removed, False otherwise
        """
        return self.config.remove_client(client_id)

    def add_provider(self, client_id, client_details):
        """
        Add a provider.
        :param client_id:
        :param client_details:
        :return: True if added, False otherwise
        """
        return self.config.add_client(client_id, client_details)

    def get_list_with_posters(self, client_id, filters: Filters, preferred_poster_provider: PosterProvider = None):
        """
        Get a list with posters.
        :param preferred_poster_provider:
        :param client_id:
        :param filters:
        :return: The list with posters
        """
        if preferred_poster_provider is None:
            preferred_poster_provider = TmdbPosterProvider(self.config)

        media_list = self.get_list(client_id, filters)
        for media_item in media_list:
            media_item.poster = self.get_poster(media_item, preferred_poster_provider)
        return media_list
