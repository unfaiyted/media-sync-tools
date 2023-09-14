from abc import ABC, abstractmethod

from src.models import LibraryType
from src.create.providers.base_provider import BaseMediaProvider

from src.create.providers.managers import ProviderManager
from src.models import Library
from src.models import MediaPoster


class LibraryProvider(BaseMediaProvider, ABC):

    @staticmethod
    def _map_emby_library_type_to_media_list_type(self, library_type: str) -> LibraryType:
        """
        Map an Emby library type to a MediaListType.
        :param library_type:
        :return:
        """
        if library_type == 'movies':
            return LibraryType.MOVIES
        elif library_type == 'tvshows':
            return LibraryType.SHOWS
        else:
            return LibraryType.UNKNOWN

    @abstractmethod
    def get_libraries(self):
        """
        Retrieve a list of libraries from the provider.
        :return:
        """
        pass

    @abstractmethod
    def sync_libraries(self, libraries: list[Library]):
        """
        Sync libraries from provider.
        :return:
        """
        pass

    @abstractmethod
    def sync_library_items(self, library: Library):
        """
        Sync library items from provider.
        :return:
        """
        pass

    @abstractmethod
    def sync_all_library_items(self):
        """
        Sync all library items from provider.
        :return:
        """
        pass

    @abstractmethod
    def save_poster(self, item_id: str, poster: MediaPoster or str):
        """
        Save poster to provider.
        :return:
        """
        pass

