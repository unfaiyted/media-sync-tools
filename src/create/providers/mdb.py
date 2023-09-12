import uuid
from datetime import datetime
from typing import Optional

from src.models.providers.mdb import MdbItem
from src.clients.mdblist import MdbClient
from src.config import ConfigManager
from src.create.providers.base_provider import BaseMediaProvider
from src.models import MediaList, MediaListItem, MediaType, MediaListType, MediaItem, MediaProviderIds
from src.models.filters import MdbFilters


class MdbProviderResult:
    def __init__(self, id, name, description, movies):
        self.id = id
        self.name = name
        self.description = description
        self.movies = movies


class MdbProvider(BaseMediaProvider):

    def __init__(self, config: ConfigManager, filters: Optional[MdbFilters] = None, details: Optional[dict] = None,
                 media_list: Optional[MediaList] = None, list_type: MediaListType = MediaListType.COLLECTION):
        """
        Initialize the MdbProvider.
        :param config: Configuration for the provider.
        :param filters: Optional filters to apply.
        :param details: Optional override details for MediaList
        :param list_type: Type of media list. Default is COLLECTION.
        """
        super().__init__(config)
        self.config = config
        self.log = config.get_logger(__name__)
        self.listType = list_type
        self.client: MdbClient = config.get_client('mdb')
        self.filters = filters

        if media_list:
            self.log.debug("Using existing MediaList", media_list=media_list)
            self.filters = media_list.filters
            self.id = self.filters.listId

        if filters is not None:
            self.log.debug("Using filters", filters=filters)
            self.id = filters.listId
        self.log.info("MdbProvider initialized", filters=filters, id=self.id)

    @staticmethod
    def _map_mdb_item_to_media_item(item: MdbItem):
        return MediaItem(
            mediaItemId=str(uuid.uuid4()),
            title=item.title,
            year=item.release_year,
            type=MediaType.MOVIE if item.mediatype == 'movie' else MediaType.SHOW,
            providers=MediaProviderIds(
                imdbId=item.imdb_id,
                tvdbId=item.tvdb_id,
            ),
        )

    async def get_list(self) -> MediaList or None:
        """
        Retrieve media list from Mdb.
        :return:
        """
        db = self.config.get_db()

        if self.id is None:
            self.log.error('No list id provided. Cannot get list.')
            return None

        mdb_list = self.client.get_list_information(list_id=self.id)[0]
        list_items = self.client.get_list_items_as_objects(mdb_list['id'])
        self.log.debug('MDB list items', list_items=list_items)

        media_list = MediaList(
            mediaListId=str(uuid.uuid4()),
            name=mdb_list['name'],
            type=self.listType,
            sortName=mdb_list['name'],
            filters=self.filters.dict(),
            items=[],
            clientId='mdb',
            createdAt=datetime.now(),
            creatorId=self.config.get_user().userId
        )

        db.media_lists.insert_one(media_list.dict())

        for item in list_items:
            self.log.debug('Original MDB item', item=item)
            media_item = self._map_mdb_item_to_media_item(item)
            self.log.debug("Appending media item", item=item, media_list=media_list)
            media_list.items.append(await self.create_media_list_item(media_item, media_list))

        self.log.debug("Returning media list", media_list=media_list)
        return media_list

    async def upload_list(self, media_list: MediaList):
        # TODO: implement
        self.log.info("Uploading list", media_list=media_list)
        pass
