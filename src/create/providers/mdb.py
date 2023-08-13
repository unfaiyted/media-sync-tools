

class ListProviderResult:
    def __init__(self, id, name, description, movies):
        self.id = id
        self.name = name
        self.description = description
        self.movies = movies

class MdbProvider:

    def __init__(self, config, filters=None):
        self.config = config
        self.client = config.get_client('mdb')
        self.filters = filters

        if filters is not None:
            self.id = filters[0].get('value', None)


    def get_list(self):
        if self.id is None:
            print('No list id provided. Cannot get list.')
            return None

        list = self.client.get_list_information(list_id=self.id)[0]
        list_items = self.client.get_list_items(list['id'])

        primary_list = []

        for item in list_items:
            print('-------------', item['id'], item['imdb_id'], item['tvdb_id'], item['language'], item['release_year'], item['rank'], item['spoken_language'])
            try:
                # TODO: Replace with OmniClient
                emby_search = self.config.get_client('emby').get_media(external_id='imdb.'+item['imdb_id'])
                if emby_search[0]['Type'] == 'Trailer':
                    continue
                primary_list.append(emby_search[0])
                continue
            except:
                print('not found-imdb')

            try:
                emby_search = self.config.get_clients('emby').get_media(external_id='tvdb.'+item['tvdb_id'])
                if emby_search[0]['Type'] == 'Trailer':
                    continue
                primary_list.append(emby_search[0])
            except:
                print('not found-tvdb')
                #emby.get_media(external_id='tvdb.'+item['tvdb_id'])

        return primary_list
