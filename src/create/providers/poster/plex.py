from abc import ABC
from typing import Optional, Union

from plexapi.server import PlexServer

from src.create.providers.poster import PosterProvider
from src.models import MediaItem, MediaProviderIds


class PlexPosterProvider(PosterProvider, ABC):

    def __init__(self, config):
        super().__init__()
        self.config = config

    async def get_poster_from_source(self, config, media_item: MediaItem) -> Union[str, None]:
        try:
            plex = self.get_plex_client()

            # Check if the MediaListItem has an associated MediaItem
            if media_item and media_item.providers:
                if poster_url := self.search_by_ids(plex, media_item.providers):
                    return poster_url

            # Fallback to title and year if ID search didn't return any result
            potential_matches = plex.search(title=media_item.title, year=media_item.year)

            for match in potential_matches:
                # Refine the logic if necessary
                if match.title == media_item.title and match.year == media_item.year:
                    return match.poster  # Assuming a poster attribute is available

        except Exception as e:
            # Logging the exception can be helpful for debugging.
            print(f"Error fetching poster from Plex: {e}")

        # If fetching from Plex fails or doesn't provide a poster, check the next provider.
        if self.next_provider:
            self.log.debug('Poster not found in Plex! Attempting to fetch from next provider.')
            return await self.next_provider.get_poster(media_item)
        return None

    def search_by_ids(self, plex, provider_ids: MediaProviderIds) -> Optional[str]:
        # NOTE: It's assumed PlexAPI provides a mechanism to search by IDs.
        # If it doesn't, this method should be modified accordingly.
        #
        # if provider_ids.imdbId:
        #     # Try searching by IMDb ID
        #     match = plex.searchByGuid(provider_ids.imdbId)
        #     if match:
        #         return match.poster

        # Continue with other IDs e.g. tvdbId, tmdbId, etc.
        # ... (Repeat the logic above for each ID)

        return None

    def get_plex_client(self) -> PlexServer:
        return self.config.get_client('plex')
