import uuid
from datetime import datetime
from typing import Optional

from src.config import ConfigManager
from src.models import EmbyFilters
from src.create.providers.posters import EmbyPosterProvider
from src.create.providers.base_provider import BaseMediaProvider
from src.create.posters import MediaPosterImageCreator
from src.create.providers.managers import PosterProviderManager
from src.models import MediaList, MediaType, MediaListType, MediaItem, MediaProviderIds, MediaPoster
from src.clients.emby import EmbyClient


class EmbyProvider(BaseMediaProvider):
    def __init__(self, config: ConfigManager, filters: Optional[EmbyFilters] = None, details: Optional[dict] = None,
                 media_list: Optional[MediaList] = None, list_type: MediaListType = MediaListType.COLLECTION):
        """
        Initialize the EmbyProvider.
        :param config: Instance of ConfigManager
        :param filters:
        :param details:
        :param list_type:
        """
        super().__init__(config)  # Initialize the BaseMediaProvider
        self.config = config
        self.log = config.get_logger(__name__)
        self.client: EmbyClient = config.get_client('emby')
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

        if self.filters is not None:
            if isinstance(self.filters, EmbyFilters):
                self.log.debug("Using filters", filters=filters)
                self.id = self.filters.listId
                self.library_name = self.filters.library
                self.log.debug("Emby type Filter initialized", id=self.id, library_name=self.library_name)
            else:
                self.log.warn("Invalid filters provided", filters=filters)

        self.log.debug("EmbyProvider initialized", filters=self.filters)

    async def get_list(self):
        """
        Retrieve MediaList from Emby.
        :return:
        """
        self.log.info("Getting Emby list")
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
                filters=self.filters,
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
                media_item = self._map_emby_item_to_media_item(item, self.log)
                media_list.items.append(await self.create_media_list_item(media_item, media_list, EmbyPosterProvider(config=self.config)))

            return media_list
        return None

    @staticmethod
    def _map_emby_item_to_media_item(provider_item: dict, log) -> MediaItem:
        """
        Map an Emby item to a MediaItem.
        :param provider_item:
        :param log:
        :return:
        """
        log.info(f"Mapping Emby item to MediaItem", provider_item=provider_item)
        return MediaItem(
            mediaItemId=str(uuid.uuid4()),
            title=provider_item.get('Name', 'TITLE MISSING'),
            year=provider_item.get('ProductionYear', None),
            description=provider_item.get('Overview', None),
            type=MediaType.MOVIE if provider_item['Type'] == 'Movie' else MediaType.SHOW,
            providers=MediaProviderIds(
                imdbId=provider_item['ProviderIds'].get('IMDB', None),
                tvdbId=provider_item['ProviderIds'].get('Tvdb', None)
            ),
        )

    def upload_list(self, media_list: MediaList):
        """
        Upload a MediaList to Emby.
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

        self.log.debug(f'Adding {len(media_list.items)} items to list {emby_list["Name"]}', emby_list=emby_list)
        for media_list_item in media_list.items:
            self.log.debug(f'Adding item {media_list_item.item.title} to list {emby_list["Name"]}', emby_list=emby_list)
            emby_item = self.client.search_media_item_by_external_ids(media_list_item.item)

            if emby_item is None:
                self.log.info(f'Item {media_list_item.item.title} not found', title=media_list_item.item.title)
                continue

            if list_type == MediaListType.PLAYLIST:
                self.log.debug(f'Adding item {media_list_item.item.title} to playlist {emby_list["Name"]}', emby_list=emby_list)
                self.client.add_item_to_playlist(emby_list['Id'], emby_item['Id'])
            elif list_type == MediaListType.COLLECTION:
                self.log.debug(f'Adding item {media_list_item.item.title} to collection {emby_list["Name"]}', emby_list=emby_list)
                self.client.add_item_to_collection(emby_list['Id'], emby_item['Id'])

            poster = (media_list_item.poster if media_list_item.poster is not None else media_list_item.item.poster)
            # Item Poster
            self.save_poster(emby_item['Id'], poster)
            self.log.debug('Poster saved', poster=poster)
        return media_list

    def save_poster(self, item_id: str, poster: MediaPoster or str):
        # TODO: Look into moving logic to EmbyClient
        """
        Save a poster to Emby.
        :param item_id:
        :param poster:
        :return:
        """
        if poster is None:
            self.log.info('No poster provided')
            return None

        if poster.startswith('http'):
            self.log.info('Downloading image from url', url=poster)
            self.client.upload_image_from_url(item_id, poster, root_path=self.config.get_root_path())
        elif poster.startswith('/'):
            self.log.info('Uploading image from local', path=poster)
            self.client.upload_image(item_id, poster)
        # if the poster is a MediaPoster object, process the image
        elif isinstance(poster, MediaPoster):
            self.log.info('Uploading image from MediaPoster', poster=poster)
            # create image from MediaPoster
            poster = MediaPosterImageCreator(poster, self.log)
            poster = poster.create()
            poster_location = f'{self.config.get_root_path()}/poster.png'
            poster.save(poster_location)
            self.client.upload_image(item_id, poster_location)
