import uuid
from abc import ABC
from datetime import datetime

from plexapi.server import PlexServer

from src.models import LibraryType
from src.create.providers.library import LibraryProvider
from src.create.providers.poster.plex import PlexPosterProvider
from src.models import Library, MediaItem


class PlexLibraryProvider(LibraryProvider, ABC):

    def __init__(self, config):
        super().__init__(config)
        self.client: PlexServer = config.get_client('plex')
        self.log = config.get_logger(__name__)

    def create_client(self):
        return self.config.get_client('plex')

    def convert_to_library(self, provider_library):
        return Library(
            libraryId=str(uuid.uuid4()),
            name=provider_library.title,
            type=LibraryType.from_plex(provider_library.type),
            sourceId=provider_library.key,
            createdAt=datetime.now(),
            configId=self.config.config_id,
            clientId='plex',
        )

    async def fetch_provider_libraries(self):
        return self.client.library.sections()

    async def fetch_provider_library_items(self, library: Library):

        plex_library = self.client.library.sectionByID(library.sourceId)
        all_list_items = plex_library.all()  # Fetch all items from the Plex library
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
                await self.create_media_list_item(item, media_list, PlexPosterProvider(config=self.config))
            )
        return media_list

