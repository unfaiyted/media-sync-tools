from create.providers.library.manager import LibraryProviderManager
from create.providers.list.manager import ListProviderManager
from create.providers.poster import PosterProvider
from create.providers.poster.manager import PosterProviderManager
from models import MediaItem


class AppProviderManager:

    def __init__(self, config):
        """
        Initialize the AppProviderManager.
        :param config: Configuration settings
        """
        self.config = config
        self.log = config.get_logger(__name__)

        self.list_provider_manager = ListProviderManager(config)
        self.poster_provider_manager = PosterProviderManager(config)
        self.library_provider_manager = LibraryProviderManager(config)

    def get_poster(self, preferred_provider: PosterProvider, media_item: MediaItem):
        """
        Get a poster for a specific media item.
        :param preferred_provider: Preferred poster provider
        :param media_item: Media item for which the poster is required
        :return: The poster
        """
        return self.poster_provider_manager.get_poster(preferred_provider, media_item)

    def get_list(self, client_id, query_params):
        """
        Get a list based on query parameters.
        :param client_id:
        :param query_params: Parameters to filter
        :return: The list
        """
        return self.list_provider_manager.get_list(client_id, query_params)

    def sync_library(self, client_id, library_name):
        """
        Sync a specific library.
        :param client_id:
        :param library_name: Name of the library
        :return: Sync status
        """
        return self.library_provider_manager.sync_library(client_id, library_name)




    # You can further add methods as per
