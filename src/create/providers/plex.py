import uuid
from datetime import datetime

from src.models.media_lists import MediaList, MediaListItem, MediaType, MediaListType


class PlexProvider:
    def __init__(self, config, filters=None):
        self.config = config
        self.client = config.get_client('plex')  # Retrieve the Plex client
        self.filters = filters

        if filters is not None:
            self.id = filters[0].get('value', None)

    def get_list(self):
        if self.id is None:
            print('No list id provided. Cannot get list.')
            return None

        # The logic to retrieve the list and list items from Plex.
        # This might be different from MDB, so adjust accordingly.
        list = self.client.getList(self.id)  # Assume your Plex client has a method called getList
        list_items = self.client.getListItems(self.id)  # Assume a method called getListItems

        db = self.config.get_db()

        media_list = MediaList(
            mediaListId=str(uuid.uuid4()),
            name=list['title'],  # Plex typically uses 'title' instead of 'name'
            type=MediaListType.COLLECTION,
            sortName=list['title'],
            clientId='PLEXLIST',
            creatorId="APPUSERID"
        )

        db.media_lists.insert_one(media_list.dict())
        print(media_list)

        primary_list = []

        for item in list_items:
            print('-------------', item)

            media_list_item = MediaListItem(
                mediaItemId=str(uuid.uuid4()),
                mediaListId=media_list.mediaListId,
                sourceId=item['ratingKey'],
                name=item['title'],
                type=MediaType.MOVIE if item['type'] == 'movie' else MediaType.SHOW,
                year=item.get('year', None),  # Plex provides the 'year' directly
                dateAdded=datetime.now(),
                imdbId=item.get('guid', None),  # 'guid' often contains external ids like imdb or tvdb
                # Plex may not have a direct 'tvdb_id', so you might need some parsing logic from 'guid'
                tvdbId=None
            )

            db.media_list_items.insert_one(media_list_item.dict())

            # Adjust the logic based on how Plex's client class methods and responses are structured.
            try:
                plex_search = self.client.searchMedia('imdb', item['guid'])
                if plex_search and not plex_search[0]['type'] == 'clip':  # 'clip' in Plex often represents trailers or extras
                    primary_list.append(plex_search[0])
                    continue
            except:
                print('not found-imdb')

            try:
                # If your Plex client can handle tvdb searches, this logic applies:
                plex_search = self.client.searchMedia('tvdb', item['guid'])
                if plex_search and not plex_search[0]['type'] == 'clip':
                    primary_list.append(plex_search[0])
            except:
                print('not found-tvdb')

        return primary_list
