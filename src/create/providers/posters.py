from abc import ABC, abstractmethod
from typing import Optional, Union

class PosterProvider(ABC):

    def __init__(self):
        self._next_provider = None

    def set_next(self, provider: "PosterProvider") -> "PosterProvider":
        self._next_provider = provider
        return provider  # For chaining

    @abstractmethod
    async def get_poster(self, media_item: 'MediaListItem') -> Union[str, None]:
        pass
