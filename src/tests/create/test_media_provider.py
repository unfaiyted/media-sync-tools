from datetime import datetime

import pytest
import asyncio
from unittest.mock import MagicMock

from models import MediaItemType
from src.create.providers.media_provider import MediaProvider
from src.models import MediaItem, MediaList, MediaProviderIds
from unittest.mock import AsyncMock



# Create a dummy class that inherits from the abstract MediaProvider to make it instantiable
class DummyMediaProvider(MediaProvider):
    def get_client(self):
        pass


@pytest.fixture
def setup_media_provider():
    config = MagicMock()
    config.get_db.return_value = MagicMock()
    config.get_logger.return_value = MagicMock()
    provider = DummyMediaProvider(config, "client_id")
    return provider


@pytest.mark.asyncio
async def test_get_existing_media_item_none(setup_media_provider):
    provider = setup_media_provider
    provider.db.media_items.find_one = AsyncMock(return_value={"title": "Inception", "year": 2010, "type": "MOVIE"})
    media_item = MediaItem(providers=None, type=MediaItemType.MOVIE, title="Inception", year=2010)
    result = await provider.get_existing_media_item(media_item)
    assert result is None


@pytest.mark.asyncio
async def test_get_existing_media_item_by_id(setup_media_provider):
    provider = setup_media_provider
    provider.db.media_items.find_one = AsyncMock(return_value={"title": "Inception", "year": 2010, "type": "MOVIE"})
    media_item = MediaItem(providers=MediaProviderIds(tmdb=12345), type="MOVIE", title="Inception", year=2010)
    result = await provider.get_existing_media_item(media_item)
    assert result.title == "Inception"
    assert result.year == '2010'


@pytest.mark.asyncio
async def test_merge_and_update_media_item(setup_media_provider):
    provider = setup_media_provider
    media_item_1 = MediaItem(title="Inception", year=None, type=MediaItemType.MOVIE)
    media_item_2 = MediaItem(title="Inception", year=2010, type=MediaItemType.MOVIE)
    result = await provider.merge_and_update_media_item(media_item_1, media_item_2)
    assert result.title == "Inception"
    assert result.year == '2010'


@pytest.mark.asyncio
async def test_create_media_list_item(setup_media_provider):
    provider = setup_media_provider
    provider.get_existing_media_item = AsyncMock(return_value=None)
    # provider.merge_and_update_media_item = MagicMock(return_value=MediaItem(title="Inception", type=MediaItemType.MOVIE, year=2010))
    media_item = MediaItem(mediaItemId="1212", title="Inception", type=MediaItemType.MOVIE, year=2010)
    media_list = MediaList(mediaListId="list_123", clientId="client_123", name="Test List", creatorId="user_123", type="COLLECTION", sortName="Test List", createdAt=datetime.now())
    result = await provider.create_media_list_item(media_item, media_list)
    assert result.mediaItemId == media_item.mediaItemId

# Add more tests as needed...
