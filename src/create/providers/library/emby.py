import uuid
from abc import ABC
from datetime import datetime

from src.models import LibraryType
from src.create.providers.library import LibraryProvider
from src.create.providers.poster.emby import EmbyPosterProvider
from src.models import Library, MediaItem


class EmbyLibraryProvider(LibraryProvider, ABC):

    def __init__(self, config):
        """
        Initialize the EmbyLibraryProvider.
        :param config:
        """
        super().__init__(config)
        self.config = config
        self.log = config.get_logger(__name__)

    def create_client(self):
        return self.config.get_client('emby')

    async def fetch_provider_libraries(self):
        return self.create_client().get_libraries()


    def convert_to_library(self, provider_library):

        return Library(
            libraryId=str(uuid.uuid4()),
            name=provider_library['Name'],
            type=LibraryType.from_emby(provider_library.get('CollectionType', LibraryType.UNKNOWN)),
            sourceId=provider_library['Id'],
            createdAt=datetime.now(),
            configId=self.config.config_id,
            clientId='emby',
        )

    async def fetch_provider_library_items(self, library: Library):
        limit = 100
        offset = 0
        all_list_items = []

        while True:
            self.log.debug("Getting Emby library items", library=library, limit=limit, offset=offset)
            list_items, list_items_count = self.client.get_items_from_parent(library.sourceId, limit=limit, offset=offset)
            all_list_items.extend(list_items)
            offset += limit
            if offset > list_items_count:
                self.log.debug("Reached end of Emby library items", library=library, limit=limit, offset=offset)
                break

        return all_list_items

    def convert_to_media_item(self, provider_item):
        self.log.debug("Converting Emby item to MediaItem", provider_item=provider_item)
        return MediaItem.from_emby(provider_item, self.log)

    async def sync_library_items(self, library: Library):
        media_list = await super().sync_library_items(library)
        self.log.debug("Synced Emby library items", library=library, media_list=media_list)
        for item in media_list.items:
            self.log.debug("Creating media list item", item=item)
            media_list.items.append(
                await self.create_media_list_item(item, media_list, EmbyPosterProvider(config=self.config))
            )
        return media_list
