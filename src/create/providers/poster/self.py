# Internal Poster Provider
# will be integrating this provider to use the MediaPoster object and we will want to
# find a way to generate a poster for a media item if it does not have one, or if it is selected.

from abc import ABC
from typing import Optional

from src.clients.emby import EmbyClient
from src.create.posters import MediaPosterImageCreator
from src.create.providers.poster import PosterProvider
from src.models import MediaItem, MediaImageType, MediaPoster


class MediaPosterProvider(PosterProvider, ABC):
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.log = config.get_logger(__name__)

    async def get_poster_from_source(self, config, media_item: MediaItem) -> Optional[str]:
        self.log.info('Attempting to create a poster', media_item=media_item.dict())

        # Attempt to create a poster
        media_poster = MediaPoster.from_media_item(media_item=media_item, type=MediaImageType.POSTER)

        image = await MediaPosterImageCreator(media_poster, config.get_logger).create()

        image.save('poster.png')

        # get a url to save as the poster.


        if not poster and self.next_provider:
            self.log.debug('Poster not found in Emby! Attempting to fetch from next provider.', media_item=media_item.dict())
            return await self.next_provider.get_poster(config, media_item=media_item)  # Ensure this is awaited if it's async
        return poster

