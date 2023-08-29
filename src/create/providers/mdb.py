import uuid
from datetime import datetime

from src.models import MediaList, MediaListItem, MediaType, MediaListType, MediaItem, MediaProviderIds


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


    async def get_list(self):
        if self.id is None:
            print('No list id provided. Cannot get list.')
            return None

        list = self.client.get_list_information(list_id=self.id)[0]
        list_items = self.client.get_list_items(list['id'])
        db = self.config.get_db()

        media_list = MediaList(
            mediaListId=str(uuid.uuid4()),
            name=list['name'],
            type=self.listType,
            sortName=list['name'],
            clientId='MDBCLIENTID',
            createdAt=datetime.now(),
            creatorId=self.config.get_user().userId
        )

        db.media_lists.insert_one(media_list.dict())
        print(media_list)

        primary_list = []

        for item in list_items:
            print('-------------', item)

            # poster_id = item['ImageTags'].get('Primary')
            # poster_url = f"{self.server_url}/emby/Items/{item['Id']}/Images/Primary?api_key={self.api_key}&X-Emby-Token={self.api_key}" if poster_id else None
            poster_url = f'https://image.tmdb.org/t/p/w500/{item["poster_path"]}'
            media_item = MediaItem(
                mediaItemId=str(uuid.uuid4()),
                name=item['title'],
                title=item.get('Name','TITLE MISSING'),
                year=item['release_year'],
                type=MediaType.MOVIE if item['mediatype'] == 'movie' else MediaType.SHOW,
                poster=poster_url,
                providers=MediaProviderIds(
                    imdbId=item['imdb_id'],
                    tvdbId=item['tvdb_id']
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

                db.media_items.update_one(
                    {"mediaItemId": existing_media_item["mediaItemId"]},
                    {"$set": media_item.dict()}
                )
            # media_item.dict()
            else:
                print('inserting new media item')
                db.media_items.insert_one(media_item.dict())

                media_list_item = MediaListItem(
                    mediaItemId=str(uuid.uuid4()),
                    mediaListId=media_list.mediaListId,
                    sourceId=item['id'],
                    dateAdded=datetime.now(),
                )

                db.media_list_items.insert_one(media_list_item.dict())
            primary_list.append(media_item.dict())

        return primary_list

    async def upload_list(self, media_list: MediaList):
       # TODO: implement
         pass
