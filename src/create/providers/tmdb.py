import uuid
from datetime import datetime

from src.create.providers.base_provider import BaseMediaProvider
from src.models import MediaListType, MediaList, MediaItem, MediaType, MediaProviderIds, MediaListItem


class TMDBListProviderResult:
    def __init__(self, id, title, overview, release_date):
        self.id = id
        self.title = title
        self.overview = overview
        self.release_date = release_date

    def __str__(self):
        return f"ID: {self.id}, Title: {self.title}, Overview: {self.overview}, Release Date: {self.release_date}"


class TMDBProvider(BaseMediaProvider):

    def __init__(self, config, filters=None, details=None, listType=MediaListType.COLLECTION):
        super().__init__(config)
        self.client = config.get_client('tmdb')
        self.details = details

        if filters is None:
            raise Exception("No filters provided. Cannot get list.")

    def _convert_filters_to_query_params(self):
        return {filter_item['type']: filter_item['value'] for filter_item in self.filters}

    def _map_tmdb_item_to_media_item(self, item):
        return MediaItem(
            mediaItemId=str(uuid.uuid4()),
            title=item['title'],
            year=item['release_date'].split('-')[0],
            description=item['overview'],
            releaseDate=item['release_date'],
            type=MediaType.MOVIE,
            providers=MediaProviderIds(
                tmdbId=item['id'],
            ),
        )

    async def get_list(self):
        db = self.get_db()
        filter_query_params = self._convert_filters_to_query_params()

        movie_data = self.client.discover_movie(**filter_query_params)
        movie_results = movie_data.get("results", [])

        media_list = MediaList(
            mediaListId=str(uuid.uuid4()),
            name=self.details.title,
            type=self.listType,
            description=self.details.description,
            sortName=self.details.sort_title,
            clientId='tmdb',
            createdAt=datetime.now(),
            creatorId=self.get_user().userId
        )

        await db.media_lists.insert_one(media_list.dict())

        media_list.items = []

        for item in movie_results:
            media_item = self._map_tmdb_item_to_media_item(item)
            media_list.items.append(
                await self.create_media_list_item(media_item, media_list,
                                                  provider_list_id=['id']))

        return media_list

    async def get_poster(self, item):
        poster_id = item['poster_path']
        poster_url = f"https://image.tmdb.org/t/p/original/{poster_id}"
        return poster_url

    # async def create_media_item(self, item, media_list):
    #     db = self.get_db()
    #
    #     poster_url = await self.get_poster(item)
    #
    #     media_item = MediaItem(
    #         mediaItemId=str(uuid.uuid4()),
    #         title=item['title'],
    #         year=item.get('release_date', None).split('-')[0],
    #         description=item.get('overview', None),
    #         releaseDate=item.get('release_date', None),
    #         type=MediaType.MOVIE,
    #         poster=poster_url,
    #         providers=MediaProviderIds(
    #             tmdbId=item['id'],
    #         ),
    #     )
    #
    #     existing_media_item = await self.get_existing_media_item(media_item)
    #
    #     if existing_media_item:
    #         media_item = await self.merge_and_update_media_item(media_item, existing_media_item)
    #
    #     media_list_item = MediaListItem(
    #         mediaListItemId=str(uuid.uuid4()),
    #         mediaListId=media_list.mediaListId,
    #         mediaItemId=media_item.mediaItemId,
    #         sourceId=item['id'],
    #         dateAdded=datetime.now()
    #     )
    #
    #     await db.media_list_items.insert_one(media_list_item.dict())
    #     media_list_item.item = media_item
    #
    #     return media_list_item
