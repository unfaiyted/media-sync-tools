

class TMDBListProviderResult:
    def __init__(self, id, title, overview, release_date):
        self.id = id
        self.title = title
        self.overview = overview
        self.release_date = release_date

    def __str__(self):
        return f"ID: {self.id}, Title: {self.title}, Overview: {self.overview}, Release Date: {self.release_date}"


class TMDBProvider:

    def __init__(self, config, filters=None):
        self.config = config
        self.client = config.get_client('tmdb')
        self.filters = filters

        if filters is None:
            raise Exception("No filters provided. Cannot get list.")

    def _convert_filters_to_query_params(self):
        return {filter_item['type']: filter_item['value'] for filter_item in self.filters}

    def get_list(self):
        filter_query_params = self._convert_filters_to_query_params()

        movie_data = self.client.discover_movie(**filter_query_params)
        movie_results = movie_data.get("results", [])


        primary_list = []

        for item in movie_results:
            print(item['title'], item['release_date'])
            # item['overview']
            # try:
            emby_search = self.config.get_client('emby').search(item['title'], 'Movie')

            # print('SEARCH = ',emby_search[0]['ProductionYear'], item['release_date'])
            try:
                if(int(emby_search[0]['ProductionYear']) == int(item['release_date'].split('-')[0])):
                    print('FOUND = ',emby_search[0]['ProductionYear'], item['release_date'].split('-')[0])

                    if emby_search[0]['Type'] == 'Trailer':
                        continue

                    primary_list.append(emby_search[0])
                    continue
            except:
                print('not found')

        return primary_list



        # return [TMDBListProviderResult(item['id'], item['title'], item['overview'], item['release_date']) for item in movie_results]


# # Example usage of the above class:
# config_manager = ConfigManager()
#
# filters = [
#     {'type': 'year', 'value': 2020},
#     {'type': 'with_genres', 'value': '28'}
# ]
# # Assuming MockConfig and MockTmdbClient are defined as earlier:
# provider = TMDBProvider(config_manager, filters)
# movie_list = provider.get_list()
#
# for movie in movie_list:
#     print(movie)
