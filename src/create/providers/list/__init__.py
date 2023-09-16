from abc import abstractmethod, ABC

from src.models import MediaItem, ProviderType
from src.create.providers.base_provider import BaseMediaProvider
from src.create.providers.poster.manager import PosterProviderManager
from src.models import MediaList


class ListProvider(BaseMediaProvider, ABC):

    def __init__(self, config, client_id: str = None):
        super().__init__(config, client_id=client_id)
        self.config = config
        self.provider_type = ProviderType.LIST
        self.client_id = client_id
        self.log = config.get_logger(__name__)
        self.poster_manager = PosterProviderManager(config=config)

    async def get_client(self):
        return self.config.get_client(self.client_id)

    @abstractmethod
    def get_list_by_id(self, list_id: str) -> MediaList:
        """
        Retrieve MediaList from provider.
        :return:
        """
        pass

    @abstractmethod
    def get_list(self):
        """
        Retrieve MediaList from provider.
        :return:
        """
        pass

    @abstractmethod
    def upload_list(self, media_list: MediaList):
        """
        Upload MediaList to provider.
        :return:
        """
        pass

    async def add_items_to_media_list(self, media_list, provider_name,  provider_items):
        media_list.items = []

        if provider_items is None:
            self.log.error("Error creating or no list found", provider_items=provider_items)
            return None

        for item in provider_items:
            self.log.debug("Creating media item", item=item, media_list=media_list)
            media_item = MediaItem.from_provider_type(provider_name, item, self.log)
            media_list.items.append(
                await self.create_media_list_item(media_item, media_list))

        return media_list
