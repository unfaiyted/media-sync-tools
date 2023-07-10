import os
import requests


class PlexManager:
    def __init__(self, client, account):
        self.client = client
        self.account = account

    @staticmethod
    def save_plex_poster(poster_url, filename="poster.jpg"):
        # Create directories if missing
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        poster_response = requests.get(poster_url, stream=True)
        if poster_response.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in poster_response.iter_content(1024):
                    f.write(chunk)
        return poster_response

