from abc import ABC, abstractmethod
from typing import Optional, Union

from plexapi.server import PlexServer

from src.clients.tmdb import TmdbClient
from src.models import MediaItem, MediaProviderIds


class PosterProvider(ABC):

    def __init__(self):
        self.next_provider = None

    def set_next(self, provider: 'PosterProvider'):
        """
        Set the next provider in the chain.
        """
        self.next_provider = provider
        return provider  # This allows for method chaining

    @abstractmethod
    async def get_poster_from_source(self, config, media_item: MediaItem) -> Optional[str]:
        """
        Retrieve poster from specific provider's source. To be implemented by each derived provider.
        """
        pass

    async def get_poster(self, config, media_item: MediaItem) -> Optional[str]:
        """
        Attempt to get the poster using the current provider.
        If not available, delegate to the next provider in the chain.
        """
        poster = await self.get_poster_from_source(config, media_item)
        if not poster and self.next_provider:
            return await self.next_provider.get_poster(config, media_item)
        return poster


class TraktPosterProvider(PosterProvider, ABC):
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config

    async def get_poster_from_source(self, config, media_item: MediaItem) -> Optional[str]:
        emby = self.config.get_client('emby')

        # Not implemented for Trakt
        poster = None
        # Attempt to fetch from Emby
        if not poster and self.next_provider:
            return await self.next_provider.get_poster(media_item)  # Ensure this is awaited if it's async
        return poster



class EmbyPosterProvider(PosterProvider, ABC):
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config

    async def get_poster_from_source(self, config, media_item: MediaItem) -> Optional[str]:
        emby = self.config.get_client('emby')

        # Attempt to fetch from Emby
        poster = await self.fetch_from_emby(media_item, emby)
        if not poster and self.next_provider:
            return await self.next_provider.get_poster(media_item)  # Ensure this is awaited if it's async
        return poster

    async def fetch_from_emby(self, media_item, emby):
        embyItem = await emby.search_emby_for_external_ids(media_item=media_item)

        if embyItem is None:
            print('Item not found in Emby')
            return None

        if poster_id := embyItem['ImageTags'].get('Primary'):
            return f"{emby.server_url}/emby/Items/{embyItem['Id']}/Images/Primary?api_key={emby.api_key}&X-Emby-Token={emby.api_key}"
        else:
            return None


class TmdbPosterProvider(PosterProvider, ABC):
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.log = config.get_logger(__name__)

    async def get_poster_from_source(self,config, media_item: MediaItem) -> Optional[str]:
        tmdb: TmdbClient = self.config.get_client('tmdb')
        # Attempt to fetch from Tmdb
        poster = tmdb.get_movie_poster_path(media_item.providers.tmdbId, full_path=True)
        self.log.info(f'Fetched poster from Tmdb', poster=poster)

        if poster is None:
            self.log.info(f'Poster not found by Tmdb Id! Attempting to fetch by name and year.')
            if movie := tmdb.get_movie_by_name_and_year(media_item.title, media_item.year):
                self.log.info(f'Found movie by name and year', movie=movie)
                poster = tmdb.get_movie_poster_path(movie['id'], full_path=True)
                self.log.info(f'Fetched poster from Tmdb', poster=poster)

        if poster is None and self.next_provider:
            self.log.info(f'Poster not found in Tmdb! Attempting to fetch from next provider.')
            return await self.next_provider.get_poster(media_item)  # Ensure this is awaited if it's async
        return poster


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

