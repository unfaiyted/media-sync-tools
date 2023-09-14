from abc import ABC
from typing import Optional

from src.clients.tmdb import TmdbClient
from src.create.providers.poster import PosterProvider
from src.models import MediaItem


class TmdbPosterProvider(PosterProvider, ABC):
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.log = config.get_logger(__name__)

    async def get_poster_from_source(self, config, media_item: MediaItem) -> Optional[str]:
        self.log.info('Fetching poster from Tmdb', media_item=media_item.dict())
        tmdb: TmdbClient = self.config.get_client('tmdb')
        # Attempt to fetch from Tmdb
        poster = tmdb.get_movie_poster_path(media_item.providers.tmdbId, full_path=True)
        self.log.info('Fetched poster from Tmdb', poster=poster)

        if poster is None:
            self.log.info(
                'Poster not found! Attempting to fetch by name and year.'
            )
            if movie := tmdb.get_movie_by_name_and_year(media_item.title, media_item.year):
                self.log.info('Found movie by name and year', movie=movie)
                poster = tmdb.get_movie_poster_path(movie['id'], full_path=True)
                self.log.info('Fetched poster from Tmdb', poster=poster)

        if poster is None and self.next_provider:
            self.log.info(
                'Poster not found in Tmdb! Attempting to fetch from next provider.'
            )
            return await self.next_provider.get_poster(media_item)  # Ensure this is awaited if it's async
        return poster
