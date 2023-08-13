import requests
import json
import os
import time


class TraktClient:
    TRAKT_API_URL = "https://api.trakt.tv"

    def __init__(self, client_id, client_secret, redirect_uri="urn:ietf:wg:oauth:2.0:oob",
                 token_file="trakt_tokens.json"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.token_file = token_file
        self.tokens = self.load_or_get_tokens()

    def headers(self):
        return {
            "Content-Type": "application/json",
            "trakt-api-version": "2",
            "trakt-api-key": self.client_id,
            "Authorization": f"Bearer {self.get_access_token()}"
        }

    def load_or_get_tokens(self):
        if not os.path.exists(self.token_file):
            return self.get_new_tokens()

        with open(self.token_file, "r") as f:
            tokens = json.load(f)

        return self.refresh_tokens(tokens["refresh_token"])

    def get_new_tokens(self):
        print(f"Visit this URL: {self.TRAKT_API_URL}/oauth/authorize?response_type=code&client_id={self.client_id}&redirect_uri={self.redirect_uri}")
        pin_code = input("Enter the PIN shown on the page: ")

        response = requests.post(
            f"{self.TRAKT_API_URL}/oauth/token",
            data={
                "code": pin_code,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "redirect_uri": self.redirect_uri,
                "grant_type": "authorization_code"
            }
        )
        response.raise_for_status()
        tokens = response.json()

        with open(self.token_file, "w") as f:
            json.dump(tokens, f)

        return tokens

    def refresh_tokens(self, refresh_token):
        response = requests.post(
            f"{self.TRAKT_API_URL}/oauth/token",
            data={
                "refresh_token": refresh_token,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "redirect_uri": self.redirect_uri,
                "grant_type": "refresh_token"
            }
        )
        response.raise_for_status()
        tokens = response.json()

        with open(self.token_file, "w") as f:
            json.dump(tokens, f)

        return tokens

    def get_access_token(self):
        return self.tokens["access_token"]

    def request_with_retry(self, method, url, retries=5, **kwargs):
        for attempt in range(retries):
            if 'data' in kwargs and "refresh_token" in kwargs['data']:
                # Refreshing token, so don't use the authorization header
                headers = {
                    "Content-Type": "application/json",
                    "trakt-api-version": "2",
                    "trakt-api-key": self.client_id
                }
            else:
                headers = self.headers()

            response = requests.request(method, f"{self.TRAKT_API_URL}{url}", headers=headers, **kwargs)
            response.raise_for_status()
            return response.json()

    def create_list(self, name, description, privacy, display_numbers, allow_comments, sort_by, sort_how, **kwargs):
        data = {
            "name": name,
            "description": description,
            "privacy": privacy,
            "display_numbers": display_numbers,
            "allow_comments": allow_comments,
            "sort_by": sort_by,
            "sort_how": sort_how
        }
        data.update(kwargs)
        return self.request_with_retry("POST", "/users/me/lists", data=json.dumps(data))

    def update_list(self, list_id, **kwargs):
        return self.request_with_retry("PUT", f"/users/me/lists/{list_id}", data=json.dumps(kwargs))

    def delete_list(self, list_id):
        return self.request_with_retry("DELETE", f"/users/me/lists/{list_id}")



    # types = movies, shows, seasons, episodes, people
    def add_list_items(self, list_id, items,type):
        return self.request_with_retry("POST", f"/users/me/lists/{list_id}/items/{type}", data=json.dumps(items))

    def remove_list_items(self, list_id, items):
        return self.request_with_retry("POST", f"/users/me/lists/{list_id}/items/remove", data=json.dumps(items))


    def get_list(self, username, list_id_or_slug):
        return self.request_with_retry("GET", f"/users/{username}/lists/{list_id_or_slug}")

    def get_list_by_id(self, list_id):
        return self.request_with_retry("GET", f"/lists/{list_id}")

    def get_list_items_by_id(self, list_id):
        return self.request_with_retry("GET", f"/lists/{list_id}/items")


    def get_list_items(self, username, list_id_or_slug):
        return self.request_with_retry("GET", f"/users/{username}/lists/{list_id_or_slug}/items")

    def get_user_lists(self, username):
        return self.request_with_retry("GET", f"/users/{username}/lists")

    def get_favorites(self, type, sort):
        return self.request_with_retry("GET", f"/sync/favorites/{type}/{sort}")

    def add_to_favorites(self, arrayOfMediaObjects):
        return self.request_with_retry("POST", "/sync/favorites", data=json.dumps(arrayOfMediaObjects))

    def remove_from_favorite(self, arrayOfMediaObjects):
        return self.request_with_retry("POST", "/sync/favorites/remove", data=json.dumps(arrayOfMediaObjects))
