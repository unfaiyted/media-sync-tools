import uuid
from abc import ABC
from datetime import datetime

from src.models import LibraryType, Provider
from src.create.providers.library import LibraryProvider
from src.create.providers.poster.jellyfin import JellyfinPosterProvider
from src.models import Library, MediaItem


class JellyfinLibraryProvider(LibraryProvider, ABC):

    def __init__(self, config, client_id='jellyfin'):
        """
        Initialize the JellyfinLibraryProvider.
        :param config:
        """
        super().__init__(config, client_id=client_id)
        self.log = config.get_logger(__name__)
        self.client_id = client_id
        self.name = Provider.JELLYFIN

    def get_client(self):
        return self.config.get_client(self.client_id)

    async def fetch_provider_libraries(self):
        return self.get_client().get_libraries()

    def convert_to_library(self, provider_library):
        return Library.from_jellyfin(provider_library, self.config.config_id)

    async def fetch_provider_library_items(self, library: Library):
        return self.get_client().get_all_items_from_library(library.sourceId)

    def convert_to_media_item(self, provider_item):
        self.log.debug("Converting Emby item to MediaItem", provider_item=provider_item)
        return MediaItem.from_jellyfin(provider_item, self.log)


