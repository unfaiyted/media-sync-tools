import uuid
from datetime import datetime

from src.models import MediaList, MediaListItem, MediaType, MediaListType


class ListProviderResult:
    def __init__(self, id, name, description, movies):
        self.id = id
        self.name = name
        self.description = description
        self.movies = movies

class MdbProvider:

    def __init__(self, config, filters=None, listType=MediaListType.COLLECTION):
        self.config = config
        self.listType = listType
        self.client = config.get_client('mdb')
        self.filters = filters

        if filters is not None:
            self.id = filters[0].get('value', None)


    def get_list(self):
        if self.id is None:
            print('No list id provided. Cannot get list.')
            return None

        list = self.client.get_list_information(list_id=self.id)[0]
        list_items = self.client.get_list_items(list['id'])
        db = self.config.get_db()

        # print('LIST    sss',list)
        # print('List Items', list_items)

        media_list = MediaList(
            mediaListId=str(uuid.uuid4()),
            name=list['name'],
            type=MediaListType.COLLECTION,
            sortName=list['name'],
            clientId='MDBLIST',
            createdAt=datetime.now(),
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
                sourceId=item['id'],
                name=item['title'],
                # poster=item['poster'],
                type=MediaType.MOVIE if item['mediatype'] == 'movie' else MediaType.SHOW,
                year=item['release_year'],
                dateAdded=datetime.now(),
                imdbId=item['imdb_id'],
                tvdbId=item['tvdb_id']
            )

            db.media_list_items.insert_one(media_list_item.dict())

            try:
                # TODO: Replace with OmniClient
                emby_search = self.config.get_client('emby').get_media(external_id='imdb.'+item['imdb_id'])
                if emby_search[0]['Type'] == 'Trailer':
                    continue
                primary_list.append(emby_search[0])
                continue
            except:
                print('not found-imdb')

            try:
                emby_search = self.config.get_clients('emby').get_media(external_id='tvdb.'+item['tvdb_id'])
                if emby_search[0]['Type'] == 'Trailer':
                    continue
                primary_list.append(emby_search[0])
            except:
                print('not found-tvdb')
                #emby.get_media(external_id='tvdb.'+item['tvdb_id'])

        return primary_list
