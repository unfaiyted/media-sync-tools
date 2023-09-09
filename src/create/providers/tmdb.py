import uuid
from datetime import datetime
from typing import Optional

from create.providers.posters import PosterProvider
from src.models import MediaListType, MediaList, MediaItem, MediaType, MediaProviderIds, MediaListItem


class TMDBListProviderResult:
    def __init__(self, id, title, overview, release_date):
        self.id = id
        self.title = title
        self.overview = overview
        self.release_date = release_date

    def __str__(self):
        return f"ID: {self.id}, Title: {self.title}, Overview: {self.overview}, Release Date: {self.release_date}"


class TMDBProvider:

    def __init__(self, config, filters=None, details=None, listType=MediaListType.COLLECTION):
        self.config = config
        self.listType = listType
        self.client = config.get_client('tmdb')
        self.filters = filters
        self.details = details

        if filters is None:
            raise Exception("No filters provided. Cannot get list.")

    def _convert_filters_to_query_params(self):
        return {filter_item['type']: filter_item['value'] for filter_item in self.filters}

    async def get_list(self):
        db = self.config.get_db()
        filter_query_params = self._convert_filters_to_query_params()

        movie_data = self.client.discover_movie(**filter_query_params)
        movie_results = movie_data.get("results", [])

        media_list = MediaList(
                mediaListId=str(uuid.uuid4()),
                name=self.details.title,
                type=self.listType,
                description=self.details.description,
                # filters=self.filters,
                sortName=self.details.sort_title,
                clientId='tmdb',
                createdAt=datetime.now(),
                creatorId=self.config.get_user().userId
            )

        db.media_lists.insert_one(media_list.dict())

        media_list.items = []

        for item in movie_results:
            print('-------------', item)
            media_list.items.append(await self.create_media_item(item, media_list))

        return media_list

    async def get_poster(self, item):
        poster_id = item['poster_path']
        poster_url = f"https://image.tmdb.org/t/p/original/{poster_id}"
        return poster_url

    async def create_media_item(self, item, media_list):
        db = self.config.get_db()

        poster_url = self.get_poster(item)

        media_item = MediaItem(
            mediaItemId=str(uuid.uuid4()),
            title=item['title'],
            year=item.get('release_date', None).split('-')[0],
            description=item.get('overview', None),
            releaseDate=item.get('release_date', None),
            type=MediaType.MOVIE,
            poster=poster_url,
            providers=MediaProviderIds(
                tmdbId=item['id'],
            ),
        )

        # Check for existing mediaItem
        existing_media_item = None
        if media_item.providers.tmdbId:
            existing_media_item = await db.media_items.find_one({"providers.tmdbId": media_item.providers.tmdbId})

        if existing_media_item:
            print('updating existing media item')
            media_item.mediaItemId = existing_media_item['mediaItemId']

            db.media_items.update_one(
                {"mediaItemId": existing_media_item["mediaItemId"]},
                {"$set": media_item.dict()}
            )
        else:
            print('inserting new media item')
            db.media_items.insert_one(media_item.dict())

        media_list_item = MediaListItem(
            mediaListItemId=str(uuid.uuid4()),
            mediaListId=media_list.mediaListId,
            mediaItemId=media_item.mediaItemId,
            sourceId=item['id'],
            dateAdded=datetime.now()
        )

        db.media_list_items.insert_one(media_list_item.dict())

        media_list_item.item = media_item

        return media_list_item

    class TmdbPosterProvider(PosterProvider):
    def get_poster(self, media_item_id: str) -> Optional[str]:
        # Logic for fetching the poster from TMDb
        poster = ...
        if not poster and self.next_provider:
            return self.next_provider.get_poster(media_item_id)
        return poster
