from src.create.providers.library import LibraryProvider
from src.create.providers.library.emby import EmbyLibraryProvider
from src.create.providers.library.jellyfin import JellyfinLibraryProvider
from src.create.providers.library.plex import PlexLibraryProvider
from src.create.providers.managers import ProviderManager
from src.models import Library


class LibraryProviderManager:

    def __init__(self, config, *providers):
        """
        Initialize the LibraryProviderManager.
        :param config:
        :param providers:
        """
        self.config = config
        self.log = config.get_logger(__name__)
        emby = EmbyLibraryProvider(config=config)
        jellyfin = JellyfinLibraryProvider(config=config)
        plex = PlexLibraryProvider(config=config)

        # Add any other providers you have
        self.provider_manager = ProviderManager(emby, jellyfin, plex)
        self.log.debug("LibraryProviderManager initialized", provider_manager=self.provider_manager)
        self.providers = [p for p in providers if isinstance(p, LibraryProvider)]

    def sync_libraries(self, libraries: list[Library] = None):
        for provider in self.providers:
            provider.sync_libraries(libraries=libraries)

    def sync_library_items(self, library: Library):
        for provider in self.providers:
            provider.sync_library_items(library=library)

    def sync_all_library_items(self):
        for provider in self.providers:
            provider.sync_all_library_items()