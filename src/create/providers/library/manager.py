from src.create.providers.library import LibraryProvider
from src.create.providers.library.emby import EmbyLibraryProvider
from src.create.providers.library.jellyfin import JellyfinLibraryProvider
from src.create.providers.library.plex import PlexLibraryProvider
from src.create.providers.provider_manager import ProviderManager


class LibraryProviderManager:

    def __init__(self, config, *providers):
        """
        Initialize the LibraryProviderManager.
        :param config:
        :param providers:
        """
        self.config = config
        self.log = config.get_logger(__name__)
        # TODO: Get user config to determine which providers to use dynamically
        emby = EmbyLibraryProvider(config=config)
        jellyfin = JellyfinLibraryProvider(config=config)
        plex = PlexLibraryProvider(config=config)

        if not providers:
            providers = [emby, jellyfin, plex]

        self.providers = providers
        self.log.debug("LibraryProviderManager initialized", providers=self.providers)

    async def sync_libraries(self):
        for provider in self.providers:
            self.log.debug("Syncing libraries from provider", provider=provider)
            await provider.sync_libraries()

    async def fetch_all_libraries(self):
        all_libraries = []
        self.log.debug("Fetching all libraries")
        for provider in self.providers:
            self.log.debug("Fetching libraries from provider", provider=provider)
            libraries = await provider.get_libraries()
            self.log.debug("Fetched libraries from provider", provider=provider, libraries=libraries)
            all_libraries.extend(libraries)
        return all_libraries

    async def sync_specific_library(self, library_id):
        target_provider = None
        target_library = None

        for provider in self.providers:
            libraries = await provider.get_libraries()
            for library in libraries:
                if library.libraryId == library_id or library.sourceId == library_id:
                    target_provider = provider
                    target_library = library
                    break

        if target_provider and target_library:
            await target_provider.sync_library_items(target_library)
            return f"Synced {target_library.name} from {target_provider.__class__.__name__}"
        else:
            return "No matching library found"

    async def sync_all_libraries_items(self):
        for provider in self.providers:
            # get all the libraries from a provider and sync them each
            libraries = await provider.get_libraries()
            for library in libraries:
                await provider.sync_library_items(library)
