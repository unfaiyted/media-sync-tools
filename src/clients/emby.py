import requests
from requests.exceptions import Timeout
from mimetypes import guess_type
import base64
import time

from src.create.posters import PosterImageCreator


class Emby:
    def __init__(self, server_url, username, api_key):
        self.server_url = server_url
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

    def _get_request_with_retry(self, url, retries=5, delay=1):
        for attempt in range(retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=60)
                response.raise_for_status()  # Raise an exception for non-2xx status codes
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

    def _get_request(self, url):
        return self._get_request_with_retry(url)

    def _post_request(self, url, data=None, files=None):
        return self._post_request_with_retry(url, data=data, files=files)

    def create_collection(self, name, type, sort_name=None):

        # Get the first items id of the correct type (so the collection is sorted right)
        initial_item_id = self.get_items_by_type(type, 1)[0]['Id']

        url = self._build_url('Collections', {'Name': name, 'Ids': initial_item_id, 'userId': self.user_id})
        response = self._post_request(url)
        collection = response.json()

        # TODO: Add sort name if other than None

        print(f"Created collection: {collection['Name']} ({collection['Id']})")

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

    def update_item_sort_name(self, item_id, sort_name):
        emby_watchlist_metadata = self.get_item_metadata(item_id)

        emby_watchlist_metadata['ForcedSortName'] = sort_name
        emby_watchlist_metadata['SortName'] = sort_name
        emby_watchlist_metadata['LockedFields'] = ['SortName']

        self.update_item_metadata(emby_watchlist_metadata)

    def create_playlist(self, name, type):

        # Get the first items id of the correct type (so the collection is sorted right)
        initial_item_id = self.get_items_by_type(type, 1)[0]['Id']

        url = self._build_url('Playlists', {'Name': name, 'userId': self.user_id})
        response = self._post_request(url)
        playlist = response.json()

        print(f"Created playlist: {playlist['Name']} ({playlist['Id']})")

        return playlist

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

    # def remove_from_collection(self, collection_id, item_id):
    #    # http://192.168.0.120:8096/emby/Collections/157581/Items/Delete?Ids=179&X-Emby-Client=Emby Web&X-Emby-Device-Name=Firefox&X-Emby-Device-Id=8bb5b233-c701-4fa9-a948-3b21af5b93d0&X-Emby-Client-Version=4.7.13.0&X-Emby-Token=fd8eb5214cd74e01a3ee152207ff3b4d&X-Emby-Language=en-us
    #     url = self._build_url(f'Collections/{collection_id}/Items/Delete?Ids={item_id}')
    #     response = self._post_request(url)
    #     return response

    def get_collection_by_name(self, name):
        collections = self.get_collections()
        return next((item for item in collections if item.get('Name') == name), None)

    def get_collection(self, collection_id):
        url = self._build_url(f'users/{self.user_id}/items/{collection_id}')
        response = self._get_request(url)
        return response

    def get_collection_items(self, collection_id):
        url = self._build_url(f'users/{self.user_id}/items/{collection_id}/children')
        response = self._get_request(url)
        return response.get('Items', [])

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
        url = self._build_url(f'Collections/{collection_id}/Items/Delete', {'Ids': item_id})
        response = self._post_request(url)
        return response

    def delete_item_from_playlist(self, playlist_id, item_id):
        url = self._build_url(f'Playlists/{playlist_id}/Items/Delete', {'Ids': item_id})
        response = self._post_request(url)
        return response

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
            self.delete_collection(collection.get('Id'))
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
        return response.get('Items', [])

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
        return next((user for user in users if user.get('Name') == username), None)

    def set_favorite(self, item_id):
        url = self._build_url(f'Users/{self.user_id}/FavoriteItems/{item_id}')
        response = self._post_request(url)
        return response

    def get_users(self):
        # https://emby.faiyts.media/emby/users/public?X-Emby-Client=Emby%20Web&X-Emby-Device-Name=Google%20Chrome%20Linux&X-Emby-Device-Id=ea453a6f-4ba4-4901-a3c5-dd875239c834&X-Emby-Client-Version=4.7.13.0&X-Emby-Language=en-us
        url = self._build_url(f'Users/Public')
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

    #	http://192.168.0.120:8096/emby/Sessions/0378c315c1302972182a1c00cf6bf265/Playing?ItemIds=12910&PlayCommand=PlayNow&X-Emby-Client=Emby Web&X-Emby-Device-Name=Firefox&X-Emby-Device-Id=8bb5b233-c701-4fa9-a948-3b21af5b93d0&X-Emby-Client-Version=4.7.13.0&X-Emby-Token=fd8eb5214cd74e01a3ee152207ff3b4d&X-Emby-Language=en-us

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

    @staticmethod
    def create_poster(path, text, root_path, icon_path=f'/resources/tv.png'):
        width, height = 400, 600
        start, end = (233, 0, 4), (88, 76, 76)
        angle = -160
        font_path = f'{root_path}/resources/OpenSans-SemiBold.ttf'  # path to your .ttf font file

        gradient_creator = PosterImageCreator(width, height, start, end, angle, font_path)
        img = gradient_creator.create_gradient().add_icon_with_text(icon_path, text)

        img.save(path)
        return img
