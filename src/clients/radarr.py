# from config import ConfigManager


class RadarrInteractions:
    def __init__(self, config, client_name='radarr'):
        self.config = config
        self.client = self.config.get_client(client_name)
        self.root_dir = self.config.get_client_details(client_name)['default_media_path']
        self.quality_profile = self.config.get_client_details(client_name)['quality_profile']
        self.quality_profile_id = self._get_profile_id(self.quality_profile)

    def _get_profile_id(self, profile_name):
        try:
            profiles = self.client.get_quality_profile()
            # print('Profiles: ', profiles)
            for profile in profiles:
                if profile['name'] == profile_name:
                    print('Found profile: ', profile['name'], profile['id'])
                    return profile['id']
        except:
            print('Error getting profile id for ', profile_name)
            return None

    def add_movie_by_name_and_year(self, movie_name, movie_year):

        # Search for the movie by name
        search_results = self.client.lookup_movie(movie_name)

        # print('Search results: ', search_results)

        if len(search_results) == 0:
            print(f"No matching movie found for '{movie_name}'")
            return

        # Find the movie with the matching year
        matching_movies = [movie for movie in search_results if str(movie['year']) == str(movie_year)]

        # print(matching_movies)

        if len(matching_movies) == 0:
            print(f"No matching movie found for '{movie_name}' ({movie_year})")
            return

        # Choose the first matching movie
        selected_movie = matching_movies[0]

        print('Found/Selected movie: ', selected_movie)

        print('Adding with profile id: ', self.quality_profile_id, ' and root dir: ', self.root_dir)
        # Add the movie to Radarr
        try:
            added_movie = self.client.add_movie(selected_movie, root_dir=self.root_dir, quality_profile_id=self.quality_profile_id)

            return added_movie
        except Exception as e:
            print('Error adding movie to Radarr. Potentially already added.', e)
            return None

# # Example usage:
# movie_name = 'A Wrinkle in Time'
# movie_year = 2014
#
# # Add movie to Radarr
#
#
# config = ConfigManager()
#
# radarr = RadarrInteractions(config)
#
# added_movie = radarr.add_movie_by_name_and_year(movie_name, movie_year)
#
# print(added_movie)
