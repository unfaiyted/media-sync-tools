import pytest
from unittest.mock import Mock
from src.create.providers.media_provider_manager import MediaProviderManager
from src.models import MediaItem, Filters
from unittest.mock import create_autospec, patch


# Mock ConfigManager to avoid using actual configuration
@pytest.fixture
def mock_config():
    return Mock()


@pytest.fixture
def media_provider_manager(mock_config):
    with patch("src.create.providers.media_provider_manager.ListProviderManager", autospec=True), \
        patch("src.create.providers.media_provider_manager.PosterProviderManager", autospec=True), \
        patch("src.create.providers.media_provider_manager.LibraryProviderManager", autospec=True):
        return MediaProviderManager(mock_config)


def test_get_poster(media_provider_manager):
    mock_media_item = Mock(spec=MediaItem)
    result = media_provider_manager.get_poster(mock_media_item)

    # Your assertions based on expected behavior,
    # For instance, if you expect it to call the get_poster of poster_provider_manager:
    media_provider_manager.poster_provider_manager.get_poster.assert_called_once_with(mock_media_item, None)


def test_get_list(media_provider_manager):
    mock_client_id = "client123"
    mock_filters = Mock(spec=Filters)
    result = media_provider_manager.get_list(mock_client_id, mock_filters)

    # Your assertions
    media_provider_manager.list_provider_manager.get_list.assert_called_once_with(mock_client_id, mock_filters)

# Continue with tests for other methods...

# For methods that use real classes like TmdbPosterProvider, you'll want to mock those too.
# For example, when testing get_list_with_posters, you'll want to mock TmdbPosterProvider and
# other dependencies to ensure they don't make actual external calls.
