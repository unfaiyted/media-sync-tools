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
            self.id = filters[0].get('value', None)

    def get_list(self):
        if self.id is None:
            print('No list id provided. Cannot get list.')
            return None

        # The logic to retrieve the list and list items from Emby.
        # This might be different from MDB, so adjust accordingly.
        list = self.client.get_list(list_id=self.id)
        print('LIST:', list)
        list_items, list_items_count = self.client.get_items_from_parent(self.id)
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

