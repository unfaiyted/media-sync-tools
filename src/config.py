import os
import yaml
import openai
from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer

from src.clients.jellyfin import Jellyfin
from src.db.queries import config_queries
from src.models import User
from src.clients.tmdb import TmdbClient
from src.clients.trakt import TraktClient
from src.clients.emby import Emby
from dotenv import load_dotenv
from pyarr import RadarrAPI
from src.clients.mdblist import MDBListClient
from pymongo import MongoClient

import motor.motor_asyncio
import motor
import re

config_manager = None


def is_uuid(string):
    """Check if string is a valid UUID"""
    regex = r'^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\Z'
    match = re.fullmatch(regex, string, re.I)
    return bool(match)


class ConfigManager:
    instance = None

    def __init__(self, config_path=None, config_id=None):
        load_dotenv()
        self.clients = {}
        self.clients_details = {}
        self.accounts = {}
        self.libraries = {}
        self.collections = {}
        self.playlists = {}
        self.sync = {}
        self.root_path = os.path.dirname(os.path.abspath(__file__))
        self.config_path = config_path or os.path.join(
            self.root_path, '../', 'config')
        self.create_subdirectories()
        self.db = self.get_db()

        if config_path:
            self.load_config()

        if config_id:
            self.config_id = config_id
            # await self.fetch_and_load_config_from_db()

        # TODO: Refactor config to take in the config object from the database for a given user. For now, we'll use the default user
        self.user: User = User(
            userId='APP-DEFAULT-USER', name='APP USER', email="app@user.com", password="test")

    @classmethod
    async def create(cls, config_path=None, config_id=None):
        self = cls(config_path, config_id)
        # self.config_id = config_id
        await self.init_async()
        return self

    async def init_async(self):
        self.db = self.get_db()
        if self.config_id:
            await self.fetch_and_load_config_from_db()

    @staticmethod
    def get_db() -> motor.motor_asyncio.AsyncIOMotorDatabase:
        client = motor.motor_asyncio.AsyncIOMotorClient(
            "mongodb://root:dragon@localhost:27017/sync-tools-db?authSource=admin")
        return client['sync-tools-db']

    async def fetch_and_load_config_from_db(self):
        print('Fetching config from DB for config ID: ', self.config_id)
        db = self.get_db()
        config_data = await config_queries.get_full_config(db, config_id=self.config_id)

        # print('Config data: ', config_data)

        if not config_data:
            raise ValueError(
                f"No configuration found for ID: {self.config_id}")

        # self.user = config_data.get('user')
        print('Config data: ', config_data)
        print(
            f'Found config for user: {self.user.name} and config ID: {self.config_id}')
        print(f'Total clients: {len(config_data.clients)}')
        # If 'clients' in the config is a list, you'll need to iterate through it.
        for config_client in config_data.clients:
            print(f'Processing client: {config_client.client.name}')
            details = {
                'type': config_client.client.name.lower(),
            }

            # print('config_client: ', config_client.clientFieldValues)

            client_fields = config_client.clientFields
            field_values = config_client.clientFieldValues

            print(
                f'Found {len(field_values)} field values for client: {config_client.client.name}')
            for field in field_values:
                details[field.clientField.name] = field.value

                # details[field_values['fieldId']] = field['value']

                # Use client ID (or name) as the key for the clients dictionary.
                self.clients_details[config_client.configClientId] = details

            print('Client Details: ',
                  self.clients_details[config_client.configClientId])

        # self.clients_details = config_data.clients
        print(f'Added {len(self.clients_details)} clients to config')
        self.add_clients(self.clients_details)
        # self.add_library_data(config_data.get('libraries', {}))
        # self.add_collection_data(config_data.get('collections', {}))
        # self.add_playlist_data(config_data.get('playlists', {}))
        # self.add_sync_data(config_data.get('sync', {}))
        # If 'clients' in the config is a list, you'll need to iterate through it.
        # for client_data in config_data.get('clients', []):
        # process each client_data as you were doing in your 'add_clients' method.

        # Similar approach for libraries and sync
        # for library_data in config_data.get('libraries', []):
        # process each library_data

        # sync_data = config_data.get('sync')
        # if sync_data:
        # process sync_data

    def get_user(self):
        return self.user

    def create_subdirectories(self):
        subdirectories = ['logs', 'collections',
                          'playlists', 'resources', 'libraries']
        for subdir in subdirectories:
            path = os.path.join(self.config_path, subdir)
            os.makedirs(path, exist_ok=True)

    def load_config(self):
        config_file = os.path.join(self.config_path, 'config.yml')
        with open(config_file, 'r') as f:
            config_data = yaml.safe_load(f)

        self.clients_details = config_data.get('clients', {})

        self.add_clients(config_data.get('clients', {}))
        self.add_library_data(config_data.get('libraries', {}))
        self.add_collection_data(config_data.get('collections', {}))
        self.add_playlist_data(config_data.get('playlists', {}))
        self.add_sync_data(config_data.get('sync', {}))
        # Add other sections (libraries, sync, collections, playlists, etc.) as needed

    def add_library_data(self, libraries):
        for library_name in libraries.keys():
            library_data = libraries[library_name]
            print('Adding library', library_name, library_data)
            self.libraries[library_name] = library_data

    def add_collection_data(self, collections):
        for collection_name in collections.keys():
            collection_data = collections[collection_name]
            print('Adding collection', collection_name, collection_data)
            self.collections[collection_name] = collection_data

    def add_playlist_data(self, playlists):
        for playlist_name in playlists.keys():
            playlist_data = playlists[playlist_name]
            print('Adding playlist', playlist_name, playlist_data)
            self.playlists[playlist_name] = playlist_data

    def add_sync_data(self, sync):
        self.sync = sync

    def add_clients(self, clients):
        for name, client_data in clients.items():
            client_type = client_data.get('type')

            if client_type == 'plex':
                server_url = client_data.get('server_url')
                access_token = client_data.get('access_token')
                self.add_plex_client(name, server_url, access_token)
            elif client_type == 'myplex':
                username = client_data.get('username')
                password = client_data.get('password')
                resource = client_data.get('resource')
                self.add_my_plex_client(name, username, password, resource)
            elif client_type == 'emby':
                server_url = client_data.get('server_url')
                username = client_data.get('username')
                api_key = client_data.get('api_key')
                self.add_emby_client(name, server_url, username, api_key)
            elif client_type == 'jellyfin':
                server_url = client_data.get('server_url')
                username = client_data.get('username')
                api_key = client_data.get('api_key')
                self.add_jellyfin_client(name, server_url, username, api_key)
            elif client_type == 'trakt':
                username = client_data.get('username')
                client_id = client_data.get('client_id')
                client_secret = client_data.get('client_secret')
                self.add_trakt_client(name, username, client_id, client_secret)
            elif client_type == 'chatGPT':
                api_key = client_data.get('api_key')
                self.add_chatGPT_client(name, api_key)
            elif client_type == 'radarr':
                api_key = client_data.get('api_key')
                host = client_data.get('server_url')
                self.add_radarr_client(name, host, api_key)
            elif client_type == 'mdb':  # Add a new elif block for the MDBList client
                api_key = client_data.get('api_key')
                self.add_mdblist_client(name, api_key)
            elif client_type == 'tmdb':
                bearer_token = client_data.get('bearer_token')
                username = client_data.get('username')
                password = client_data.get('password')
                self.add_tmdb_client(name, bearer_token, username, password)

            # Add other client types as needed

    # Rest of the methods remain the same

    def add_plex_client(self, name, server_url, access_token):
        print('Adding plex client', server_url, access_token)
        plex_client = PlexServer(server_url, access_token, timeout=120)
        self.clients[name] = plex_client
        return plex_client

    def add_mdblist_client(self, name, api_key):
        print('Adding MDBList client', api_key, name)
        mdblist_client = MDBListClient(api_key)
        self.clients[name] = mdblist_client
        print('MDBList client added', self.clients[name])
        return mdblist_client

    # Client to login through plex online plex.myapp.com
    def add_my_plex_client(self, name, username, password, resource):
        print('Adding myplex client', username, password, resource)
        account = MyPlexAccount(username, password)
        my_plex_client = account.resource(resource).connect()
        self.clients[name] = my_plex_client
        self.accounts[name] = account
        return my_plex_client

    def add_emby_client(self, name, server_url, username, api_key):
        print('Adding emby client', server_url, username, api_key)
        emby_client = Emby(server_url, username, api_key)
        self.clients[name] = emby_client
        return emby_client

    def add_jellyfin_client(self, name, server_url, username, api_key):
        print('Adding jellyfin client', server_url, username, api_key)
        jellyfin_client = Jellyfin(server_url, username, api_key)
        self.clients[name] = jellyfin_client
        return jellyfin_client

    def add_radarr_client(self, name, host, api_key):
        radarr_client = RadarrAPI(host, api_key)
        self.clients[name] = radarr_client
        return radarr_client  # https://docs.totaldebug.uk/pyarr/modules/radarr.html

    # def add_sonarr_client(self, name, host, api_key):

    # TODO: Implement these
    # def add_portainer_client(self, name, server_url, username, password):
    #     print('Adding portainer client', server_url, username, password)
    #     portainer_client = Portainer(server_url, username, password)
    #     self.clients.ts[name] = portainer_client
    #     return portainer_client
    #
    def add_trakt_client(self, name, username, client_id, client_secret):
        # TODO implement based on client_id and client_secret oauth
        print('Adding trakt client', name, username, client_id, client_secret)

        trakt_client = TraktClient(
            client_id, client_secret, token_file=f'{self.config_path}/trakt.json')

        self.clients[name] = trakt_client

        return trakt_client

    def add_chatGPT_client(self, name, api_key):
        print('Adding chatGPT client', api_key)
        openai.api_key = api_key
        self.clients[name] = openai
        return openai

    def get_client(self, id_or_type):
        # check if client is a uuid
        # if not uuid, search for client by type and find the uuid in the db.

        if is_uuid(id_or_type):
            try:
                return self.clients[id_or_type]
            except KeyError:
                print(f'Client with UUID {id_or_type} not found!')
                return None

        else:
            # Here, you'd search the database for the client's UUID by type
            # For this step, you'd likely need an additional method or database query
            try:
                print('Searching for client by type', id_or_type)
                return self.get_client_by_type(id_or_type)
            except KeyError:
                print(f'Client by {id_or_type} not found!')
                return None

    def get_client_details(self, name):
        try:
            return self.clients_details[name]
        except:
            print(f'{name} client details not found!')
            return None

    def get_account(self, name):
        return self.accounts[name]

    def get_root_path(self):
        print('Root path: ', self.root_path)
        return self.root_path

    def get_config_path(self):
        return self.config_path

    def get_libraries(self):
        return self.libraries

    def get_collection_settings(self):
        return self.collections

    def add_tmdb_client(self, name, api_key, username, password):
        print('Adding tmdb client', api_key)

        tmdb_client = TmdbClient(api_key, username, password)
        self.clients[name] = tmdb_client
        return tmdb_client

    @staticmethod
    async def get_manager(config_id='APP-DEFAULT-CONFIG'):
        if ConfigManager.instance is None:
            ConfigManager.instance = await ConfigManager.create(config_id=config_id)
        return ConfigManager.instance

    def get_client_by_type(self, type):
        # loop through clients and find the one with the matching type
        print(
            f'Looking for client by type: {type}, total clients: {len(self.clients_details)}')
        print('Clients: ', self.clients_details)
        for clientId, client in self.clients_details.items():
            print('Checking client', client, clientId)
            # print('Checking client', client_id)
            if client['type'] == type:
                print('Found client by type', clientId, client)
                print('self.clients', self.clients[clientId])
                return self.clients[clientId]
        print('Client not found by type', type)
