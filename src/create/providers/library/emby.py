from abc import ABC

from src.clients.emby import EmbyClient
from src.models import Provider
from src.create.providers.library import LibraryProvider
from src.models import Library, MediaItem


class EmbyLibraryProvider(LibraryProvider, ABC):

    def __init__(self, config, client_id='emby'):
        """
        Initialize the EmbyLibraryProvider.
        :param config:
        """
        super().__init__(config, client_id)
        self.name = Provider.EMBY
        self.client_id = client_id
        self.log = config.get_logger(__name__)

    def get_client(self) -> EmbyClient:
        self.log.debug("Getting Emby client", client_id=self.client_id)
        print(self.client_id)
        return self.config.get_client(self.client_id)

    async def fetch_provider_libraries(self):
        return self.get_client().get_libraries()

    def convert_to_library(self, provider_library):
        return Library.from_emby(provider_library, self.config.config_id)

    async def fetch_provider_library_items(self, library: Library):
        return self.get_client().get_all_items_from_parent(library.sourceId)

    def convert_to_media_item(self, provider_item):
        self.log.debug("Converting Emby item to MediaItem", provider_item=provider_item)
        return MediaItem.from_emby(provider_item, self.log)

