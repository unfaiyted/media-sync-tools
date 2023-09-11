import requests


class MdbClient:
    BASE_URL = "https://mdblist.com/api/"

    def __init__(self,log, api_key):
        self.log = log
        self.api_key = api_key

    def _make_request(self, endpoint, params=None):
        url = f"{self.BASE_URL}{endpoint}"
        params = params or {}
        params["apikey"] = self.api_key

        response = requests.get(url, params=params)
        if response.status_code == 200:
            self.log.debug("MDBList request successful", url=url, params=params)
            return response.json()
        else:
            self.log.error("MDBList request failed", url=url, params=params, response=response)
            # response.raise_for_status()
            return None

    def get_movie_info_by_imdb_id(self, imdb_id):
        endpoint = ""
        params = {"i": imdb_id}
        self.log.debug("Getting movie info by IMDB ID", imdb_id=imdb_id)
        return self._make_request(endpoint, params)

    def search_movie_or_show(self, query):
        endpoint = ""
        params = {"s": query}
        self.log.debug("Searching for movie or show", query=query)
        return self._make_request(endpoint, params)

    def get_user_limits(self):
        endpoint = "user/"
        self.log.debug("Getting user limits", endpoint=endpoint)
        return self._make_request(endpoint)

    def get_user_lists(self):
        endpoint = "lists/user/"
        self.log.debug("Getting user lists", endpoint=endpoint)
        return self._make_request(endpoint)

    def get_list_information(self, list_id):
        endpoint = f"lists/{list_id}"
        self.log.debug("Getting list information", endpoint=endpoint, list_id=list_id)
        return self._make_request(endpoint)

    def get_list_items(self, list_id):
        endpoint = f"lists/{list_id}/items"
        self.log.debug("Getting list items", endpoint=endpoint, list_id=list_id)
        return self._make_request(endpoint)

    def get_top_lists(self):
        endpoint = "lists/top"
        self.log.debug("Getting top lists", endpoint=endpoint)
        return self._make_request(endpoint)

    def search_lists(self, query):
        endpoint = "lists/search"
        params = {"s": query}
        self.log.debug("Searching for lists", endpoint=endpoint, query=query)
        return self._make_request(endpoint, params)

    def get_bulk_ratings(self, media_type, return_rating, ids, provider):
        endpoint = f"rating/{media_type}/{return_rating}"
        payload = {"ids": ids, "provider": provider}
        response = requests.post(f"{self.BASE_URL}{endpoint}", json=payload, params={"apikey": self.api_key})
        self.log.debug("Getting bulk ratings", endpoint=endpoint, payload=payload)
        if response.status_code == 200:
            self.log.debug("Got bulk ratings", endpoint=endpoint, payload=payload)
            return response.json()
        else:
            self.log.error("Failed to get bulk ratings", endpoint=endpoint, payload=payload, response=response)
            response.raise_for_status()
