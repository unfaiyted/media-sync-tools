from src.create.providers.tmdb import TMDBProvider
from src.create.providers.trakt import TraktProvider
from src.create.posters import PosterImageCreator
from src.create.providers.ai import AiProvider
from src.create.providers.mdb import MdbProvider
from src.create.providers.trakt import TraktProvider


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

    def __init__(self, config, list_type="Collection", list=None):
        self.config = config
        self._ai_list = []
        self.rules = []
        self.filters = []
        self.title = None
        self.type = list_type
        self.emby = config.get_client('emby')
        self.retry_count = 3
        self.description = f'Automatically generated {list_type} list'
        self.sort_title = self.title
        self.provider = None
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

    def _get_media_list_from_provider(self):

        if self.provider == 'self':
            print(f'Using media list')

        if self.provider == 'ai':
            print(f'Using AI list')
            self.media_list = AiProvider(self.media_types, self.description, self._process_filters('ai'),
                                         self.limit).get_list()

        if self.provider == 'mdb':
            print(f'Using MDB list')
            self.media_list = MdbProvider(self.config, self.filters).get_list()

        if self.provider == 'trakt':
            print('Using Trakt list')
            self.media_list = TraktProvider(self.config, self.filters).get_list()

        if self.provider == 'tmdb':
            print('Using TMDB list')
            self.media_list = TMDBProvider(self.config, self.filters).get_list()

        return self.media_list

    def _create_poster(self):
        if self.poster['enabled'] is False:
            print('Poster disabled')
            return None


        bg_color =  self.poster['bg_color'] if self.poster['bg_color'] is None else 'olive-darkolive'

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

    def build(self):
        # join the rules into a string
        rules_string = ','.join(self.rules)
        if self.delete_existing:
            print(f'Deleting existing list {self.title}')
            # self.emby.delete_list_by_name(self.title)

        new_list = None
        # create the list
        print(f'Creating {self.type} - {self.title}')
        if self.type == 'Collection':
            self.print_list()
            self
            new_list = self.emby.create_collection(self.title, self._get_media_type_for_emby(), self.sort_title)
        elif self.type == 'Playlist':
            self.print_list()
            new_list = self.emby.create_playlist(self.title, self._get_media_type_for_emby())

        if new_list is not None:
            self.new_list_id = new_list['Id']

        # if the list already exists, delete it
        poster_location = self._create_poster()

        if poster_location is not None:
            self.emby.upload_image(self.new_list_id, poster_location)

        if self.new_list_id is None:
            print(f'Unable to create list {self.title}')
            return

        media_list = self._get_media_list_from_provider()

        if media_list is None:
            print(f'Unable to get media list')
            return

        # add the media to the list
        print(f'Adding {len(media_list)} items to {self.title}')
        for media in media_list:
            self.emby.add_item_to_collection(self.new_list_id, media['Id'])
            print(f'Added {media["Name"]} to {self.title}')


        print('Completed list creation')
        return media_list
