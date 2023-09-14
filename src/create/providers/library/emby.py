import uuid
from abc import ABC
from datetime import datetime

from create.providers.libraries import LibraryProvider
from create.providers.posters import EmbyPosterProvider
from models import Library, MediaList, MediaListType, EmbyFilters, MediaItem


class EmbyLibraryProvider(LibraryProvider, ABC):

    def __init__(self, config):
        """
        Initialize the EmbyLibraryProvider.
        :param config:
        """
        super().__init__(config)
        self.config = config
        self.client = config.get_client('emby')
        self.log = config.get_logger(__name__)

    async def get_libraries(self):
        """
        Retrieve libraries from Emby.
        :return:
        """
        self.log.info("Getting Emby libraries")
        libraries = self.client.get_libraries()
        self.log.debug("Getting Emby libraries", library_count=len(libraries))

        libraries = []

        for provider_library in libraries:
            self.log.info("Getting Emby library", library=provider_library)
            libraries.append(Library(
                libraryId=str(uuid.uuid4()),
                name=provider_library['Name'],
                type=provider_library['Type'],
                sourceId=provider_library['Id'],
                clientId='emby',
                createdAt=datetime.now(),
            ))

        return libraries

    async def sync_libraries(self, libraries: list[Library] = None):
        """
        Sync libraries from Emby.
        :return:
        """
        db = self.config.get_db()
        self.log.info("Syncing Emby libraries")
        if libraries is None:
            libraries = await self.get_libraries()

        for library in libraries:
            existing_library = await db.libraries.find_one({"sourceId": library.sourceId})
            if existing_library is None:
                self.log.info("Inserting Emby library", library=library)
                await db.libraries.insert_one(library.dict())
            else:
                self.log.info("Updating Emby library", library=library)
                await db.libraries.update_one({"sourceId": library.sourceId}, {"$set": library.dict()})
        return libraries

    async def sync_library_items(self, library: Library):
        """
        Sync library items from Emby.
        :param library:
        :return:
        """
        db = self.config.get_db()
        self.log.info("Syncing Emby library items", library=library)
        if library is None:
            self.log.error("No library provided")
            return None

        # get library items
        limit = 100
        offset = 0
        all_list_items = []

        while True:
            list_items, list_items_count = self.client.get_items_from_parent(library.sourceId, limit=limit,
                                                                             offset=offset)
            self.log.info("Getting items from parent", offset=offset, list_items_count=list_items_count)
            all_list_items.extend(list_items)
            offset += limit
            if offset > list_items_count:
                break

        media_list = MediaList(
            mediaListId=str(uuid.uuid4()),
            name=library.name,
            type=MediaListType.LIBRARY,
            sourceListId=library.sourceId,
            filters=EmbyFilters(library=library.name),
            items=[],  # Will be populated later
            sortName=library.name,
            clientId='emby',
            createdAt=datetime.now(),
            creatorId=self.config.get_user().userId
        )

        # check if library already has a media list
        existing_media_list = await db.media_lists.find_one({"sourceListId": library.sourceId})
        if existing_media_list is not None:
            self.log.info("Updating existing MediaList", media_list=existing_media_list)
            media_list = MediaList(**existing_media_list)
            media_list.items = []
            await db.media_lists.update_one({"sourceListId": library.sourceId}, {"$set": media_list.dict()})

        for item in all_list_items:
            self.log.debug("Creating media list item", item=item, library=library)
            media_item = MediaItem.from_emby(item, self.log)

            #  TODO: check if this item is already in the media list

            media_list.items.append(
                await self.create_media_list_item(media_item, media_list, EmbyPosterProvider(config=self.config)))

        return media_list