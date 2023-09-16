from io import BytesIO
from PIL import Image

import requests
import time


class TmdbClient:
    TMDB_API_URL = "https://api.themoviedb.org/3"
    TMDB_V4_API_URL = "https://api.themoviedb.org/4"
    TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/original"
    RETRY_MAX = 5
    RETRY_DELAY = 5  # Starts with 5 seconds

    def __init__(self, log, bearer_key, username=None, password=None):
        self.bearer_key = bearer_key,
        self.log = log

    def _headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.bearer_key}"
        }

    def _request(self, method, endpoint, version=3, **kwargs):
        retries = 0
        delay = self.RETRY_DELAY

        while retries <= self.RETRY_MAX:
            if version == 4:
                self.log.debug("Making request", method=method, endpoint=endpoint, retries=retries)
                response = requests.request(
                    method, f"{self.TMDB_V4_API_URL}{endpoint}", headers=self._headers(), **kwargs)
            else:
                self.log.debug("Making request", method=method, endpoint=endpoint, retries=retries)
                response = requests.request(
                method, f"{self.TMDB_API_URL}{endpoint}", headers=self._headers(), **kwargs)

            if response.status_code == 429:  # Too Many Requests
                self.log.warning('Too many requests. Retrying after delay.', delay=delay, response=response)
                time.sleep(delay)
                retries += 1
                delay *= 2
                continue

            # response.raise_for_status()
            if response.status_code == 200:
                self.log.debug("Got response", response=response)
                return response.json()

            return None if response.status_code == 404 else response.json()
        raise Exception("Max retries exceeded")

    def get_popular_movies(self, page=1):
        self.log.debug(f"Getting popular movies for page {page}", page=page)
        return self._request("GET", f"/movie/popular?language=en-US&page={page}")

    def search_movie(self, query):
        self.log.debug("Searching for movie", query=query)
        return self._request("GET", f"/search/movie?query={query}")

    def get_movie_details(self, movie_id):
        self.log.debug("Getting movie details", movie_id=movie_id)
        return self._request("GET", f"/movie/{movie_id}")

    def discover_movie(self, **kwargs):
        """
        Uses the Discover endpoint to search for movies based on specific criteria.
        Accepts various keyword arguments as filters for discovery.
        """
        query_params = '&'.join([f"{k}={v}" for k, v in kwargs.items()])
        self.log.debug("Discovering movies", query_params=query_params)
        return self._request("GET", f"/discover/movie?{query_params}")

    # ... Add other methods as required ...
    def get_movie_poster_path(self, movie_id, full_path=False):
        """
        Fetches the poster path for a movie using its ID.
        :param full_path:
        :param movie_id: ID of the movie.
        :return: poster path.
        """

        relative_path = self.get_movie_details(movie_id)

        if full_path:
            self.log.debug("Getting full movie poster path", movie_id=movie_id)
            return f"{self.TMDB_IMAGE_URL}{relative_path}"

        movie_details = self.get_movie_details(movie_id)

        try:
            self.log.debug("Getting movie poster path", movie_details=movie_details)
            return movie_details.get('poster_path')
        except Exception:
            self.log.error("Movie poster path not found", movie_details=movie_details)
            return None

    def get_movie_by_name_and_year(self, name, year):
        """
        Search for a movie by its name and year of release.

        :param name: Name of the movie.
        :param year: Year of release.
        :return: JSON response containing the search results.
        """
        self.log.debug("Searching for movie by name and year", name=name, year=year)
        endpoint = f"/search/movie?query={name}&primary_release_year={year}"
        return self._request("GET", endpoint)

    def get_movie_poster(self, movie_id):
        """
        Fetches the movie poster as an RGBA image.
        :param movie_id: ID of the movie.
        :return: PIL Image object in RGBA format.
        """
        poster_path = self.get_movie_poster_path(movie_id)
        self.log.debug(
            "Getting movie poster", movie_id=movie_id, poster_path=poster_path
        )
        if not poster_path:
            return None

        response = requests.get(f"{self.TMDB_IMAGE_URL}{poster_path}", stream=True)
        response.raise_for_status()
        if response.status_code == 200:
            self.log.debug("Got movie poster.", movie_id=movie_id, poster_path=poster_path)
            image = Image.open(BytesIO(response.content)).convert("RGBA")
            self.log.debug(
                "Converted movie poster to RGBA.",
                movie_id=movie_id,
                poster_path=poster_path,
            )
            return image

        return None

    def get_list_by_id(self, list_id):
        """
        Retrieve MediaList from TMDB by ID.
        :return:
        """
        self.log.info("Getting TMDB list by id", list_id=list_id)
        return self._request("GET", f"/list/{list_id}", version=4)
