from abc import abstractmethod, ABC

from src.create.providers.base_provider import BaseMediaProvider
from src.create.providers.poster.manager import PosterProviderManager
from src.models import MediaList


class ListProvider(BaseMediaProvider, ABC):

    def __init__(self, config):
        super().__init__(config)
        self.config = config
        self.log = config.get_logger(__name__)
        self.poster_manager = PosterProviderManager(config=config)



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
