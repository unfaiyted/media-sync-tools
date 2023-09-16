import random
from typing import Optional, Dict, Any

from PIL import Image
from io import BytesIO
import requests
from requests.exceptions import Timeout
from mimetypes import guess_type
import base64
import time

from src.models import JellyfinFilters
from src.models import MediaList
from src.models.media_lists import MediaItem, MediaListType


class JellyfinClient:
    def __init__(self, get_logger, server_url, username, api_key):
        self.server_url = server_url
        self.log = get_logger(__name__)

        self.log.debug('Initializing JellyfinClient')
        self.username = username
        self.api_key = api_key
        self.headers = {'X-Emby-Token': api_key}

        self.user = self.get_user_by_username(username)
        self.user_id = self.user['Id']

    def _build_url(self, path, params=None):
        url = f'{self.server_url}/emby/{path}?api_key={self.api_key}&X-Emby-Token={self.api_key}'
        if params:
            url += '&' + '&'.join(f'{key}={value}' for key, value in params.items())
        return url

    def _get_request_with_retry(self, url, retries=5, delay=1, stream=False):
        for attempt in range(retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=60, stream=stream)
                response.raise_for_status()  # Raise an exception for non-2xx status codes
                if stream is True:
                    return response
                else:
                    return response.json()
            except (Timeout, requests.exceptions.RequestException, requests.exceptions.ReadTimeout) as e:
                print(f"Request failed: {e}")
                if attempt < retries - 1:
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
        raise Exception(f"Failed to make the request after {retries} attempts.")

    def _post_request_with_retry(self, url, data=None, files=None, retries=5, delay=1):
        for attempt in range(retries):
            try:
                response = requests.post(url, data=data, files=files, headers=self.headers, timeout=60)
                response.raise_for_status()  # Raise an exception for non-2xx status codes
                return response
            except (Timeout, requests.exceptions.RequestException, requests.exceptions.ReadTimeout) as e:
                print(f"Request failed: {e}")
                if attempt < retries - 1:
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
        raise Exception(f"Failed to make the request after {retries} attempts.")

        # Modify your existing methods to use the new _get_request_with_retry and _post_request_with_retry methods

    def _delete_request_with_retry(self, url, data=None, files=None, retries=5, delay=1):
        for attempt in range(retries):
            try:
                response = requests.delete(url, data=data, files=files, headers=self.headers, timeout=60)
                response.raise_for_status()  # Raise an exception for non-2xx status codes
                return response
            except (Timeout, requests.exceptions.RequestException, requests.exceptions.ReadTimeout) as e:
                print(f"Request failed: {e}")
                if attempt < retries - 1:
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
        raise Exception(f"Failed to make the request after {retries} attempts.")

        # Modify your existing methods to use the new _get_request_with_retry and _post_request_with_retry methods

    def _get_request(self, url, stream=False, retries=5, delay=1):
        return self._get_request_with_retry(url, stream=stream, retries=retries, delay=delay)

    def _post_request(self, url, data=None, files=None):
        return self._post_request_with_retry(url, data=data, files=files)

    def _delete_request(self, url, data=None, files=None):
        return self._delete_request_with_retry(url, data=data, files=files)

    def create_collection(self, name, type, sort_name=None, poster=None):

        # Get the first items id of the correct type (so the collection is sorted right)
        initial_item_id = self.get_items_by_type(type, 1)[0]['Id']

        url = self._build_url('Collections', {'Name': name, 'Ids': initial_item_id, 'userId': self.user_id})
        response = self._post_request(url)
        collection = response.json()

        # TODO: Add sort name if other than None

        print(f"Created collection: {name} ({collection['Id']})")

        if sort_name:
            self.update_item_sort_name(collection['Id'], sort_name)

        # Remove the initial item from the collection,
        # since we don't want the item and I had errors trying
        # to create a collection without an initial item.

        try:
            self.delete_item_from_collection(collection['Id'], initial_item_id)
        except:
            print(f"Failed to remove initial item #{initial_item_id}  from collection")

        return collection

    def create_playlist(self, name, type, sort_name=None, poster=None):

        # Get the first items id of the correct type (so the collection is sorted right)
        initial_item_id = self.get_items_by_type(type, 1)[0]['Id']

        url = self._build_url('Playlists', {'Name': name, 'userId': self.user_id})
        response = self._post_request(url)
        playlist = response.json()

        print(f"Created playlist: {playlist['Name']} ({playlist['Id']})")

        return playlist

    def update_item_sort_name(self, item_id, sort_name):
        emby_watchlist_metadata = self.get_item_metadata(item_id)

        emby_watchlist_metadata['ForcedSortName'] = sort_name
        emby_watchlist_metadata['SortName'] = sort_name
        emby_watchlist_metadata['LockedFields'] = ['SortName']

        self.update_item_metadata(emby_watchlist_metadata)

    def get_collections(self):
        url = self._build_url(f'users/{self.user_id}/items',
                              {'Fields': 'ChildCount,RecursiveItemCount',
                               'Recursive': 'true',
                               'SortBy': 'SortName',
                               'SortOrder': 'Ascending',
                               'IncludeItemTypes': 'boxset'})
        response = self._get_request(url)
        return response.get('Items', [])

    def get_playlists(self):
        url = self._build_url(f'users/{self.user_id}/items',
                              {'Fields': 'ChildCount,RecursiveItemCount',
                               'Recursive': 'true',
                               'SortBy': 'SortName',
                               'SortOrder': 'Ascending',
                               'IncludeItemTypes': 'playlist'})
        response = self._get_request(url)
        return response.get('Items', [])

    def get_collection_by_name(self, name, item_type=None):
        collections = self.get_collections()

        if item_type is not None:
            return next((item for item in collections if item.get('Type') == name and item.get('Name') == name), None)
        return next((item for item in collections if item.get('Name') == name), None)

    def get_collection(self, collection_id):
        return self.get_list(collection_id)

    def get_list(self, list_id):
        url = self._build_url(f'users/{self.user_id}/items/{list_id}')
        response = self._get_request(url)
        return response

    def get_collection_items(self, collection_id):
        return self.get_list_items(collection_id)

    def get_items_from_parent(self, parent_id, image_type_limit=1,
                              fields='BasicSyncInfo,CanDelete,Container,PrimaryImageAspectRatio,ProductionYear,ExternalUrls,Status,EndDate,ProviderIds',
                              enable_total_record_count=True,
                              limit: int = 50, offset: int = 0):
        params = {
            'ParentId': parent_id,
            'ImageTypeLimit': image_type_limit,
            'Fields': fields,
            'IncludeItemTypes': 'Movie,Series,Season,Episode',
            'Recursive': 'true',
            'EnableTotalRecordCount': enable_total_record_count,
            'StartIndex': offset,
            'Limit': limit
        }

        url = self._build_url(f'Users/{self.user_id}/Items', params=params)
        response = self._get_request(url)
        items = response.get('Items', [])
        total_count = response.get('TotalRecordCount', 0)
        # print(items, total_count)
        return items, total_count

    def get_all_items_from_parent(self, parent_id, per_request_limit = 100) -> list:
        offset = 0
        all_list_items = []

        while True:
            list_items, list_items_count = self.get_items_from_parent(parent_id, limit=per_request_limit, offset=offset)
            self.log.info("Getting items from parent", offset=offset, list_items_count=list_items_count)
            all_list_items.extend(list_items)
            offset += per_request_limit
            if offset > list_items_count:
                self.log.debug("Reached end of Jellyfin list items", offset=offset, list_items_count=list_items_count)
                break

        return all_list_items

    def get_libraries(self):
        url = self._build_url(f'Users/{self.user_id}/views')
        response = self._get_request(url)
        return response.get('Items', [])

    def get_library(self, library_id):
        libraries = self.get_libraries()
        library = next((item for item in libraries if item.get('Id') == library_id), None)
        return library

    def get_items_from_library(self, library_name):
        libraries = self.get_libraries()
        library = next((item for item in libraries if item.get('Name') == library_name), None)
        if library:
            return self.get_items_from_parent(library['Id'])
        return None, 0

    def get_list_items(self, list_id):
        url = self._build_url(f'users/{self.user_id}/items/{list_id}/children')
        response = self._get_request(url)
        items = response.get('Items', [])
        total_count = response.get('TotalRecordCount', 0)
        print(items, total_count)
        return items, total_count

    def get_seasons(self, series_id):
        print(f"Getting seasons for series {series_id}")
        url = self._build_url(f'Shows/{series_id}/Seasons')
        response = self._get_request(url)
        return response.get('Items', [])

    def get_episodes(self, series_id, season_id):
        print(f"Getting episodes for series {series_id} season {season_id}")
        url = self._build_url(f'Shows/{series_id}/Episodes', {'SeasonId': season_id})
        response = self._get_request(url)
        return response.get('Items', [])

    def does_collection_exist(self, collection_name):
        collections = self.get_collections()
        for collection in collections:
            if collection.get('Name') == collection_name:
                return True
        return False

    def get_collection_poster(self, collection_id):
        url = self._build_url(f'Items/{collection_id}/Images/Primary')
        response = requests.get(url, headers=self.headers)
        return response

    def add_item_to_collection(self, collection_id, item_id):
        url = self._build_url(f'Collections/{collection_id}/Items', {'Ids': item_id})
        response = self._post_request(url)
        return response

    def add_item_to_playlist(self, playlist_id, item_id):
        url = self._build_url(f'Playlists/{playlist_id}/Items', {'Ids': item_id})
        response = self._post_request(url)
        return response

    def delete_item_from_collection(self, collection_id, item_id):
        url = self._build_url(f'Collections/{collection_id}/Items', {'Ids': item_id})
        response = self._delete_request(url)
        return response

    def delete_item_from_playlist(self, playlist_id, item_id):
        url = self._build_url(f'Playlists/{playlist_id}/Items/Delete', {'Ids': item_id})
        response = self._post_request(url)
        return response

    def get_item_image(self, item_id):
        url = self._build_url(f'Items/{item_id}/Images/Primary')
        print(url)
        response = self._get_request(url, stream=True, retries=1)

        if response.status_code == 200:
            # Assuming _get_request is using the requests library.
            # Use BytesIO to convert the response content into a file-like object so it can be opened by PIL
            img = Image.open(BytesIO(response.content)).convert('RGBA')
            return img
        else:
            raise Exception(f"Failed to fetch the image for collection {item_id}. Status code: {response.status_code}")

    def delete_collection(self, collection_id):
        return self.delete_item(collection_id)

    def delete_playlist(self, playlist_id):
        return self.delete_item(playlist_id)

    def delete_item(self, item_id):
        url = self._build_url(f'Items/{item_id}/Delete')
        response = self._post_request(url)
        return response

    def delete_all_collections(self):
        collections = self.get_collections()
        for collection in collections:
            # Skip this ALWAYS
            # TODO: implement some sort of "skip" list
            if (collection.get('Name') == 'Watchlist'):
                continue

            print(f"Deleting collection {collection.get('Name')} ({collection.get('Id')})")
            self.delete_collection(collection.get('Id'))
        return

    def delete_collection_by_name(self, collection_name):
        collection = self.get_collection_by_name(collection_name)
        if collection:
            self.delete_item(collection.get('Id'))
        return

    def add_search_results_to_collection(self, collection_id, results):
        for item in results.get('Items', []):
            item_id = item.get('Id')
            print(f"Found {item.get('Name')} with id {item_id}")
            self.add_item_to_collection(collection_id, item_id)
            print(f"Added {item.get('Name')} to {collection_id}")

    def delete_search_results_from_collection(self, collection_id, results):
        for item in results.get('Items', []):
            item_id = item.get('Id')
            print(f"Found {item.get('Name')} with id {item_id}")
            self.delete_item_from_collection(collection_id, item_id)
            print(f"Removed {item.get('Name')} from {collection_id}")

    def get_items_by_type(self, item_types='Series', limit=50):
        url = self._build_url(f'Users/{self.user_id}/Items',
                              {'SortBy': 'SortName',
                               'SortOrder': 'Ascending',
                               'IncludeItemTypes': item_types,
                               'Recursive': 'true',
                               'Fields': 'BasicSyncInfo,CanDelete,Container,PrimaryImageAspectRatio,Prefix',
                               'StartIndex': '0',
                               'EnableImageTypes': 'Primary,Backdrop,Thumb',
                               'ImageTypeLimit': '1',
                               'Limit': limit})
        response = self._get_request_with_retry(url)
        return response.get('Items', [])

    def get_items_in_collection(self, collection_id):
        url = self._build_url(f'users/{self.user_id}/items', {'Parentid': collection_id})
        response = self._get_request(url)
        items = response.get('Items', [])
        return items, len(items)

    def get_all_trailers(self):
        """
        Retrieves all trailers from the Jellyfin collection.
        """
        item_type = 'Trailer'
        url = self._build_url(f'Users/{self.user_id}/Items',
                              {
                                  'IncludeItemTypes': item_type,
                                  'Recursive': 'true',
                                  'Fields': 'Title,Year,Type,Description'
                              })
        response = self._get_request(url)
        return response.get('Items', [])

    # def get_all_trailers(self):
    #     url = self._build_url(f'Users/{self.user_id}/Items', {'IncludeItemTypes': 'Trailer'})
    #     response = self._get_request(url)
    #     return response.get('Items', [])

    def upload_image(self, id, image_path, imgType='Primary'):
        mime_type = guess_type(image_path)[0]
        with open(image_path, 'rb') as f:
            image_data = f.read()
        encoded_image_data = base64.b64encode(image_data)
        headers = {'Content-Type': mime_type}
        print('Uploading collection image: ', image_path, mime_type)
        url = self._build_url(f'Items/{id}/Images/{imgType}')
        response = requests.post(url, data=encoded_image_data, headers=headers)
        return response

    def get_item_metadata(self, item_id):
        url = self._build_url(f'Users/{self.user_id}/Items/{item_id}', {'Fields': 'ChannelMappingInfo'})
        response = self._get_request(url)
        return response

    def update_item_metadata(self, metadata):
        url = self._build_url(f'Items/{metadata["Id"]}')
        response = requests.post(url, json=metadata)
        return response.text

    def get_user_by_username(self, username):
        users = self.get_users()
        # print('users', users)
        print(type(self.log))
        self.log.debug('Got users.', users=users)
        return next((user for user in users if user.get('Name') == username), None)

    def set_favorite(self, item_id):
        url = self._build_url(f'Users/{self.user_id}/FavoriteItems/{item_id}')
        response = self._post_request(url)
        return response

    def get_users(self):
        url = self._build_url(f'Users')
        response = self._get_request(url)
        return response

    def search(self, query, item_type):
        url = self._build_url(f'Users/{self.user_id}/Items',
                              {'SortBy': 'SortName',
                               'SortOrder': 'Ascending',
                               'IncludeItemTypes': item_type,
                               'Fields': 'BasicSyncInfo,CanDelete,Container,PrimaryImageAspectRatio,ProductionYear,Status,EndDate',
                               'StartIndex': '0',
                               'EnableImageTypes': 'Primary,Backdrop,Thumb',
                               'ImageTypeLimit': '1',
                               'Recursive': 'true',
                               'SearchTerm': query,
                               'Limit': '50',
                               'IncludeSearchTypes': 'false'})
        response = self._get_request(url)
        return response.get('Items', [])

    @staticmethod
    def build_query_parameters(filter_data: JellyfinFilters) -> Dict[str, Any]:
        filter_dict = filter_data.dict(exclude_none=True)

        # Remap keys as necessary
        remapped_keys = {
            'search': 'SearchTerm',
            'limit': 'Limit',
            'listId': 'ParentId',
            'offset': 'StartIndex',
            # ... add other remapped keys here ...
        }

        for key, new_key in remapped_keys.items():
            if key in filter_dict:
                filter_dict[new_key] = filter_dict.pop(key)

        # Special handling for Filters
        filters_list = []

        if 'isPlayed' in filter_dict:
            filters_list.append('IsUnplayed' if not filter_dict['isPlayed'] else 'IsPlayed')
            del filter_dict['isPlayed']

        if 'isFavorite' in filter_dict and filter_dict['isFavorite']:
            filters_list.append('IsFavorite')
            del filter_dict['isFavorite']

        if filters_list:
            filter_dict['Filters'] = ','.join(filters_list)

        # Capitalizing the first letter of each key in the dictionary
        filter_dict = {key.capitalize(): value for key, value in filter_dict.items()}

        return filter_dict

    def filter_search(self, filters: JellyfinFilters) -> Dict[str, Any]:
        # Building the request URL
        url = self._build_url(f'Users/{self.user_id}/Items', self.build_query_parameters(filters))

        response = self._get_request(url)
        return response.get('Items', [])

    def get_sessions(self):
        url = self._build_url(f'Sessions')
        response = self._get_request(url)
        return response

    def play_item(self, session_id, item_id):
        url = self._build_url(f'Sessions/{session_id}/Playing', {'ItemIds': item_id, 'PlayCommand': 'PlayNow'})
        response = self._post_request(url)
        return response

    def send_message(self, session_id, message):
        url = self._build_url(f'Sessions/{session_id}/Message', {'Text': message})
        response = self._post_request(url)
        return response

    def get_movies(self, limit=50, is_played=None, is_favorite=None):
        return self.get_media(limit, "Movie", is_played, is_favorite)

    def get_media(self, limit=50, item_types="Movie", genre=None, is_played=None, is_favorite=None,
                  external_id=None, name=None, year=None):

        params = {'Recursive': 'true', 'IncludeItemTypes': item_types, "Limit": limit}

        if is_played is not None:
            params['IsPlayed'] = str(is_played)
        if is_favorite is not None:
            params['IsFavorite'] = str(is_favorite)
        if genre is not None:
            params['Genres'] = genre
        if external_id is not None:
            params['AnyProviderIdEquals'] = external_id
        if name is not None:
            params['Name'] = name
        if year is not None:
            params['ProductionYear'] = str(year)

        url = self._build_url(f'Users/{self.user_id}/Items', params)
        response = self._get_request(url)
        items = response.get('Items', [])
        random.shuffle(items)
        return items[:limit]

    def get_liked_movies(self, limit=50):
        return self.get_movies(limit, is_favorite=True)

    def get_unwatched_movies(self, limit=50):
        return self.get_movies(limit, is_played=False)

    def get_watched_series(self, limit=50):
        return self.get_media(limit, "Series", is_played=True)

    def get_movies_by_genre(self, limit=50, genre="Action"):
        return self.get_media(limit, "Movie", genre=genre)

    ####
    # MediaList based Methods
    ####

    def search_for_external_ids(self, media_item: MediaItem) -> Optional[dict]:
        item = None

        def search_id(external_id: str) -> Optional[dict]:
            try:
                search_results = self.get_media(external_id=external_id)
                if search_results and search_results[0]['Type'] != 'Trailer':
                    return search_results[0]
            except Exception as e:
                print(f"Failed searching for {external_id} due to {e}")
            return None

        try:
            imdb_result = search_id(f"imdb.{media_item.providers.imdbId}")
            tvdb_result = search_id(f"tvdb.{media_item.providers.tvdbId}")
        except Exception as e:
            print(f"Failed searching for {media_item} due to {e}")
            return None

        if imdb_result:
            item = imdb_result
        elif tvdb_result:
            item = tvdb_result
        return item

    def create_collection_from_list(self, media_list: MediaList):
        collection = self.create_collection(media_list.name, media_list.type, media_list.sortName)
        # search emby for the items
        # add the first result to the collection

        print('-------------', media_list.items)
        for item in media_list.items:
            print('-------------', item)
            media_item = self.search_for_external_ids(item)
            if media_item:
                self.add_item_to_collection(collection['Id'], media_item['Id'])
        return collection

    def delete_collection_items(self, collection_id):
        items = self.get_collection_items(collection_id)
        for item in items:
            self.delete_item_from_collection(collection_id, item['Id'])
        return

    def update_collection_from_list(self, media_list: MediaList):
        collection = self.get_list(media_list.sourceListId)
        if collection:
            self.delete_collection_items(collection['Id'])
        return self.create_collection_from_list(media_list)

    def create_playlist_from_list(self, media_list: MediaList):
        playlist = self.create_playlist(media_list.name, media_list.type, media_list.sortName)
        # search emby for the items
        # add the first result to the collection

        for item in media_list.items:
            print('-------------', item)
            emby_media_item = self.search_for_external_ids(item)
            if emby_media_item:
                self.add_item_to_playlist(playlist['Id'], emby_media_item['Id'])
        return playlist

    def update_playlist_from_list(self, media_list: MediaList):
        playlist = self.get_list(media_list.sourceListId)
        if playlist:
            self.delete_collection_items(playlist['Id'])
        return self.create_playlist_from_list(media_list)

    def upload_image_from_url(self, sourceListId, poster, root_path):
        if poster is None:
            self.log.info('no poster provided', sourceListId=sourceListId)
            return None

        # if the media_list.poster is a url, download the image and upload it to the provider

        self.log.debug('downloading image from url', sourceListId=sourceListId, poster=poster)
        response = requests.get(poster, stream=True)
        if response.status_code == 200:
            # Assuming _get_request is using the requests library.
            # Use BytesIO to convert the response content into a file-like object so it can be opened by PIL
            img = Image.open(BytesIO(response.content)).convert('RGBA')

            poster_location = f'{root_path}/poster.png'
            img.save(poster_location, quality=95)
            self.upload_image(sourceListId, poster_location)

    def search_media_item_by_external_ids(self, media_item=None) -> dict or None:

        if media_item is None:
            self.log.info('no media item provided')
            return None

        match = None

        def search_id(external_id: str) -> Optional[dict]:
            try:
                search_results = self.get_media(external_id=external_id)
                if search_results and search_results[0]['Type'] != 'Trailer':
                    return search_results[0]
                if search_results and search_results[0]['Type'] == 'Trailer':
                    return search_results[1]

            except Exception as e:
                self.log.error(f"Failed searching for {external_id} due to {e}", external_id=external_id, media_item=media_item, error=e)
            return None

        imdb_result = search_id(f"imdb.{media_item.providers.imdbId}")
        tvdb_result = search_id(f"tvdb.{media_item.providers.tvdbId}")
        tmdb_result = search_id(f"Tmdb.{media_item.providers.tmdbId}")

        if imdb_result:
            return imdb_result
        elif tvdb_result:
            return tvdb_result
        elif tmdb_result:
            return tmdb_result

        emby_type = 'Movie' if media_item.type == MediaType.MOVIE else 'Series'
        # Fallback to name and year
        search_results = self.search(media_item.item.title, emby_type)
        if search_results:
            for result in search_results:
                if int(result['ProductionYear']) == int(media_item.item.year):
                    match = result
                    break
            return match
        return match

    async def get_poster_from_emby_by_media_item(self, media_item):
        jellyfin_item = await self.search_media_item_by_external_ids(media_item=media_item)

        if jellyfin_item is None:
            self.log.info('Item not found in Emby')
            return None

        if poster_id := jellyfin_item['ImageTags'].get('Primary'):
            self.log.debug(f"Found poster id {poster_id} for {media_item.item.title}", poster_id=poster_id, media_item=media_item)
            return f"{self.server_url}/emby/Items/{jellyfin_item['Id']}/Images/Primary?api_key={self.api_key}&X-Emby-Token={self.api_key}"
        else:
            return None

