import uuid
from datetime import datetime

from src.models import MediaList, MediaListItem, MediaType, MediaListType


class EmbyProvider:
    def __init__(self, config, filters=None, listType=MediaListType.COLLECTION):
        self.config = config
        self.client = config.get_client('emby')  # Retrieve the Emby client
        self.filters = filters
        self.server_url = self.client.server_url
        self.api_key = self.client.api_key
        self.listType = listType

        if filters is not None:
            self.id, self.library_name = self.parse_filters(filters)


    def parse_filters(self, filters):
        id_filter = next((f for f in filters if f['name'] == 'id'), None)
        library_filter = next((f for f in filters if f['name'] == 'library'), None)

        id_value = id_filter.get('value', None) if id_filter else None
        library_name = library_filter.get('value', None) if library_filter else None

        return id_value, library_name
    def get_list(self):
        if self.id is None and self.library_name is None:
            print('No filter provided. Cannot get list.')
            return None

        elif(self.library_name is not None):
            self.id = self.client.get_library(self.library_name)

        if(self.id is not None):
            list_items, list_items_count = self.client.get_items_from_parent(self.id)

        list = self.client.get_list(list_id=self.id)
        print('LIST:', list)

        # print('LIST ITEMS:', list_items)
        db = self.config.get_db()
        media_list = MediaList(
            mediaListId=str(uuid.uuid4()),
            name=list['Name'],
            type=self.listType,
            sortName=list['SortName'],
            clientId='EMBYLIST',
            createdAt=datetime.now(),
            creatorId="APPUSERID"
        )

        db.media_lists.insert_one(media_list.dict())
        print(media_list)

        primary_list = []

        for item in list_items:
            print('-------------', item)

            poster_id = item['ImageTags'].get('Primary')
            if poster_id:
                # TODO: think about implementing a more reliable poster option
                # if emby is down or off your posters are down.
                poster_url = f"{self.server_url}/emby/Items/{item['Id']}/Images/Primary?api_key={self.api_key}&X-Emby-Token={self.api_key}"
            else:
                poster_url = None

            media_list_item = MediaListItem(
                mediaItemId=str(uuid.uuid4()),
                mediaListId=media_list.mediaListId,
                sourceId=item['Id'],
                name=item['Name'],
                type=MediaType.MOVIE if item['Type'] == 'Movie' else MediaType.SHOW,
                year=item.get('ProductionYear'),
                dateAdded=datetime.now(),
                imdbId=item['ProviderIds'].get('IMDB'),
                tvdbId=item['ProviderIds'].get('Tvdb'),
                poster=poster_url  # Set the full poster URL
            )

            db.media_list_items.insert_one(media_list_item.dict())

            # Adjust the logic below based on how Emby's client class methods and responses are structured.
            try:
                emby_search = self.client.search_media(external_id='imdb.'+item['imdb_id'])
                if emby_search and emby_search[0]['Type'] != 'Trailer':
                    primary_list.append(emby_search[0])
                    continue
            except:
                print('not found-imdb')

            try:
                emby_search = self.client.search_media(external_id='tvdb.'+item['tvdb_id'])
                if emby_search and emby_search[0]['Type'] != 'Trailer':
                    primary_list.append(emby_search[0])
            except:
                print('not found-tvdb')

        return primary_list

