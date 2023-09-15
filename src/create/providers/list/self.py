import uuid
from datetime import datetime

from src.models import MediaListType, MediaList, MediaItem, MediaType, MediaProviderIds, MediaListItem


class SelfProvider:

    def __init__(self, config, filters=None, details=None, media_list: MediaList = None):
        self.config = config
        self.filters = filters
        self.details = details
        self.media_list = media_list

        if filters is None:
            raise Exception("No filters provided. Cannot get list.")

    def _convert_filters_to_query_params(self):
        return {filter_item['type']: filter_item['value'] for filter_item in self.filters}

    async def get_list(self):
        filter_query_params = self._convert_filters_to_query_params()

        # check if its existing mediaList in the database
        db = self.config.get_db()
        existing_media_list = None
        if self.media_list:
            existing_media_list = await db.media_lists.find_one({"mediaListId": self.media_list.mediaListId})

        media_list = self.media_list

        if existing_media_list:
            print('updating existing media list')
            media_list.mediaListId = existing_media_list['mediaListId']
            media_list.updatedAt = datetime.now()
            db.media_lists.update_one(
                {"mediaListId": existing_media_list["mediaListId"]},
                {"$set": media_list.dict()}
            )

        db.media_lists.insert_one(media_list.dict())

        if media_list.items is None:
            print('media list items is none')
            return media_list

        for item in media_list.items:
            print('-------------', item)
            media_list.items.append(await self.create_media_item(item, media_list))

        return media_list

    async def create_media_item(self, list_item: MediaListItem, media_list: MediaList):
        db = self.config.get_db()

        # poster_id = item['poster_path']
        # poster_url = f"https://image.tmdb.org/t/p/original/{poster_id}"

        # Check for existing mediaItem
        existing_media_item = None
        if list_item.item.mediaItemId:
            existing_media_item = await db.media_items.find_one({"mediaItemId": list_item.mediaItemId})

        if list_item.item.providers.tmdbId:
            existing_media_item = await db.media_items.find_one({"providers.tmdbId": list_item.item.providers.tmdbId})
        elif list_item.item.providers.imdbId:
            existing_media_item = await db.media_items.find_one({"providers.imdbId": list_item.item.providers.imdbId})
        elif list_item.item.providers.tvdbId:
            existing_media_item = await db.media_items.find_one({"providers.tvdbId": list_item.item.providers.tvdbId})

        if existing_media_item:
            print('updating existing media item')
            list_item.mediaItemId = existing_media_item['mediaItemId']

            db.media_items.update_one(
                {"mediaItemId": existing_media_item["mediaItemId"]},
                {"$set": list_item.dict()}
            )
        else:
            print('inserting new media item')
            db.media_items.insert_one(list_item.dict())

        existing_media_list_item = None
        if list_item.mediaListItemId:
            existing_media_list_item = await db.media_list_items.find_one(
                {"mediaListItemId": list_item.mediaListItemId})

        if existing_media_list_item:
            print('updating existing media list item')
            list_item.mediaListItemId = existing_media_list_item['mediaListItemId']

            db.media_list_items.update_one(
                {"mediaListItemId": existing_media_list_item["mediaListItemId"]},
                {"$set": list_item.dict()}
            )

        db.media_list_items.insert_one(list_item.dict())

        return list_item
