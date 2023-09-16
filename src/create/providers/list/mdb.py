from abc import ABC
from typing import Optional

from src.create.providers.poster.tmdb import TmdbPosterProvider
from src.create.providers.list import ListProvider
from src.clients.mdblist import MdbClient
from src.config import ConfigManager
from src.models import MediaList, MediaListType, Provider
from src.models.filters import MdbFilters


class MdbListProvider(ListProvider, ABC):

    def __init__(self, config: ConfigManager, filters: Optional[MdbFilters] = None, details: Optional[dict] = None,
                 media_list: Optional[MediaList] = None, list_type: MediaListType = MediaListType.COLLECTION,
                 client_id: str = 'mdb'):
        """
        Initialize the MdbProvider.
        :param config: Configuration for the provider.
        :param filters: Optional filters to apply.
        :param details: Optional override details for MediaList
        :param list_type: Type of media list. Default is COLLECTION.
        """
        super().__init__(config)
        self.name = Provider.MDB
        self.config = config
        self.client_id = client_id
        self.log = config.get_logger(__name__)
        self.list_type = list_type
        self.client: MdbClient = config.get_client(client_id)
        self.filters = filters

        if media_list:
            self.log.debug("Using existing MediaList", media_list=media_list)
            self.filters = media_list.filters
            self.id = self.filters.listId

        if filters is not None:
            self.log.debug("Using filters", filters=filters)
            self.id = filters.listId
        self.log.info("MdbProvider initialized", filters=filters, id=self.id)

    def get_list_by_id(self, list_id) -> MediaList | None:
        """
        Retrieve media list from Mdb.
        :return:
        """
        if self.id is None:
            self.log.error('No list id provided. Cannot get list.')
            return None

        mdb_list = self.client.get_list_information(list_id=self.id)[0]
        return MediaList.from_mdb(log=self.log,
                                  mdb_list=mdb_list,
                                  client_id=self.client_id,
                                  creator_id=self.config.get_user().userId,
                                  filters=self.filters)

    async def get_list(self) -> MediaList or None:
        """
        Retrieve media list from Mdb.
        :return:
        """
        db = self.config.get_db()

        if self.id is None:
            self.log.error('No list id provided. Cannot get list.')
            return None

        media_list = self.get_list_by_id(self.id)
        list_items = self.client.get_list_items_as_objects(media_list.sourceListId)

        db.media_lists.insert_one(media_list.dict())

        return self.add_items_to_media_list(media_list, 'mdb', list_items, TmdbPosterProvider(config=self.config))

    async def upload_list(self, media_list: MediaList):
        # TODO: implement
        self.log.info("Uploading list", media_list=media_list)
        pass
