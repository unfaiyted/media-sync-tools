import uuid
from abc import ABC
from datetime import datetime
from typing import Optional

from src.create.providers.list import ListProvider
from src.config import ConfigManager
from src.models import JellyfinFilters
from src.create.providers.poster.jellyfin import JellyfinPosterProvider
from src.create.posters import MediaPosterImageCreator
from src.create.providers.managers import PosterProviderManager
from src.models import MediaList, MediaType, MediaListType, MediaItem, MediaProviderIds, MediaPoster
from src.clients.jellyfin import JellyfinClient


class JellyfinListProvider(ListProvider, ABC):
    def __init__(self, config: ConfigManager,
                 filters: Optional[JellyfinFilters] = None,
                 details: Optional[dict] = None,
                 media_list: Optional[MediaList] = None,
                 list_type: MediaListType = MediaListType.COLLECTION):
        """
        Initialize the JellyfinProvider.
        :param config: Instance of ConfigManager
        :param filters:
        :param details:
        :param list_type:
        """
        super().__init__(config)  # Initialize the BaseMediaProvider
        self.config = config
        self.log = config.get_logger()
        self.client: JellyfinClient = config.get_client('emby')
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
            limit = 100
            offset = 0
            all_list_items = []

            while True:
                list_items, list_items_count = self.client.get_items_from_parent(self.id, limit=limit, offset=offset)
                self.log.info("Getting items from parent", offset=offset, list_items_count=list_items_count)
                all_list_items.extend(list_items)
                offset += limit
                if offset > list_items_count:
                    break

            emby_list = self.client.get_list(list_id=self.id)
            db = self.config.get_db()

            media_list = MediaList(
                mediaListId=str(uuid.uuid4()),
                name=emby_list['Name'],
                type=self.list_type,
                sourceListId=emby_list['Id'],
                items=[],  # Will be populated later
                sortName=emby_list['SortName'],
                clientId='emby',
                createdAt=datetime.now(),
                creatorId=self.config.get_user().userId
            )

            db.media_lists.insert_one(media_list.dict())
            self.log.debug("Inserted MediaLis in database", media_list=media_list)

            for item in all_list_items:
                self.log.debug("Creating media list item", item=item, media_list=media_list)
                media_item = MediaItem.from_jellyfin(item, self.log)
                media_list.items.append(await self.create_media_list_item(media_item, media_list, JellyfinPosterProvider(config=self.config)))

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
                self.log.debug(f'adding item {media_list_item.item.title} to playlist {emby_list["Name"]}', emby_list=emby_list)
                self.client.add_item_to_playlist(emby_list['Id'], emby_item['Id'])
            elif list_type == MediaListType.COLLECTION:
                self.log.debug(f'adding item {media_list_item.item.title} to collection {emby_list["Name"]}', emby_list=emby_list)
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