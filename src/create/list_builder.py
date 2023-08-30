from src.create.providers.emby import EmbyProvider
from src.create.providers.plex import PlexProvider
from src.create.providers.tmdb import TMDBProvider
# from src.create.providers.trakt import TraktProvider
from src.create.posters import PosterImageCreator
from src.create.providers.ai import AiProvider
from src.create.providers.mdb import MdbProvider
from src.create.providers.trakt import TraktProvider
from src.models import MediaListType, MediaList, MediaPoster, MediaItem


class ProcessedFilter:
    def __init__(self, filter, process_type='ai'):
        self.filter = filter
        self.processed = False
        self.process_type = process_type
        self.filter_message = ''
        self.media_list = []

    def process(self, process_type='ai'):
        print(f'Processing filters')

        type = self.filter.get('type', None)
        if type == 'genre':
            self._process_genre_filter(self.filter, process_type)
        elif type == 'year':
            self._process_year_filter(self.filter, process_type)
        elif type == 'is_watched':
            self._process_watched_filter(self.filter, process_type)

    def _process_genre_filter(self, filter, process_type='ai'):

        if process_type == 'ai':
            genre = filter.get('value', 'Any')
            genere_list = genre.split(',')
            processed_genres = []

            for genre in genere_list:
                genre = genre.strip()
                if genre.startswith('!'):
                    genre = genre[1:]
                    processed_genres.append(f'NOT {genre}')

            self.message = f'Genres: {",".join(processed_genres)}'

    def _process_year_filter(self, filter, process_type='ai'):
        if process_type == 'ai':
            year = filter.get('value', None)
            operator = filter.get('op', '=')
            if year is not None:
                self.message = f'Year {operator} {year}'

    def _process_watched_filter(self, filter, process_type='ai'):
        if process_type == 'ai':
            watched = filter.get('value', 'true')
            if watched is not None:
                if watched == 'true':
                    # get a list of played media items
                    self.message = 'IsPlayed: true'
                    self.media_list = []
                else:
                    # get a list of unplayed media items
                    self.message = 'IsPlayed: false'
                    self.media_list = []


class ListBuilder:

    def __init__(self, config, list_type=MediaListType.COLLECTION, list=None, media_list=None):
        self.config = config
        self._ai_list = []
        self.rules = []
        self.filters = []
        self.title = None
        self.sort_title = None
        self.type = list_type
        self.emby = config.get_client('emby')
        self.retry_count = 3
        self.description = f'Automatically generated {list_type} list'
        self.sort_title = self.title
        self.provider = None
        self.name = None
        self.library_name = None
        self.media_types = None
        self.media_list = []  # list of media objects to reference when building the list
        self.icon_path = f'{config.root_path}/resources/icons/tv.png'
        self.add_missing = False
        self.limit = 25
        self.delete_existing = False
        self.new_list_id = None

        self.poster = {
            'enabled': True,
            'bg_image_query': self.title,
            'bg_color': 'magenta-purple',

        }

        if(media_list is not None):
            print(media_list)
            MediaItem.update_forward_refs()
            media_list = MediaList(**media_list)
            print(f'Initializing list from media list {media_list.name}')
            self.media_list = media_list
            # self.description = media_list.description
            self.title = media_list.name
            self.sort_title = media_list.sortName
            self.type = media_list.type


        if list is not None:
            self._init_list(list)

    def _init_list(self, list):
        print(f'Initializing list {list}')
        self.set_title(list.get("name", self.title))
        self.set_description(list.get("description", self.description))
        self.set_sort_title(list.get("sort_name", self.title))
        self.set_library_name(list.get("library_name", None))

        self.set_icon_path(list.get('icon_path', self.icon_path))
        self.set_provider(list.get('provider', self.provider))

        media_types = list.get('media_types', None)

        if media_types is not None:
            self.set_media_types(media_types)

        options = list.get('options', None)

        if options is not None:
            self.set_add_missing(options.get('add_missing', self.add_missing))
            self.set_delete_existing(options.get('delete_existing', self.delete_existing))
            self.set_limit(options.get('limit', self.limit))

        self.set_filters(list.get('filters', self.filters))

        if list.get('poster', None) is not None:
            # set poster values
            self.poster['enabled'] = list['poster'].get('enabled', self.poster['enabled'])
            self.poster['bg_image_query'] = list['poster'].get('bg_image_query', self.poster['bg_image_query'])

    def set_type(self, type):  # type can be 'Collection' or 'Playlist'
        self.type = type
        return self

    def set_rule(self, type):
        self.rules.append(type)
        return self

    def set_title(self, title):  # title of the list
        self.title = title
        return self

    def set_description(self, description):  # description of the list
        self.description = description
        return self

    def set_limit(self, size):  # total size of the list
        self.limit = size
        return self

    def set_sort_title(self, sort_title):
        self.sort_title = sort_title
        return self

    def set_retry_count(self, count):
        self.retry_count = count
        return self

    def set_library_name(self, name):
        self.library_name = name
        return self

    def set_icon_path(self, path: str):
        self.icon_path = path
        return self

    def set_media_list(self, list, after=None, before=None):
        self.media_list = list
        return self

    def set_add_missing(self, enabled="false"):
        self.add_missing = enabled
        return self

    def set_filter(self, filter):
        self.filters.append(filter)
        return self

    def set_filters(self, filters):
        self.filters = filters
        return self

    def set_provider(self, provider):
        self.provider = provider
        return self

    def set_delete_existing(self, enabled="false"):
        self.delete_existing = enabled
        return self

    def set_media_types(self, types):
        self.media_types = types
        return self

    def _get_media_type_for_emby(self):
        if self.media_types is not None and len(self.media_types) == 1:
            return self.media_types[0]
        else:
            return 'Mixed'

    # def _create_collection(self, rules):
    #
    # def _create_playlist(self):
    def print_list(self):
        print(f'List: {self.title}')
        print(f'Rules: {self.rules}')
        print(f'Filters: {self.filters}')
        print(f'Limit: {self.limit}')
        print(f'Library: {self.library_name}')
        print(f'Icon Path: {self.icon_path}')
        print(f'Add Missing: {self.add_missing}')
        print(f'Delete Existing: {self.delete_existing}')
        print(f'Media Types: {self.media_types}')
        print(f'Provider: {self.provider}')
        print(f'Sort Title: {self.sort_title}')
        print(f'Description: {self.description}')
        print(f'Retry Count: {self.retry_count}')
        print(f'Media List: {self.media_list}')

    async def _get_media_list_from_provider(self):

        provider_mapping = {
            'self': (lambda: print('Using media list')),
            'ai': (lambda: AiProvider(self.media_types, self.description, self._process_filters('ai'), self.limit)),
            'mdb': (lambda: MdbProvider(self.config, self.filters, listType=self.type)),
            'trakt': (lambda: TraktProvider(self.config, self.filters,details=self, listType=self.type)),
            'tmdb': (lambda: TMDBProvider(self.config, self.filters, details=self, listType=self.type)),
            'plex': (lambda: PlexProvider(self.config, self.filters, listType=self.type)),
            'emby': (lambda: EmbyProvider(self.config, self.filters, details=self, listType=self.type))
        }

        if self.provider in provider_mapping:
            if self.provider != 'self':
                print(f'Using {self.provider.capitalize()} list')
                try:
                    self.media_list = await provider_mapping[self.provider]().get_list()
                    return self.media_list
                except Exception as e:
                    print(f'Error getting list from provider {self.provider}: {e}, {e.args}', )
                    import traceback
                    traceback.print_exc()
                print('Media List', self.media_list)
            else:
                provider_mapping[self.provider]()  # Only prints a message for 'self'
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

        return None

    async def _save_media_list_to_provider(self, provider: str):

        provider_mapping = {
            'self': (lambda: print('Using media list')),
            'ai': (lambda: AiProvider(self.media_types, self.description, self._process_filters('ai'), self.limit)),
            'mdb': (lambda: MdbProvider(self.config, self.filters, listType=self.type)),
            'trakt': (lambda: TraktProvider(self.config, self.filters, details=self, listType=self.type)),
            'tmdb': (lambda: TMDBProvider(self.config, self.filters, details=self, listType=self.type)),
            'plex': (lambda: PlexProvider(self.config, self.filters, listType=self.type)),
            'emby': (lambda: EmbyProvider(self.config, self.filters, details=self, listType=self.type))
        }

        if provider in provider_mapping:
            if provider != 'self':
                print(f'Using {provider.capitalize()} list')
                print('Media List', self.media_list)
                try:
                    media_list = provider_mapping[provider]().upload_list(self.media_list)
                except Exception as e:
                    print(f'Error saving list to provider {provider}: {e}, {e.args}', )
                    import traceback
                    traceback.print_exc()
            else:
                provider_mapping[provider]()  # Only prints a message for 'self'
        else:
            raise ValueError(f"Unknown provider: {provider}")

        return self.media_list

    def _save_poster_to_provider(self, item_id: str, poster: MediaPoster or str):

        provider_mapping = {
            'self': (lambda: print('Using media list')),
            'plex': (lambda: PlexProvider(self.config, self.filters, listType=self.type)),
            'emby': (lambda: EmbyProvider(self.config, self.filters, details=self, listType=self.type))
        }

        if self.provider in provider_mapping:
            if self.provider != 'self':
                print(f'Using {self.provider.capitalize()} list')
                print('Media List', self.media_list)
                try:
                    provider_mapping[self.provider]().save_poster(item_id, poster)
                except Exception as e:
                    print(f'Error saving poster image to provider {self.provider}: {e}, {e.args}', )
                    import traceback
                    traceback.print_exc()
            else:
                provider_mapping[self.provider]()

    def _create_poster(self):
        if self.poster['enabled'] is False:
            print('Poster disabled')
            return None

        bg_color = self.poster['bg_color'] if self.poster['bg_color'] is None else 'olive-darkolive'

        width, height = 400, 600
        start, end = (233, 0, 4), (88, 76, 76)
        angle = -160
        font_path = f'{self.config.get_root_path()}/resources/fonts/DroneRangerPro-ExtendedBold.ttf'  # path to your .ttf font file
        poster = PosterImageCreator(width, height, bg_color, angle, font_path)

        poster.create_gradient() \
            .add_background_image_from_query(search_query=self.title) \
            .add_icon_with_text(self.icon_path, self.title) \
            .add_border()
        poster_location = f'{self.config.get_root_path()}/list-builder.png'
        poster.save(poster_location, quality=95)
        return poster_location

    async def sync(self, provider: str):
        print(f'Syncing list {self.title} with provider {provider}')
        if self.media_list is None:
            print('No media list found')
            return self

        await self._save_media_list_to_provider(provider)
        return self

    async def build(self):
        # join the rules into a string
        rules_string = ','.join(self.rules)
        if self.delete_existing:
            print(f'Deleting existing list {self.title}')

        print(f'Creating {self.type} - {self.title}')

        media_list: MediaList = await self._get_media_list_from_provider()

        print('MEDIA_LIST', media_list)

        if media_list is None:
            print(f'ERROR: Unable to get media list!!!')
            return self

        # add the media to the list
        print(f'Adding {len(media_list.items)} items to {self.title}')
        print('Completed list creation')
        self.media_list = media_list
        return self
