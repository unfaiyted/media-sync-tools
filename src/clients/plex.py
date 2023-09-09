import os
import requests
import string


class PlexManager:
    def __init__(self, config):
        self.client = config.get_client("plex")
        # self.account = config.get_account("plex")
        self.guidLookup = self.get_all("TV Shows")

    def get_all(self, library_name, limit=100):
        alphabet = string.ascii_uppercase

        for letter in alphabet:
            # Perform a search query with the title filter
            items = self.client.library.section(library_name).search(
                title__startswith=letter,
                limit=limit
            )

            # Process the retrieved items
            print(f"Processing {len(items)} items starting with {letter}")
            for item in items:
                # Do something with each item
                print(item.title)
                self.guidLookup[item.guid] = item
                self.guidLookup.update({guid.id: item for guid in item.guids})

        return self.guidLookup

    def get_by_guid(self, guid):
        return self.guidLookup.get(guid)

    # def create_collection(self, title, items):

    # def create_playlist(self, title, items):

    @staticmethod
    def save_poster(poster_url, filename="poster.jpg"):
        # Create directories if missing
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        poster_response = requests.get(poster_url, stream=True)
        if poster_response.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in poster_response.iter_content(1024):
                    f.write(chunk)
        return poster_response
