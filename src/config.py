import os

from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
from utils.emby import Emby
from dotenv import load_dotenv
class ConfigManager:
    def __init__(self, config_path=None):
        load_dotenv()
        self.clients = {}
        self.accounts = {}
        self.root_path = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(self.root_path, '../', 'config')
        #TODO: handle errors and validate env variables
        self.add_plex_client('plex', os.getenv('PLEX_SERVER_URL'), os.getenv('PLEX_ACCESS_TOKEN'))
        self.add_my_plex_client('myplex',os.getenv('PLEX_USERNAME'), os.getenv('PLEX_PASSWORD'), os.getenv('PLEX_RESOURCE'))
        self.add_emby_client('emby', os.getenv('EMBY_SERVER_URL') ,os.getenv('EMBY_USERNAME'), os.getenv('EMBY_API_KEY'))

    def add_plex_client(self, name, server_url, access_token):
        print('Adding plex client', server_url, access_token)
        plex_client = PlexServer(server_url, access_token)
        self.clients[name] = plex_client
        return plex_client

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

    # TODO: Implement these
    # def add_portainer_client(self, name, server_url, username, password):
    #     print('Adding portainer client', server_url, username, password)
    #     portainer_client = Portainer(server_url, username, password)
    #     self.clients[name] = portainer_client
    #     return portainer_client
    #
    # def add_trakt_client(self, name, username, password):
    #     print('Adding trakt client', username, password)
    #     trakt_client = Trakt(username, password)
    #     self.clients[name] = trakt_client
    #     return trakt_client

    def get_client(self, name):
        return self.clients[name]

    # TODO: Error handling, and is this the best way to handle this?
    def get_account(self, name):
        return self.accounts[name]

    def get_root_path(self):
        print('Root path: ', self.root_path)
        return self.root_path

    def get_config_path(self):
        return self.config_path



