class TraktProvider:
    def __init__(self, config, filters=None):
        self.config = config
        self.client = config.get_client('trakt')
        self.username = None
        self.list_slug_or_id = None

        if filters:
            for filter_item in filters:
                if filter_item['type'] == 'username':
                    self.username = filter_item['value']
                elif filter_item['type'] in ['list_slug', 'list_id']:
                    self.list_slug_or_id = filter_item['value']

        if not self.username or not self.list_slug_or_id:
            print("Both username and list_slug/list_id are required.")
            # Handle error or throw exception

    def get_list(self):
        if self.list_slug_or_id is None:
            print('No list id provided. Cannot get list.')
            return None

        # list_info =  self.client.get_list(username=self.username, list_id_or_slug=self.list_slug_or_id)
        list_items = self.client.get_list_items(username=self.username, list_id_or_slug=self.list_slug_or_id)

        primary_list = []

        for item in list_items:
            # Assuming items contain these fields, you'll need to adjust based on Trakt API documentation
            print('-------------', item['show']['ids'],  item['show']['title'], item['show']['year'])

            try:
                emby_search = self.config.get_client('emby').get_media(external_id='imdb.'+item['show']['ids']['imdb'])

                if emby_search[0]['Type'] == 'Trailer':
                        continue

                primary_list.append(emby_search[0])
                continue
            except:
                print('not found-imdb')

            try:
                emby_search = self.config.get_clients('emby').get_media(external_id='tvdb.'+item['show']['ids']['tvdb'])
                if emby_search[0]['Type'] == 'Trailer':
                    continue

                primary_list.append(emby_search[0])
            except:
                print('not found-tvdb')

        return primary_list



