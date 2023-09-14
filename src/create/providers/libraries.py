


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

    def sync_libraries(self):
        for provider in self.providers:
            provider.sync_libraries()
