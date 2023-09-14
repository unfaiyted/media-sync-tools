from abc import abstractmethod, ABC

from src.create.providers.base_provider import BaseMediaProvider
from src.models import MediaList


class ListProvider(BaseMediaProvider, ABC):

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
