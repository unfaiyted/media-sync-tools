import requests

class MDBListClient:
    BASE_URL = "https://mdblist.com/api/"

    def __init__(self, api_key):
        self.api_key = api_key

    def _make_request(self, endpoint, params=None):
        url = f"{self.BASE_URL}{endpoint}"
        params = params or {}
        params["apikey"] = self.api_key

        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_movie_info_by_imdb_id(self, imdb_id):
        endpoint = ""
        params = {"i": imdb_id}
        return self._make_request(endpoint, params)

    def search_movie_or_show(self, query):
        endpoint = ""
        params = {"s": query}
        return self._make_request(endpoint, params)

    def get_user_limits(self):
        endpoint = "user/"
        return self._make_request(endpoint)

    def get_user_lists(self):
        endpoint = "lists/user/"
        return self._make_request(endpoint)

    def get_list_information(self, list_id):
        endpoint = f"lists/{list_id}"
        return self._make_request(endpoint)

    def get_list_items(self, list_id):
        endpoint = f"lists/{list_id}/items"
        return self._make_request(endpoint)

    def get_top_lists(self):
        endpoint = "lists/top"
        return self._make_request(endpoint)

    def search_lists(self, query):
        endpoint = "lists/search"
        params = {"s": query}
        return self._make_request(endpoint, params)

    def get_bulk_ratings(self, media_type, return_rating, ids, provider):
        endpoint = f"rating/{media_type}/{return_rating}"
        payload = {"ids": ids, "provider": provider}
        response = requests.post(f"{self.BASE_URL}{endpoint}", json=payload, params={"apikey": self.api_key})
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
