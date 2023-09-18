from config import ConfigManager
from create.providers.list.emby import EmbyListProvider
from create.providers.list.jellyfin import JellyfinListProvider
from create.providers.list.plex import PlexListProvider
from create.providers.list.tmdb import TmdbListProvider
from create.providers.list.trakt import TraktListProvider
from models import Filters


class ListProviderManager:

    def __init__(self, config: ConfigManager, *providers: object):
        """
        Initialize the LibraryProviderManager.
        :param config:
        :param providers:
        """
        self.config = config
        self.log = config.get_logger(__name__)
        # TODO: Get user config to determine which providers to use dynamically
        emby = EmbyListProvider(config=config)
        jellyfin = JellyfinListProvider(config=config)
        plex = PlexListProvider(config=config)
        trakt = TraktListProvider(config=config)
        mdb = TraktListProvider(config=config)
        tmdb = TmdbListProvider(config=config)

        if not providers:
            providers = [emby, jellyfin, plex, trakt, mdb, tmdb]

        self.providers = providers
        self.log.debug("ListProviderManager initialized", providers=self.providers)

    def update_provider_config(self, provider_id, new_config):
        """
            Update the config for each provider
            :param new_config:
            :param provider_id:
            :return:
            """
        for provider in self.providers:
            if provider.client_id == provider_id:
                provider.config = new_config

    def search_all_providers_for_lists(self, query: str):
        """
        Search all providers for lists matching the query.
        :param query: Query to search for.
        :return: List of MediaList objects.
        """
        results = []
        for provider in self.providers:
            provider_results = provider.search_for_lists(query)
            results.extend(provider_results)
        return results

    def search_all_providers_for_list_items(self, query: str):
        """
        Search all providers for lists matching the query.
        :param query: Query to search for.
        :return: List of MediaList objects.
        """
        results = []
        for provider in self.providers:
            provider_results = provider.search_for_list_items(query)
            results.extend(provider_results)
        return results

    def get_list_by_id(self, list_id: str):
        """
        Get a list by id from the providers.
        :param list_id: ID of the list to retrieve.
        :return: MediaList object.
        """
        for provider in self.providers:
            try:
                # TODO: This method is not a great plan.
                # We should be able to determine what provider to use by client_id
                return provider.get_list_by_id(list_id)
            except Exception as e:
                self.log.error("Error getting list", provider=provider, error=e)
                continue

        return None

    def get_list_by_provider_and_id(self, client_id, list_id):
        """
        Get a list by id from the providers.
        :param client_id:
        :param list_id: ID of the list to retrieve.
        :return: MediaList object.
        """
        for provider in self.providers:
            if provider.client_id == client_id:
                return provider.get_list_by_id(list_id)
        return None

    def get_list(self, client_id, filters: Filters):
        """
        Get a list from the providers. If the list does not exist, create it.
        :param client_id:
        :param filters:
        :return:
        """
        for provider in self.providers:
            if provider.client_id == client_id:
                return provider.get_list(filters=filters)
        return None
    def get_list_with_items(self, client_id, filters: Filters):
        """
        Get a list from the providers. If the list does not exist, create it.
        :param client_id:
        :param filters:
        :return:
        """
        pass
