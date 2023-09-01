import uuid
from dataclasses import asdict
from datetime import datetime
from typing import Dict, List
from plexapi.library import LibrarySection
from plexapi.server import PlexServer
from plexapi.video import Movie, Show
import re

from src.models import MediaList, MediaListItem, MediaType, MediaListType, MediaItem, MediaProviderIds


class PlexSearcher:
    def __init__(self, config):
        self.plex = config.get_client('plex')
        # Consider having invalid_keys and key_mapping as class variables if they are constant.
        # Else, you can set them in __init__ based on some config or dynamically.
        self.invalid_keys = ['filtersId', 'clientId', 'filterType']  # Update this with actual invalid keys.
        self.key_mapping = {
            'offset': 'container_start',
            'limit': 'maxresults',
            'type': 'libtype',
            # Add other key mappings if required.
        }

    @staticmethod
    def to_snake_case(string):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def remove_invalid_keys(self, filters: Dict[str, str]):
        for key in self.invalid_keys:
            filters.pop(key, None)
        return filters

    def parse_filters(self, filters):
        parsed_filters = {}

        filters = filters.dict()
        filters = self.remove_invalid_keys(filters)

        for key, value in filters.items():
            # Remove invalid keys
            # Rename keys if needed
            new_key = self.key_mapping.get(key, key)
            # Convert camelCase to snake_case
            new_key = self.to_snake_case(new_key)
            parsed_filters[new_key] = value
        return parsed_filters

    def search_libraries(self, filters):
        # print('searching libraries', filters)
        parsed_filters = self.parse_filters(filters)

        parsed_filters = {k: v for k, v in parsed_filters.items() if v is not None}
        print('parsed filters', parsed_filters)
        # Define a set of valid filter fields for the Plex API
        valid_filters = {
            'title', 'studio', 'genre', 'contentRating', 'decade',
            'genre', 'actor', 'country', 'studio', 'actor', 'libtype'
            'director', 'resolution', 'producer', 'actor', 'country',
            'addedAt', 'sort', 'year','maxresults','libtype'
        }
        # Remove any keys not in valid_filters
        parsed_filters = {k: v for k, v in parsed_filters.items() if k in valid_filters}
        print('valid filters', parsed_filters)

        if('sort' not in parsed_filters):
            parsed_filters['sort'] = 'titleSort:asc'


        if 'maxresults' not in parsed_filters or parsed_filters['maxresults'] is None:
            parsed_filters['maxresults'] = 100  # Set a default value if you want

        combined_results = []

        libraries: List[LibrarySection] = self.plex.library.sections()
        for library in libraries:
            try:
                print('searching library', library.title)
                search_results = library.search(**parsed_filters)
                combined_results.extend(search_results)
                print('added results', len(search_results))
            except Exception as e:
                print('error searching library', e)
                continue

        return combined_results

    def search_lists(self, listId, type):
        try:
            if type == MediaListType.COLLECTION:
                # print('searching collection', listId)
                return self.plex.fetchItem(int(listId))
            elif type == MediaListType.PLAYLIST:
                return self.plex.playlist(title=listId)
        except Exception as e:
            print('not item found',e)
            print(f"Type: {type(e).__name__}")
            print(f"Arguments: {e.args}")
            return None

    def search_list_items(self, media, type):
        # print('search list items', media, type)
        if type == MediaListType.COLLECTION:
            if media:
                if hasattr(media, 'children'):
                    # print('has children', media.children)
                    return media.children
        elif type == MediaListType.PLAYLIST:
            if media:
                return media.items()
        return []

class PlexProvider:
    def __init__(self, config, media_list=None):
        self.config = config
        self.client: PlexServer = config.get_client('plex')  # Retrieve the Plex client
        self.media_list = media_list
        self.filters = media_list.filters if media_list else {}
        self.list_type = self.media_list.type if self.media_list else MediaListType.COLLECTION

    async def get_list(self):
        plex_search = PlexSearcher(self.config)
        list = None

        # print(self.filters)
        # The logic to retrieve the list and list items from Plex.
        # This might be different from MDB, so adjust accordingly.
        if self.filters.listId:
            print('searching list', self.filters.listId, self.list_type)
            list = plex_search.search_lists(self.filters.listId, self.list_type)  # Assume your Plex client has a method called getList

            if list is None:
                print('ERROR: list didnt return anything')
                return None

            list_items = plex_search.search_list_items(list, self.list_type)
        else:
            list_items = plex_search.search_libraries(self.filters)

        db = self.config.get_db()

        if list is not None:
            # print(dir(list))
            self.media_list.name = list.title
            self.media_list.type = self.list_type
            self.media_list.sortName = list.titleSort
            self.media_list.description = list.summary
        else:
            self.media_list.name = self.media_list.name
            self.media_list.type = self.list_type or self.filters.listType
            self.media_list.sortName = self.media_list.sortName
            self.media_list.description = self.media_list.description

        self.media_list.creatorId = self.config.get_user().userId
        self.media_list.createdAt = datetime.now()

        db.media_lists.insert_one(self.media_list.dict())
        print(self.media_list)

        for item in list_items:
            # print('-------------', dir(item))
            self.media_list.items.append(await self.create_media_item(item, self.media_list))
            # Adjust the logic based on how Plex's client class methods and responses are structured.

        return self.media_list

    def _extract_external_ids(self, movie: Movie):
        ids = {}

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

        # print('ITEM ==============', item)
        # poster_id = item['ImageTags'].get('Primary')
        # poster_url = f"{self.server_url}/emby/Items/{item['Id']}/Images/Primary?api_key={self.api_key}&X-Emby-Token={self.api_key}" if poster_id else None

        poster_url = item.thumbUrl if item.thumbUrl else None
        # print('poster url', poster_url)

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
            sourceId=item.ratingKey,
            dateAdded=datetime.now()
        )

        db.media_list_items.insert_one(media_list_item.dict())

        media_list_item.item = media_item

        return media_item
