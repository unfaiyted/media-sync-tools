import uuid
from abc import ABC, abstractmethod
from datetime import datetime

from src.models import MediaList, MediaListType, EmbyFilters, ProviderType
from src.create.providers.media_provider import MediaProvider

from src.models import Library


class LibraryProvider(MediaProvider, ABC):

    def __init__(self, config, client_id):
        super().__init__(config, client_id=client_id)
        self.config = config
        self.log = config.get_logger(__name__)
        self.type = ProviderType.LIBRARY
        self.client_id = client_id
        self.db = self.config.get_db()

    # @abstractmethod
    # def sync_all_library_items(self):
    #     """
    #     Sync all library items from provider.
    #     :return:
    #     """
    #     pass

    # @abstractmethod
    # def save_poster(self, item_id: str, poster: MediaPoster or str):
    #     """
    #     Save poster to provider.
    #     :return:
    #     """
    # pass

    # @abstractmethod
    # async def fetch_provider_library_items(self, library: Library):
    #     """
    #     Fetch library items from the provider for a specific library.
    #     """
    #     pass

    @abstractmethod
    def convert_to_media_item(self, provider_item):
        """
        Convert provider's item format to common MediaItem format.
        """
        pass

    @abstractmethod
    async def fetch_provider_libraries(self):
        """
        Fetch libraries from the provider.
        """
        pass

    @abstractmethod
    def convert_to_library(self, provider_library):
        """
        Convert provider's library format to common Library format.
        """
        pass

    async def get_libraries(self):
        libraries = await self.fetch_provider_libraries()
        self.log.debug("Fetched libraries", libraries=libraries)
        return [self.convert_to_library(provider_library) for provider_library in libraries]

    async def sync_libraries(self, libraries: list[Library] = None):
        if libraries is None:
            self.log.info("No libraries provided, fetching from provider")
            libraries = await self.get_libraries()

        for library in libraries:
            existing_library = await self.db.libraries.find_one({"sourceId": library.sourceId})
            if existing_library is None:
                self.log.info("Inserting library", library=library)
                await self.db.libraries.insert_one(library.dict())
            else:
                self.log.info("Updating library", library=library)
                await self.db.libraries.update_one({"sourceId": library.sourceId}, {"$set": library.dict()})

        return libraries

    async def sync_library_items(self, library: Library):
        """
        Sync library items.
        :param library:
        :return:
        """

        if library is None:
            self.log.error("No library provided")
            return None

        all_provider_items = await self.fetch_provider_library_items(library)

        media_list = MediaList(
            mediaListId=str(uuid.uuid4()),
            name=library.name,
            type=MediaListType.LIBRARY,
            sourceListId=library.sourceId,
            filters=EmbyFilters(
                clientId=library.clientId,
                library=library.name).dict(),  # This might need to be made more generic.
            items=[],
            sortName=library.name,
            clientId=library.clientId,  # This might need to be made more generic.
            createdAt=datetime.now(),
            creatorId=self.config.get_user().userId
        )

        existing_media_list = await self.db.media_lists.find_one({"sourceListId": library.sourceId})
        if existing_media_list is not None:
            self.log.info("Updating existing MediaList", media_list=existing_media_list)
            media_list = MediaList(**existing_media_list)
            media_list.items = []

        for provider_item in all_provider_items:
            self.log.debug("Converting provider item to MediaItem", provider_item=provider_item)
            media_item = self.convert_to_media_item(provider_item)
            self.log.debug("Converted provider item to MediaItem", media_item=media_item)

            # TODO: check if this item is already in the media list

            # I've kept the poster provider part in the Emby specific class below.
            media_list.items.append(media_item)

        self.log.info("Saving MediaList", total_items=len(media_list.items), media_list=media_list)
        self.log.debug("Synced Jellyfin library items", library=library, media_list=media_list)

        for item in media_list.items:
            self.log.debug("Creating media list item", item=item)
            media_list.items.append(
                await self.create_media_list_item(item, media_list)
            )
        return media_list

    @abstractmethod
    def fetch_provider_library_items(self, library):
        """
        Fetch library items from the provider for a specific library.
        :param library:
        :return:
        """
        pass
