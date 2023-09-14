import uuid
from abc import ABC
from datetime import datetime
from typing import Dict, List, Optional, Union
from plexapi.server import PlexServer
from plexapi.video import Movie, Show

from src.create.providers.list import ListProvider
from src.clients.plex import PlexManager
from src.config import ConfigManager
from src.create.providers.base_provider import BaseMediaProvider

from src.models import PlexFilters
from src.create.providers.poster.tmdb import  TmdbPosterProvider
from src.models import MediaList, MediaListItem, MediaType, MediaListType, MediaItem, MediaProviderIds


class PlexListProvider(ListProvider, ABC):
    def __init__(self, config: ConfigManager, filters: Optional[PlexFilters] = None, details: Optional[dict] = None,
                 media_list: Optional[MediaList] = None, list_type: MediaListType = MediaListType.COLLECTION):
        """
        Initialize the PlexProvider.
        :param config:
        :param filters:
        :param details:
        :param media_list:
        :param list_type:
        """
        super().__init__(config)
        self.config = config
        self.log = config.get_logger(__name__)
        self.client: PlexServer = config.get_client('plex')  # Retrieve the Plex client
        self.media_list = media_list
        self.filters = media_list.filters if media_list else {}
        self.list_type = self.media_list.type if self.media_list else list_type
        self.plex_manager = PlexManager(self.config)



    async def get_list(self):
        db = self.config.get_db()
        plex_list = None

        if self.filters.listId:
            self.log.info("Getting Plex list", list_id=self.filters.listId)
            plex_list = self.plex_manager.search_lists(self.filters.listId,
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
            self.media_list.name = plex_list.title
            self.media_list.type = self.list_type
            self.media_list.sortName = plex_list.titleSort
            self.media_list.description = plex_list.summary
        else:
            self.log.debug("Creating MediaList from Plex filters", filters=self.filters)
            self.media_list.name = self.media_list.name
            self.media_list.type = self.list_type
            self.media_list.sortName = self.media_list.sortName
            self.media_list.description = self.media_list.description

        self.media_list.creatorId = self.config.get_user().userId
        self.media_list.createdAt = datetime.now()

        db.media_lists.insert_one(self.media_list.dict())
        self.log.debug("Created MediaList", media_list=self.media_list)

        for item in list_items:
            self.log.debug("Creating media item", item=item, media_list=self.media_list)
            media_item = MediaItem.from_plex(item, self.log)
            self.media_list.items.append(
                await self.create_media_list_item(media_item, self.media_list, TmdbPosterProvider(config=self.config)))
            # Adjust the logic based on how Plex's client class methods and responses are structured.

        self.log.debug("Created MediaList", media_list=self.media_list)
        return self.media_list
