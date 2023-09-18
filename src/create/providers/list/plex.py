import uuid
from abc import ABC
from datetime import datetime
from typing import  Optional
from plexapi.server import PlexServer

from src.create.providers.poster.plex import PlexPosterProvider
from src.create.providers.list import ListProvider
from src.clients.plex import PlexManager
from src.config import ConfigManager

from src.models import PlexFilters, Provider
from src.models import MediaList,   MediaListType, MediaItem


class PlexListProvider(ListProvider, ABC):
    def __init__(self, config: ConfigManager, filters: Optional[PlexFilters] = None, details: Optional[dict] = None,
                 media_list: Optional[MediaList] = None, list_type: MediaListType = MediaListType.COLLECTION,
                 client_id: str = 'plex'):
        """
        Initialize the PlexProvider.
        :param config:
        :param filters:
        :param details: would provide detail overrides for the MediaList...
        :param media_list:
        :param list_type:
        """
        super().__init__(config, client_id=client_id)
        self.config = config
        self.name = Provider.PLEX
        self.log = config.get_logger(__name__)
        self.client_id = client_id
        self.media_list = media_list
        self.override_details = details
        self.filters = media_list.filters if media_list else {}
        self.list_type = self.media_list.type if self.media_list else list_type
        self.plex_manager = PlexManager(self.config)

        if filters:
            self.filters = filters

    def get_list_by_id(self, list_id: str):
        """
        Retrieve MediaList from Plex.
        :return:
        """
        self.log.info("Getting Plex list by id", parent_id=self.id)
        plex_list = self.plex_manager.search_lists_by_type(list_id, self.list_type)

    async def get_list(self):
        db = self.config.get_db()
        plex_list = None

        if self.filters.listId:
            self.log.info("Getting Plex list", list_id=self.filters.listId)
            plex_list = self.plex_manager.search_lists_by_type(self.filters.listId,
                                                               self.list_type)  # Assume your Plex client has a method called getList

            if plex_list is None:
                self.log.error('No list found')
                return None

            self.log.debug("Getting Plex list items", plex_list=plex_list)
            list_items = self.plex_manager.search_list_items(plex_list, self.list_type)
        else:
            self.log.debug("Getting Plex list items", filters=self.filters)
            parsed_filters = self.filters.parse_filters()
            list_items = self.plex_manager.search_libraries(parsed_filters)

        if plex_list is not None:
            self.log.debug("Creating MediaList from Plex list", plex_list=plex_list)
            creator_id = self.config.get_user().userId
            self.media_list = MediaList.from_plex(self.log, plex_list, creator_id, self.media_list.filters)
        else:
            self.log.debug("Creating MediaList from Plex filters", filters=self.filters)
            self.media_list.type = self.list_type

        self.media_list.creatorId = self.config.get_user().userId
        self.media_list.createdAt = datetime.now()

        db.media_lists.insert_one(self.media_list.dict())
        self.log.debug("Created MediaList", media_list=self.media_list)

        for item in list_items:
            self.log.debug("Creating media item", item=item, media_list=self.media_list)
            media_item = MediaItem.from_plex(item, self.log)
            self.media_list.items.append(
                await self.create_media_list_item(media_item, self.media_list ))
            # Adjust the logic based on how Plex's client class methods and responses are structured.

        self.log.debug("Created MediaList", media_list=self.media_list)
        return self.media_list
