import logging
import os

import structlog
import yaml
import openai
from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer

from src.clients.jellyfin import JellyfinClient
from src.db.queries import config_queries
from src.models import User, ClientType
from src.clients.tmdb import TmdbClient
from src.clients.trakt import TraktClient
from src.clients.emby import EmbyClient
from dotenv import load_dotenv
from pyarr import RadarrAPI
from src.clients.mdblist import MdbClient

import motor.motor_asyncio
import motor

from src.utils.string import is_uuid
from src.utils.logs import NamedPrintLoggerFactory, CenteredConsoleRenderer, redact_sensitive_data, \
    redact_keys_based_on_name

config_manager = None


class ConfigManager:
    instance = None

    def __init__(self, config_path=None, config_id=None):
        load_dotenv()
        self.log = self.get_logger(__name__)
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
            self.log.info('Config path found', configPath=config_path)
            self.load_config()

        if config_id:
            self.log.debug('Config ID found', configId=config_id)
            self.config_id = config_id
            # await self.fetch_and_load_config_from_db()

        # TODO: Refactor config to take in the config object from the database for a given user. For now, we'll use the default user
        self.user: User = User(
            userId='APP-DEFAULT-USER', name='APP USER', email="app@user.com", password="test")

    @classmethod
    async def create(cls, config_path=None, config_id=None):
        self = cls(config_path, config_id)
        await self.init_async()
        return self

    async def init_async(self):
        self.db = self.get_db()
        if self.config_id:
            self.log.debug('Config ID found', configId=self.config_id)
            await self.fetch_and_load_config_from_db()

    @staticmethod
    def get_logger(name=None) -> structlog.stdlib.BoundLogger:
        # print('Getting logger', name)
        """
        Retrieve a structured logger.

        :param name: Optional name for the logger. If not provided, will default to calling module's name.
        :return: Structured logger
        """
        structlog.configure(
            processors=[
                structlog.stdlib.add_logger_name,
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.set_exc_info,
                structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
                redact_sensitive_data,  # <-- Add this line
                CenteredConsoleRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
            context_class=dict,
            logger_factory=NamedPrintLoggerFactory(),
            cache_logger_on_first_use=False
        )
        return structlog.get_logger(name)

    @staticmethod
    def get_db() -> motor.motor_asyncio.AsyncIOMotorDatabase:
        client = motor.motor_asyncio.AsyncIOMotorClient(
            "mongodb://root:dragon@localhost:27017/sync-tools-db?authSource=admin")
        return client['sync-tools-db']

    async def fetch_and_load_config_from_db(self):
        self.log.info('Fetching config from DB for config ID', configId=self.config_id)
        db = self.get_db()
        config_data = await config_queries.get_full_config(db, config_id=self.config_id, log=self.log)

        if not config_data:
            raise ValueError(
                f"No configuration found for ID: {self.config_id}")

        self.log.info('Found config for user', userName=self.user.name, config_id=self.config_id,
                      len=len(config_data.clients))

        for config_client in config_data.clients:
            self.log.info('Processing client:', clientName=config_client.client.name)
            details = {
                'type': config_client.client.name.lower(),
            }

            client_fields = config_client.clientFields
            field_values = config_client.clientFieldValues

            self.log.info(f'Found {len(field_values)} field values for client:', total=len(field_values),
                          clientName=config_client.client.name)
            for field in field_values:
                details[field.clientField.name] = field.value

                # Use client ID (or name) as the key for the clients dictionary.
                self.clients_details[config_client.configClientId] = details

        self.log.info(f'Added {len(self.clients_details)} clients to config', clients=self.clients_details)
        self.add_clients(self.clients_details)

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
            self.log.info('Adding library', library_name=library_name, library_data=library_data)
            self.libraries[library_name] = library_data

    def add_collection_data(self, collections):
        for collection_name in collections.keys():
            collection_data = collections[collection_name]
            self.log.info('Adding collection', collection_name=collection_name, collection_data=collection_data)
            self.collections[collection_name] = collection_data

    def add_playlist_data(self, playlists):
        for playlist_name in playlists.keys():
            playlist_data = playlists[playlist_name]
            self.log.info('Adding playlist', playlist_name=playlist_name, playlist_data=playlist_data)
            self.playlists[playlist_name] = playlist_data

    def add_sync_data(self, sync):
        self.sync = sync

    def add_clients(self, clients):
        self.log.debug('Adding clients', clients=clients)
        for name, client_data in clients.items():
            self.log.debug('Adding client', clientName=name)
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
        self.log.info('Adding plex client', clientName=name)
        try:
            plex_client = PlexServer(server_url, access_token, timeout=120)
            self.clients[name] = plex_client
        except Exception as e:
            self.log.error('Error adding plex client', error=e, clientName=name)
            # raise ClientConnectionError
        return plex_client

    def add_mdblist_client(self, name, api_key):
        self.log.info('Adding MDBList client', clientName=name)
        mdblist_client = MdbClient(self.get_logger, api_key)
        self.clients[name] = mdblist_client
        return mdblist_client

    # Client to login through plex online plex.myapp.com
    def add_my_plex_client(self, name, username, password, resource):
        self.log.info('Adding myplex client', clientName=name)
        account = MyPlexAccount(username, password)
        my_plex_client = account.resource(resource).connect()
        self.clients[name] = my_plex_client
        self.accounts[name] = account
        return my_plex_client

    def add_emby_client(self, name, server_url, username, api_key):
        self.log.info('Adding emby client', clientName=name)
        emby_client = EmbyClient(self.get_logger, server_url, username, api_key)
        self.clients[name] = emby_client
        return emby_client

    def add_jellyfin_client(self, name, server_url, username, api_key):
        self.log.info('Adding jellyfin client', clientName=name)

        jellyfin_client = JellyfinClient(self.get_logger, server_url, username, api_key)
        self.clients[name] = jellyfin_client
        return jellyfin_client

    def add_radarr_client(self, name, host, api_key):
        self.log.info('Adding radarr client', clientName=name)
        radarr_client = RadarrAPI(host, api_key)
        self.clients[name] = radarr_client
        return radarr_client  # https://docs.totaldebug.uk/pyarr/modules/radarr.html

    # def add_sonarr_client(self, name, host, api_key):

    # TODO: Implement these
    # def add_portainer_client(self, name, server_url, username, password):
    #     portainer_client = Portainer(server_url, username, password)
    #     self.clients.ts[name] = portainer_client
    #     return portainer_client
    #
    def add_trakt_client(self, name, username, client_id, client_secret):
        self.log.info('Adding trakt client', clientName=name)
        trakt_client = TraktClient(self.get_logger,
                                   client_id=client_id, client_secret=client_secret,
                                   token_file=f'{self.config_path}/trakt.json')  # TODO: unique per clientId
        self.clients[name] = trakt_client
        return trakt_client

    def add_chatGPT_client(self, name, api_key):
        self.log.info('Adding chatGPT client', clientName=name)
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
                self.log.info('Client with UUID not found!', uuid=id_or_type)
                return None

        else:
            try:
                self.log.info('Searching for client by type', type=id_or_type)
                return self.get_client_by_type(id_or_type)
            except KeyError:
                self.log.info('Client by type not found!', type=id_or_type)
                return None

    def get_client_details(self, name):
        try:
            return self.clients_details[name]
        except:
            self.log.info(f'{name} client details not found!', clientName=name)
            return None

    def get_account(self, name):
        return self.accounts[name]

    def get_root_path(self):
        return self.root_path

    def get_config_path(self):
        return self.config_path

    def get_libraries(self):
        return self.libraries

    def get_collection_settings(self):
        return self.collections

    def add_tmdb_client(self, name, api_key, username, password):
        self.log.info('Adding tmdb client', clientName=name)
        tmdb_client = TmdbClient(self.log, api_key, username, password)
        self.clients[name] = tmdb_client
        return tmdb_client

    @staticmethod
    async def get_manager(config_id='APP-DEFAULT-CONFIG'):
        if ConfigManager.instance is None:
            ConfigManager.instance = await ConfigManager.create(config_id=config_id)
        return ConfigManager.instance

    def get_client_by_type(self, client_type: ClientType):
        # loop through clients and find the one with the matching client_type
        self.log.info('Looking for client by type', total=len(self.clients_details), client_type=client_type)
        for clientId, client in self.clients_details.items():
            if client['type'] == client_type:
                self.log.info('Found client by client_type', clientId=clientId, client=client)
                return self.clients[clientId]
        self.log.info('Client not found by client_type', client_type=type)
