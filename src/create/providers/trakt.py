import uuid
from datetime import datetime

from src.models import MediaListType, MediaList, MediaItem, MediaProviderIds, MediaType, MediaListItem


class TraktProvider:
    def __init__(self, config, filters=None, details = None, listType=MediaListType.COLLECTION):
        self.config = config
        self.listType = listType
        self.client = config.get_client('trakt')
        self.username = None
        self.details = details
        self.list_slug_or_id = None

        if filters:
            for filter_item in filters:
                if filter_item['type'] == 'username':
                    self.username = filter_item['value']
                elif filter_item['type'] in ['list_slug', 'list_id']:
                    self.list_slug_or_id = filter_item['value']

        # if not self.username or not self.list_slug_or_id:
        #     print("Both username and list_slug/list_id are required.")
            # Handle error or throw exception


    async def get_list(self):
        if self.list_slug_or_id is None:
            print('No list id provided. Cannot get list.')
            return None

        # list_info =  self.client.get_list(username=self.username, list_id_or_slug=self.list_slug_or_id)
        if self.username:
            list_items = self.client.get_list_items(username=self.username, list_id_or_slug=self.list_slug_or_id)
        else:
            list_items = self.client.get_list_items_by_id(list_id=self.list_slug_or_id)

        media_list = MediaList(
            mediaListId=str(uuid.uuid4()),
            name=self.details.title,
            type=self.listType,
            sourceListId=self.list_slug_or_id,
            # filters=self.filters,
            items=[],
            sortName=self.details.sort_title,
            clientId='TRAKTCLIENTID',
            createdAt=datetime.now(),
            creatorId=self.config.get_user().userId
        )

        print('-------------', media_list.dict())

        db = self.config.get_db()
        await db.media_lists.insert_one(media_list.dict())

        for item in list_items:
            # Assuming items contain these fields, you'll need to adjust based on Trakt API documentation
            # print('-------------', item['show']['ids'], item['show']['title'], item['show']['year'])
            print(item)
            print('------------')
            media_list.items.append(await self.create_media_item(item, media_list))

        return media_list


    async def create_media_item(self, provider_item, media_list):
        db = self.config.get_db()

        item = provider_item['show'] if 'show' in provider_item else provider_item['movie']
        # poster_id = item['ImageTags'].get('Primary')
        # poster_url = f"{self.server_url}/emby/Items/{item['Id']}/Images/Primary?api_key={self.api_key}&X-Emby-Token={self.api_key}" if poster_id else None

        print('ITEM = ', item)

        media_item = MediaItem(
                mediaItemId=str(uuid.uuid4()),
                title=item['title'],
                year=item['year'],
                type=MediaType.MOVIE if provider_item['type'] == 'movie' else MediaType.SHOW,
                # poster=poster_url,
                providers=MediaProviderIds(
                    imdbId=item['ids'].get('imdb', None),
                    tvdbId=item['ids'].get('tvdb', None),
                    traktId=item['ids'].get('trakt', None),
                    tmdbId=item['ids'].get('tmdb', None),
                    tvRageId=item['ids'].get('tvrage', None),
                ),
                # ... add any other fields you need here ...
            )

        # Check for existing mediaItem
        existing_media_item = None
        if media_item.providers.traktId:
            existing_media_item = await db.media_items.find_one({"providers.traktId": media_item.providers.traktId})
        elif media_item.providers.imdbId:
            existing_media_item = await db.media_items.find_one({"providers.imdbId": media_item.providers.imdbId})
        elif media_item.providers.tvdbId:
            existing_media_item = await db.media_items.find_one({"providers.tvdbId": media_item.providers.tvdbId})
        elif media_item.title and media_item.year:
            existing_media_item = await db.media_items.find_one({"title": media_item.title, "year": media_item.year})

        if existing_media_item:
                    print('updating existing media item')
                    media_item.mediaItemId = existing_media_item['mediaItemId']

                    # Filter out fields in the media item that are not valid
                    valid_fields = {k: v for k, v in media_item.dict().items() if v}

                    db.media_items.update_one(
                        {"mediaItemId": existing_media_item["mediaItemId"]},
                        {"$set": valid_fields}
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
            sourceId=item['ids']['trakt'],
            dateAdded=datetime.now()
        )

        db.media_list_items.insert_one(media_list_item.dict())

        media_list_item.item = media_item

        return media_item
