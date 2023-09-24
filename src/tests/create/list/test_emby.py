import pytest
from unittest.mock import Mock, patch
from src.create.providers.list.emby import EmbyListProvider
from src.models import EmbyFilters, MediaListType


# 1. Set up necessary imports

@pytest.fixture
def mock_config():
    config = Mock()
    config.get_logger.return_value = Mock()
    config.get_db.return_value = Mock()
    config.get_user.return_value = Mock(userId="test_user")
    config.get_client.return_value = Mock()
    config.get_root_path.return_value = "/path/to/root"
    return config


@pytest.fixture
def mock_emby_client():
    client = Mock()
    client.server_url = "http://localhost:8096"
    client.api_key = "test_api_key"
    return client


# 2. Create test setup functions

def test_emby_list_provider_initialization(mock_config):
    emby_provider = EmbyListProvider(config=mock_config)
    assert emby_provider.config == mock_config


@patch('src.clients.emby.EmbyClient', autospec=True)
def test_get_list_by_id(mock_emby_client_class, mock_config):
    # Define the mock response for the client
    mock_list_response = {
        "Name": "Test List",
        "Id": "test_id",
        "SortName": "Test Sort Name",
        "Type": "Collection"
    }

    # Set return values for the mock client
    mock_emby_client_instance = mock_emby_client_class.return_value
    mock_emby_client_instance.get_list.return_value = mock_list_response

    # Pass the mocked client to the EmbyProvider directly (dependency injection)
    emby_provider = EmbyListProvider(config=mock_config, filters=EmbyFilters(clientId="emby", listId="test_id"), client=mock_emby_client_instance)

    # Call the method and check the result
    result = emby_provider.get_list_by_id("test_id")

    mock_emby_client_instance.get_list.assert_called_once_with("test_id")

    # Assertions for the behavior
    assert result.name == 'Test List'

