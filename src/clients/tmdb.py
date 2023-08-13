import requests
import time

class TmdbClient:
    TMDB_API_URL = "https://api.themoviedb.org/3"
    RETRY_MAX = 5
    RETRY_DELAY = 5  # Starts with 5 seconds

    def __init__(self, bearer_key, username=None, password=None):
        self.bearer_key = bearer_key

    def _headers(self):
        return {
            "Content-Type": "application/json",
             "Authorization": f"Bearer {self.bearer_key}"
        }

    def _request(self, method, endpoint, **kwargs):
        retries = 0
        delay = self.RETRY_DELAY

        while retries <= self.RETRY_MAX:
            response = requests.request(
                method, f"{self.TMDB_API_URL}{endpoint}" , headers=self._headers(), **kwargs)

            if response.status_code == 429:  # Too Many Requests
                time.sleep(delay)
                retries += 1
                delay *= 2
                continue

            response.raise_for_status()
            return response.json()

        raise Exception("Max retries exceeded")

    def get_popular_movies(self, page=1):
        return self._request("GET", f"/movie/popular?language=en-US&page={page}")

    def search_movie(self, query):
        return self._request("GET", f"/search/movie?query={query}")

    def get_movie_details(self, movie_id):
        return self._request("GET", f"/movie/{movie_id}")

    def discover_movie(self, **kwargs):
        """
        Uses the discover endpoint to search for movies based on specific criteria.
        Accepts various keyword arguments as filters for discovery.
        """
        query_params = '&'.join([f"{k}={v}" for k, v in kwargs.items()])
        return self._request("GET", f"/discover/movie?{query_params}")

    # ... Add other methods as required ...

# tmdb = TmdbClient("eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwYzNjZjNlNzI2YjZkMzU2NmZiZTM4Yjc0YzIzOWU1YiIsInN1YiI6IjVhYjk0NDdjMGUwYTI2MzY0ZTAwNWRjZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Hacuw5YT8hWm7Ec5crZBTGQ1LTJalUKutcTFHCiWByk")
#
# # Fetch popular movies
# popular_movies = tmdb.get_popular_movies()
# print(popular_movies)
# # Search for a movie
# search_results = tmdb.search_movie("Inception")
# print(search_results)
# # Get movie details by ID
# movie_details = tmdb.get_movie_details(157336)  # Replace 12345 with a real movie ID
# print(movie_details)
# # ... Use the fetched data ...
