import uuid
from datetime import datetime

from src.models import MediaList, MediaListItem, MediaType, MediaListType, MediaItem, MediaProviderIds

from typing import Optional

class EmbyProvider:
    def __init__(self, config, filters=None, listType=MediaListType.COLLECTION):
        self.config = config
        self.client = config.get_client('emby')
        self.filters = filters
        self.server_url = self.client.server_url
        self.api_key = self.client.api_key
        self.listType = listType

        self.id, self.library_name = self.parse_filters(filters if filters is not None else [])
        print('id ',self.id)
        print('library name ',self.library_name)

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
            list_items, list_items_count = self.client.get_items_from_parent(self.id)

            list_ = self.client.get_list(list_id=self.id)  # Renamed to avoid conflict with built-in name 'list'
            # print('list ',list_)
            db = self.config.get_db()

            media_list = MediaList(
                mediaListId=str(uuid.uuid4()),
                name=list_['Name'],
                type=self.listType,
                sourceListId=list_['Id'],
                # filters=self.filters,
                sortName=list_['SortName'],
                clientId='EMBYCLIENTID',
                createdAt=datetime.now(),
                creatorId=self.config.get_user().userId
            )

            # print('media list ', media_list.dict())

            db.media_lists.insert_one(media_list.dict())

            primary_list = []

            for item in list_items:
                print('-------------', item)
                # primary_list.extend(self.search_emby_for_external_ids(item))

                # media_item = await self.create_media_item(item, media_list)


                # Adding to primary list or any other processing you need to do
                # ...

            return primary_list
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
            title=item['Name'],
            year=item.get('ProductionYear'),
            type=MediaType.MOVIE if item['Type'] == 'Movie' else MediaType.SHOW,
            poster=poster_url,
            providers=MediaProviderIds(
                imdbId=item['ProviderIds'].get('IMDB'),
                tvdbId=item['ProviderIds'].get('Tvdb')
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
            # Update missing fields
            for field, value in media_item.dict().items():
                if value and not existing_media_item.get(field):
                    existing_media_item[field] = value
            db.media_items.update_one(
                {"_id": existing_media_item["_id"]},
                {"$set": existing_media_item}
            )
        else:
            db.media_items.insert_one(media_item.dict())

        media_list_item = MediaListItem(
            mediaListItemId=str(uuid.uuid4()),
            mediaListId=media_list.mediaListId,
            mediaItemId=media_item.mediaItemId,
            sourceId=item['Id'],
            dateAdded=datetime.now()
        )

        db.media_list_items.insert_one(media_list_item.dict())

        return media_item

    def search_emby_for_external_ids(self, media_item: MediaItem) -> list:
        primary_list = []

        def search_id(external_id: str) -> Optional[dict]:
            try:
                search_results = self.client.search_media(external_id=external_id)
                if search_results and search_results[0]['Type'] != 'Trailer':
                    return search_results[0]
            except Exception as e:
                print(f"Failed searching for {external_id} due to {e}")
            return None

        imdb_result = search_id(f"imdb.{media_item.providers.imdbId}")
        tvdb_result = search_id(f"tvdb.{media_item.providers.tvdbId}")

        if imdb_result:
            primary_list.append(imdb_result)
        if tvdb_result:
            primary_list.append(tvdb_result)

        return primary_list
