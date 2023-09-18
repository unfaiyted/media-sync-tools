from abc import ABC
from typing import Optional

from src.models import PlexFilters
from src.create.providers.list import ListProvider
from src.config import ConfigManager
from src.models import JellyfinFilters, Provider
from src.create.providers.poster.jellyfin import JellyfinPosterProvider
from src.create.posters import MediaPosterImageCreator
from src.create.providers.poster.manager import PosterProviderManager
from src.models import MediaList,  MediaListType, MediaItem, MediaPoster
from src.clients.jellyfin import JellyfinClient


class JellyfinListProvider(ListProvider, ABC):
    def __init__(self, config: ConfigManager,
                 media_list: Optional[MediaList] = None,
                 list_type: MediaListType = MediaListType.COLLECTION,
                 filters: Optional[JellyfinFilters] = None,
                 details: Optional[dict] = None,
                 client_id: str = 'jellyfin'):
        """
        Initialize the JellyfinProvider.
        :param config: Instance of ConfigManager
        :param filters:
        :param details:
        :param list_type:
        """
        super().__init__(config)
        self.name = Provider.JELLYFIN
        self.config = config
        self.log = config.get_logger()
        self.client_id = client_id
        self.client: JellyfinClient = config.get_client(client_id)
        self.filters = filters
        self.media_list = media_list
        self.server_url = self.client.server_url
        self.api_key = self.client.api_key
        self.poster_manager = PosterProviderManager(config=config)
        self.list_type = list_type
        self.details = details

        if media_list:
            self.log.debug("Using existing MediaList", media_list=media_list)
            self.filters = media_list.filters

        if filters is not None:
            self.log.debug("Using filters", filters=filters)
            self.id = filters.listId
            self.library_name = filters.library

        self.log.debug("JellyfinProvider initialized", id=self.id, library_name=self.library_name)

    def get_list_by_id(self, list_id: str):
        """
        Retrieve MediaList from Emby.
        :return:
        """
        self.log.info("Getting Emby list by id", parent_id=self.id)

        emby_list = self.client.get_list(list_id=self.id)

        filters = PlexFilters(
            clientId=self.client_id,
            listId=list_id)

        return MediaList.from_emby(log=self.log,
                                   emby_list=emby_list,
                                   client_id=self.client_id,
                                   creator_id=self.config.get_user().userId,
                                   filters=filters.dict())

    async def get_list(self):
        """
        Retrieve MediaList from Jellyfin.
        :return:
        """
        self.log.info("Getting Jellyfin list")
        if self.id is None and self.library_name is None:
            self.log.error("No filter provided. Cannot get list.")
            return None
        elif self.library_name is not None:
            self.log.debug("Getting library by name", library_name=self.library_name)
            self.id = self.client.get_library(self.library_name)

        if self.id is not None:
            self.log.debug("Getting items from parent", parent_id=self.id)
            all_list_items = self.client.get_all_items_from_parent(self.id)

            media_list = self.get_list_by_id(self.id)

            self.log.debug("Inserted MediaList in database", media_list=media_list)
            for item in all_list_items:
                self.log.debug("Creating media list item", item=item, media_list=media_list)
                media_item = MediaItem.from_jellyfin(item, self.log)
                media_list.items.append(await self.create_media_list_item(media_item, media_list))

            return media_list
        return None

    def upload_list(self, media_list: MediaList):
        """
        Upload a MediaList to Jellyfin.
        :param media_list:
        :return:
        """
        if media_list is None:
            self.log.info('no list provided')
            return None
        list_type: MediaListType = media_list.type

        if list_type == MediaListType.COLLECTION:
            emby_list = self.client.create_collection(media_list.name, media_list.sortName)
        elif list_type == MediaListType.PLAYLIST:
            emby_list = self.client.create_playlist(media_list.name, media_list.sortName)
        else:
            self.log.info('invalid list type')
            return None

        # Main List Poster
        self.save_poster(media_list.sourceListId, media_list.poster)

        self.log.debug(f'adding {len(media_list.items)} items to list {emby_list["Name"]}', emby_list=emby_list)
        for media_list_item in media_list.items:
            self.log.debug(f'adding item {media_list_item.item.title} to list {emby_list["Name"]}', emby_list=emby_list)
            emby_item = self.client.search_media_item_by_external_ids(media_list_item.item)

            if emby_item is None:
                self.log.info(f'item {media_list_item.item.title} not found', title=media_list_item.item.title)
                continue

            if list_type == MediaListType.PLAYLIST:
                self.log.debug(f'adding item {media_list_item.item.title} to playlist {emby_list["Name"]}',
                               emby_list=emby_list)
                self.client.add_item_to_playlist(emby_list['Id'], emby_item['Id'])
            elif list_type == MediaListType.COLLECTION:
                self.log.debug(f'adding item {media_list_item.item.title} to collection {emby_list["Name"]}',
                               emby_list=emby_list)
                self.client.add_item_to_collection(emby_list['Id'], emby_item['Id'])

            poster = (media_list_item.poster if media_list_item.poster is not None else media_list_item.item.poster)
            # Item Poster
            self.save_poster(emby_item['Id'], poster)
            self.log.debug(f'added item {media_list_item.item.title} to list {emby_list["Name"]}', emby_list=emby_list)
        return media_list

    def save_poster(self, item_id: str, poster: MediaPoster or str):
        # TODO: Look into moving logic to JellyfinClient
        """
        Save a poster to Jellyfin.
        :param item_id:
        :param poster:
        :return:
        """
        if poster is None:
            self.log.info('no poster provided')
            return None

        if poster.startswith('http'):
            self.log.info('downloading image from url', url=poster)
            self.client.upload_image_from_url(item_id, poster, root_path=self.config.get_root_path())
        elif poster.startswith('/'):
            self.log.info('uploading image from local', path=poster)
            self.client.upload_image(item_id, poster)
        # if the poster is a MediaPoster object, process the image
        elif isinstance(poster, MediaPoster):
            self.log.info('uploading image from MediaPoster instance', poster=poster)
            # create image from MediaPoster
            poster = MediaPosterImageCreator(poster, self.log)
            poster = poster.create()
            poster_location = f'{self.config.get_root_path()}/poster.png'
            poster.save(poster_location)
            self.client.upload_image(item_id, poster_location)
