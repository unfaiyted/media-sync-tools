import uuid
from datetime import datetime

from plexapi.server import PlexServer
from plexapi.video import Movie, Show

from src.models import MediaList, MediaListItem, MediaType, MediaListType, MediaItem, MediaProviderIds


class PlexProvider:
    def __init__(self, config, filters=None, listType=MediaListType.COLLECTION):
        self.config = config
        self.client: PlexServer = config.get_client('plex')  # Retrieve the Plex client
        self.filters = filters

        self.id, self.library_name, self.list_type = (
            self.parse_filters(filters if filters is not None else []))
        if filters is not None:
            self.id = filters[0].get('value', None)

    @staticmethod
    def parse_filters(filters):
        id_value = None
        library_value = None
        list_type_value = None

        for f in filters:
            try:
                if f['type'] == 'list_id': # rating_key in plex
                    id_value = f.get('value')
                elif f['type'] == 'library':
                    library_value = f.get('value')
                elif f['type'] == 'list_type':
                    list_type_value = f.get('value')
            except KeyError:
                print(f"Key 'name' missing in filter: {f}")

        return id_value, library_value, list_type_value


    def _get_media_by_id(self, id):
        try:
            if self.list_type == MediaListType.COLLECTION:
                return self.client.fetchItem(id)
            elif self.list_type == MediaListType.PLAYLIST:
                return self.client.playlist(title=id)
        except:
            print('not item found')
            return None

    def _get_list_items(self, media):
        if self.list_type == MediaListType.COLLECTION:
            if media:
                if hasattr(media, 'children'):
                    print('has children', media.children)
                    return media.children
        elif self.list_type == MediaListType.PLAYLIST:
            if media:
                    return media.items()
        return []


    async def get_list(self):
        if self.id is None or self.list_type is None:
            print('No list id or type provided. Cannot get list.')
            return None

        # The logic to retrieve the list and list items from Plex.
        # This might be different from MDB, so adjust accordingly.
        list = self._get_media_by_id(self.id)  # Assume your Plex client has a method called getList

        list_items = self._get_list_items(list)


        db = self.config.get_db()

        media_list = MediaList(
            mediaListId=str(uuid.uuid4()),
            name=list.title,  # Plex typically uses 'title' instead of 'name'
            type=self.list_type,
            sortName=list.title,
            description=list.summary,
            clientId='PLEXCLIENTID',
            items=[],
            creatorId=self.config.get_user().userId,
            createdAt=datetime.now(),

        )

        db.media_lists.insert_one(media_list.dict())
        print(media_list)


        for item in list_items:
            print('-------------', dir(item))
            media_list.items.append(await self.create_media_item(item, media_list))
            # Adjust the logic based on how Plex's client class methods and responses are structured.


        return media_list

    def _extract_external_ids(self, movie: Movie):
        ids = {}

        print('[[movie guid]]', movie.guid)

        if not movie.guid:
            return ids

        # Check for IMDb
        if "imdb://" in movie.guid:
            ids['imdb'] = movie.guid.split('imdb://')[1].split('?')[0]

        # Check for TheMovieDB
        if "themoviedb://" in movie.guid:
            ids['tmdb'] = movie.guid.split('themoviedb://')[1].split('?')[0]

        # You can continue adding checks for other ID types in a similar manner...
    # Check for TVDB
        if "thetvdb://" in movie.guid:
            ids['tvdb'] = movie.guid.split('thetvdb://')[1].split('?')[0]

        return ids



    async def create_media_item(self, item: Movie or Show, media_list):
        db = self.config.get_db()

        external_ids = self._extract_external_ids(item)


        print('ITEM ==============', item)
        # poster_id = item['ImageTags'].get('Primary')
        # poster_url = f"{self.server_url}/emby/Items/{item['Id']}/Images/Primary?api_key={self.api_key}&X-Emby-Token={self.api_key}" if poster_id else None

        poster_url = item.thumbUrl if item.thumbUrl else None
        print('poster url', poster_url)

        media_item = MediaItem(
            mediaItemId=str(uuid.uuid4()),
            title=item.title,
            year=item.year,
            type=MediaType.MOVIE if item.TYPE == 'movie' else MediaType.SHOW,
            poster=poster_url,
            providers=MediaProviderIds(
                imdbId=external_ids.get('imdb', None),
                tvdbId=external_ids.get('tvdb', None),
                tmdbId=external_ids.get('tmdb', None),
            ),
            # ... add any other fields you need here ...
        )


           # # media_list_item = MediaListItem(
           #      mediaItemId=str(uuid.uuid4()),
           #      mediaListId=media_list.mediaListId,
           #      sourceId=item['ratingKey'],
           #      name=item['title'],
           #      type=MediaType.MOVIE if item['type'] == 'movie' else MediaType.SHOW,
           #      year=item.get('year', None),  # Plex provides the 'year' directly
           #      dateAdded=datetime.now(),
           #      imdbId=item.get('guid', None),  # 'guid' often contains external ids like imdb or tvdb
           #      # Plex may not have a direct 'tvdb_id', so you might need some parsing logic from 'guid'
           #      tvdbId=None

          #  db.media_list_items.insert_one(media_list_item.dict())

        # Check for existing mediaItem
        existing_media_item = None
        if media_item.providers.imdbId:
            existing_media_item = await db.media_items.find_one({"providers.imdbId": media_item.providers.imdbId})
        elif media_item.providers.tvdbId:
            existing_media_item = await db.media_items.find_one({"providers.tvdbId": media_item.providers.tvdbId})
        elif media_item.title and media_item.year:
            existing_media_item = await db.media_items.find_one({"title": media_item.title, "year": media_item.year})


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
            sourceId=item.ratingKey,
            dateAdded=datetime.now()
        )

        db.media_list_items.insert_one(media_list_item.dict())

        media_list_item.item = media_item

        return media_item
