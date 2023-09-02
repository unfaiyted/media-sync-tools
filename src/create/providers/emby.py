import uuid
from datetime import datetime

from src.create.posters import MediaPosterImageCreator
from src.models import MediaList, MediaListItem, MediaType, MediaListType, MediaItem, MediaProviderIds, MediaPoster

from typing import Optional

class EmbyProvider:
    def __init__(self, config, filters=None, details=None, listType=MediaListType.COLLECTION):
        self.config = config
        self.client: Emby = config.get_client('emby')
        self.filters = filters
        self.server_url = self.client.server_url
        self.api_key = self.client.api_key
        self.listType = listType
        self.details = details

        self.id, self.library_name = self.parse_filters(filters if filters is not None else [])
        print('id ',self.id)
        print('library name ', self.library_name)

    def parse_filters(self, filters):
        id_value = None
        library_value = None

        for f in filters:
            try:
                if f['type'] == 'list_id':
                    id_value = f.get('value')
                elif f['type'] == 'library':
                    library_value = f.get('value')
            except KeyError:
                print(f"Key 'name' missing in filter: {f}")

        return id_value, library_value

    async def get_list(self):
        print('get list')
        if self.id is None and self.library_name is None:
            print('No filter provided. Cannot get list.')
            return None
        elif self.library_name is not None:
            self.id = self.client.get_library(self.library_name)

        if self.id is not None:
            limit = 100
            offset = 0
            all_list_items = []

            while True:
                list_items, list_items_count = self.client.get_items_from_parent(self.id, limit=limit, offset=offset)
                print('Getting items from parent', offset, list_items_count)
                all_list_items.extend(list_items)
                offset += limit
                if offset > list_items_count:
                    break

            list_ = self.client.get_list(list_id=self.id)  # Renamed to avoid conflict with built-in name 'list'
            db = self.config.get_db()

            media_list = MediaList(
                mediaListId=str(uuid.uuid4()),
                name=list_['Name'],
                type=self.listType,
                sourceListId=list_['Id'],
                # filters=self.filters,
                items=[],  # Will be populated later
                sortName=list_['SortName'],
                clientId='EMBYCLIENTID',
                createdAt=datetime.now(),
                creatorId=self.config.get_user().userId
            )

            db.media_lists.insert_one(media_list.dict())

            for item in all_list_items:
                print('-------------', item)
                media_list.items.append(await self.create_media_item(item, media_list))

            return media_list
        return None

    def process_list_items(self, list_items):
        db = self.config.get_db()
        media_list_data = self.client.get_list(list_id=self.id)

        media_list = MediaList(
            mediaListId=str(uuid.uuid4()),
            name=media_list_data['Name'],
            type=self.listType,
            sortName=media_list_data['SortName'],
            clientId='EMBYLIST',
            createdAt=datetime.now(),
            creatorId="APPUSERID"
        )

        db.media_lists.insert_one(media_list.dict())

        primary_list = []

        for item in list_items:
            media_item, media_list_item = self.create_media_item(item, media_list)
            db.media_list_items.insert_one(media_list_item.dict())
            primary_list.extend(self.search_emby_for_external_ids(media_item))

        return primary_list

    async def create_media_item(self, item, media_list):
        db = self.config.get_db()

        poster_id = item['ImageTags'].get('Primary')
        poster_url = f"{self.server_url}/emby/Items/{item['Id']}/Images/Primary?api_key={self.api_key}&X-Emby-Token={self.api_key}" if poster_id else None

        media_item = MediaItem(
            mediaItemId=str(uuid.uuid4()),
            title=item.get('Name','TITLE MISSING'),
            year=item.get('ProductionYear', None),
            type=MediaType.MOVIE if item['Type'] == 'Movie' else MediaType.SHOW,
            poster=poster_url,
            providers=MediaProviderIds(
                imdbId=item['ProviderIds'].get('IMDB', None),
                tvdbId=item['ProviderIds'].get('Tvdb', None)
            ),
            # ... add any other fields you need here ...
        )

        # Check for existing mediaItem
        existing_media_item = None
        if media_item.providers.imdbId:
            existing_media_item = await db.media_items.find_one({"providers.imdbId": media_item.providers.imdbId})
        elif media_item.providers.tvdbId:
            existing_media_item = await db.media_items.find_one({"providers.tvdbId": media_item.providers.tvdbId})

        if existing_media_item:
            media_item.mediaItemId = existing_media_item['mediaItemId']
            valid_fields = {k: v for k, v in media_item.dict().items() if v}
            # Update missing fields
            # for field, value in media_item.dict().items():
            #     if value and not existing_media_item.get(field):
            #         existing_media_item[field] = value
            db.media_items.update_one(
                {"mediaItemId": existing_media_item["mediaItemId"]},
                {"$set": valid_fields }
            )
         # media_item.dict()
        else:
            print('inserting new media item')
            db.media_items.insert_one(media_item.dict())
            # return media_item.dict()

        media_list_item = MediaListItem(
            mediaListItemId=str(uuid.uuid4()),
            mediaListId=media_list.mediaListId,
            mediaItemId=media_item.mediaItemId,
            sourceId=item['Id'],
            dateAdded=datetime.now()
        )

        db.media_list_items.insert_one(media_list_item.dict())

        media_list_item.item = media_item

        return media_item

    def search_emby_for_external_ids(self, media_list_item: MediaListItem) -> dict or None:
        match = None
        def search_id(external_id: str) -> Optional[dict]:
            try:
                search_results = self.client.get_media(external_id=external_id)
                if search_results and search_results[0]['Type'] != 'Trailer':
                    return search_results[0]
                if search_results and search_results[0]['Type'] == 'Trailer':
                    return search_results[1]

            except Exception as e:
                print(f"Failed searching for {external_id} due to {e}")
            return None

        imdb_result = search_id(f"imdb.{media_list_item.item.providers.imdbId}")
        tvdb_result = search_id(f"tvdb.{media_list_item.item.providers.tvdbId}")
        tmdb_result = search_id(f"Tmdb.{media_list_item.item.providers.tmdbId}")

        if imdb_result:
           return imdb_result
        elif tvdb_result:
           return tvdb_result
        elif tmdb_result:
           return tmdb_result

            #emby_media_items = self.emby.search(media.title, emby_type)
            # for emby_media in emby_media_items:
                # try:
                    # if emby_media['ProductionYear'] == media.year:

        emby_type = 'Movie' if media_list_item.item.type == MediaType.MOVIE else 'Series'
        # Fallback to name and year
        search_results = self.client.search(media_list_item.item.title, emby_type)
        print('SEARCH RESULTS::::', search_results)
        if search_results:
                for result in search_results:
                    if int(result['ProductionYear']) == int(media_list_item.item.year):
                        match = result
                        break
                return match
        return match

    def upload_list(self, media_list: MediaList):
        if media_list is None:
            print('no list provided')
            return None

        # Will expect a media_list object and upload it to the provider
        # create a playlist or collection based on type
        # add items to the playlist or collection
        # return the playlist or collection id

        # print(media_list)
        type = media_list.type

        if type == MediaListType.COLLECTION:
           list = self.client.create_collection(media_list.name, media_list.sortName)
        elif type == MediaListType.PLAYLIST:
           list = self.client.create_playlist(media_list.name, media_list.sortName)
        else:
            print('invalid list type')
            return None


        # Main List Poster
        self.save_poster(media_list.sourceListId, media_list.poster)

        print(f'adding {len(media_list.items)} items to list {list["Name"]}')
        for media_list_item in media_list.items:
            print(f'adding item {media_list_item.item.title} to list {list["Name"]}')
            embyItem = self.search_emby_for_external_ids(media_list_item)

            if embyItem is None:
                print('item not found')
                continue

            if type == MediaListType.PLAYLIST:
                self.client.add_item_to_playlist(list['Id'], embyItem['Id'])
            elif type == MediaListType.COLLECTION:
                self.client.add_item_to_collection(list['Id'], embyItem['Id'])

            poster = (media_list_item.poster if media_list_item.poster is not None else media_list_item.item.poster)
            # Item Poster
            self.save_poster(embyItem['Id'], poster)
        return media_list

    def save_poster(self, item_id: str, poster: MediaPoster or str):
        if poster is None:
            print('no poster provided')
            return None

        # if the media_list.poster is a url, download the image and upload it to the provider
        # if the media_list.poster is a file path, upload the image to the provider
        # through the PosterImage class and upload it to the provider

        if poster.startswith('http'):
            print('downloading image from url')
            self.client.upload_image_from_url(item_id, poster, root_path=self.config.get_root_path())
        elif poster.startswith('/'):
            print('uploading image from local')
            self.client.upload_image(item_id, poster)
        # if the poster is a MediaPoster object, process the image
        elif isinstance(poster, MediaPoster):
            print('uploading image from MediaPoster')
            # create image from MediaPoster
            poster = MediaPosterImageCreator(poster)
            poster = poster.create()
            poster_location = f'{self.config.get_root_path()}/poster.png'
            poster.save(poster_location)
            self.client.upload_image(item_id, poster_location)
