from abc import ABC

from plexapi.server import PlexServer

from src.models import Provider
from src.create.providers.library import LibraryProvider
from src.create.providers.poster.plex import PlexPosterProvider
from src.models import Library, MediaItem


class PlexLibraryProvider(LibraryProvider, ABC):
    def __init__(self, config, config_id: str = 'plex'):
        super().__init__(config, config_id)
        self.log = config.get_logger(__name__)
        self.name = Provider.PLEX
        self.client: PlexServer = self.get_client()
        self.client_id = config_id

    def get_client(self):
        return self.config.get_client(self.client_id)

    def convert_to_library(self, provider_library):
        return Library.from_plex(provider_library, self.config.config_id)

    async def fetch_provider_libraries(self):
        return self.client.library.sections()

    async def fetch_provider_library_items(self, library: Library):
        plex_library = self.client.library.sectionByID(library.sourceId)
        all_list_items = plex_library.all()
        self.log.info("Total Plex library items", library=library, total=len(all_list_items))
        return all_list_items

    def convert_to_media_item(self, provider_item):
        return MediaItem.from_plex(provider_item, self.log)

    async def sync_library_items(self, library: Library):
        media_list = await super().sync_library_items(library)
        self.log.debug("Synced Plex library items", library=library, media_list=media_list)
        for item in media_list.items:
            self.log.debug("Creating media list item", item=item)
            media_list.items.append(
                await self.create_media_list_item(item, media_list)
            )
        return media_list

