import os
from typing import List

import requests
import string

from plexapi.library import LibrarySection

from src.models import MediaListType


class PlexManager:
    def __init__(self, config):
        self.client = config.get_client("plex")
        self.log = config.get_logger(__name__)
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
            self.log.info(f"Processing {len(items)} items starting with {letter} ", letter=letter, len=len(items))
            for item in items:
                self.log.debug("Processing item", title=item.title, guid=item.guid, guids=item.guids)
                # Do something with each item
                self.guidLookup[item.guid] = item
                self.guidLookup.update({guid.id: item for guid in item.guids})

        return self.guidLookup

    def get_by_guid(self, guid):
        return self.guidLookup.get(guid)

    # def create_collection(self, title, items):

    # def create_playlist(self, title, items):

    @staticmethod
    def save_poster(log, poster_url, filename="poster.jpg", ):
        log.debug("Saving poster", poster_url=poster_url, filename=filename)
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        poster_response = requests.get(poster_url, stream=True)
        if poster_response.status_code == 200:
            log.debug("Saving poster", poster_url=poster_url, filename=filename)
            with open(filename, 'wb') as f:
                for chunk in poster_response.iter_content(1024):
                    log.debug("Saving poster chunk", poster_url=poster_url, filename=filename)
                    f.write(chunk)

        log.debug("Saved poster", poster_url=poster_url, filename=filename)
        return poster_response

    def search_libraries(self, filters):
        self.log.debug("Searching libraries", filters=filters)

        if 'sort' not in filters:
            self.log.debug("No sort filter provided. Setting default sort to titleSort:asc")
            filters['sort'] = 'titleSort:asc'

        if 'maxresults' not in filters or filters['maxresults'] is None:
            self.log.debug("No maxresults filter provided. Setting default maxresults to 100")
            filters['maxresults'] = 100  # Set a default value if you want

        combined_results = []

        libraries: List[LibrarySection] = self.client.library.sections()
        for library in libraries:
            self.log.debug("Searching library", library_title=library.title)
            try:
                self.log.debug("Searching library", library_title=library.title)
                search_results = library.search(**filters)
                combined_results.extend(search_results)
                self.log.debug("Added results", library_title=library.title, len=len(search_results))
            except Exception as e:
                self.log.error("Error searching library", library_title=library.title, error=e)
                continue

        self.log.debug("Returning combined results", len=len(combined_results))
        return combined_results

    def search_lists_by_type(self, listId, type):
        try:
            if type == MediaListType.COLLECTION:
                self.log.debug("Searching collection", listId=listId)
                return self.client.fetchItem(int(listId))
            elif type == MediaListType.PLAYLIST:
                self.log.debug("Searching playlist", listId=listId)
                return self.client.playlist(title=listId)
        except Exception as e:
            self.log.error("Error searching list", listId=listId, error=e, type=type, args=e.args)
            return None

    def search_list_by_id(self, listId):
        plex_list = self.search_lists_by_type(listId, MediaListType.COLLECTION)
        if plex_list is None:
            plex_list = self.search_lists_by_type(listId, MediaListType.PLAYLIST)
        return plex_list

    def search_list_items(self, media, type):
        if type == MediaListType.COLLECTION:
            self.log.debug("Searching collection items", media=media)
            if media:
                if hasattr(media, 'children'):
                    self.log.debug("Collection has children", children=media.children)
                    return media.children
        elif type == MediaListType.PLAYLIST:
            self.log.debug("Searching playlist items", media=media)
            if media:
                self.log.debug("Playlist has items", items=media.items())
                return media.items()

        self.log.debug("No items found", media=media)
        return []

    @staticmethod
    def extract_external_ids(plex_item):
        ids = {}

        if not plex_item.guid:
            return ids

            # Check for IMDb
        if "imdb://" in plex_item.guid:
            ids['imdb'] = plex_item.guid.split('imdb://')[1].split('?')[0]

            # Check for TheMovieDB
        if "themoviedb://" in plex_item.guid:
            ids['tmdb'] = plex_item.guid.split('themoviedb://')[1].split('?')[0]

            # You can continue adding checks for other ID types in a similar manner...
            # Check for TVDB
        if "thetvdb://" in plex_item.guid:
            ids['tvdb'] = plex_item.guid.split('thetvdb://')[1].split('?')[0]

        return ids
