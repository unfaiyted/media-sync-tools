# Class that will be able to sync an action to a series of clients


# Example: Omni.createCollection() -> OmniCollection -> which will create a collection
# for the defined clients, one in plex, one in emby, one in jellyfin, etc.
# OmniCollection will have a method to sync the collection to all clients
# OmniCollection will need to know what clients to sync to, and what the collection or list is.

# clients should also include list storing websites like Trakt, IMDB, etc.
# could sync lists across sites.  Could also sync lists across clients.

# Other Methods to add:
# Omni.syncCollection() -> OmniCollection.sync() -> syncs the collection to all clients
# Omni.syncList() -> OmniList.sync() -> syncs the list to all clients
# Omni.savePosters() -> Omni.savePosters() -> saves posters for all clients
# Omni.saveBackdrops() -> Omni.saveBackdrops() -> saves backdrops for all clients
# Omni.getCollection() -> OmniCollection -> gets the collection from all clients
SUPPORTED_CLIENT_TYPES = ['plex', 'emby', 'myplex']  # and so on...


class Omni:

    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.clients = self._initialize_clients()
        self.primary = self._determine_primary()

    def _initialize_clients(self):
        all_clients = self.config_manager.clients
        clients = {}

        # Filter clients based on supported types
        for name, client in all_clients.items():
            client_details = self.config_manager.get_client_details(name)
            client_type = client_details.get('type')
            if client_type in SUPPORTED_CLIENT_TYPES:
                clients[name] = client

        return clients

    def _determine_primary(self):
        for name, client in self.clients.items():
            client_details = self.config_manager.get_client_details(name)
            if client_details.get('isPrimary', False):
                return client
        return None

    def createCollection(self, collection_name):
        # Fetch data or any action from the primary
        data = self.primary.get_collection_data(collection_name)

        # Sync this data to all clients
        for client in self.clients.values():
            client.create_collection(data)

    def createPlaylist(self, playlist_name):
        # Similar to above, get from primary
        data = self.primary.get_playlist_data(playlist_name)

        # Sync to all
        for client in self.clients.values():
            client.create_playlist(data)

    def uploadPoster(self, poster_path):
        poster_data = self.primary.get_poster_data(poster_path)

        for client in self.clients.values():
            client.upload_poster(poster_data)

    def deleteCollection(self, collection_name):
        # Might not need to fetch from primary, just delete in all
        for client in self.clients.values():
            client.delete_collection(collection_name)

    def addItemsToList(self, list_id, items):
         for client in self.clients.values():
            client.add_items_to_list(list_id, items)

    def delete_item_from_list(self, list_id, item_id):
        for client in self.clients.values():
            client.delete_item_from_list(list_id, item_id)

