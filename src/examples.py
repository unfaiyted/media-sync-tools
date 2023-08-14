# import os
# import sys
from create import PosterImageCreator
from src.create.list_builder import ListBuilder
from src.create.lists import Lists
from src.config import ConfigManager


# src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))

# Add the 'src' folder to the sys.path list
# sys.path.append(src_path)

def examples(config):
    mdb_list_api = config.get_client('mdb')

    emby = config.get_client('emby')

    # emby_movies = emby.get_media(external_id='imdb.tt6718170')

    # print(emby_movies)

    # poster = emby.get_item_image(emby_movies[0]['Id'])
    # print(f'poster: {poster}')

    # Get list information by list ID

    # mdb_list_api = config.get_client('mdb')

    emby = config.get_client('emby')
    tmdb = config.get_client('tmdb')

    # Fetch all trailers from Emby
    trailers = emby.get_all_trailers()
    config_path = config.config_path

    for trailer in trailers:
        print(trailer)


        id = trailer.get('Id', 'N/A')
        title = trailer.get('Name', 'N/A')
        type_ = trailer.get('Type', 'N/A')
        description = trailer.get('Description', 'N/A')

        trailer_id = trailer.get('Id', None)
        #Details: {'Name': 'Alcarràs', 'ServerId': '79657efcf1e441e0af5914999b0cbb62', 'Id': '686', 'Etag': '543b6ca4c9f21c87d81daf7a932499c0', 'DateCreated': '2023-07-20T22:20:20.0000000Z', 'ExtraType': 'Trailer', 'CanDelete': False, 'CanDownload': True, 'PresentationUniqueKey': 'd3d83e1362b142a0b6db53eb9b479cec', 'SupportsSync': True, 'SortName': 'Alcarras', 'ForcedSortName': 'Alcarras', 'PremiereDate': '2022-04-29T04:00:00.0000000Z', 'ExternalUrls': [{'Name': 'IMDb', 'Url': 'https://www.imdb.com/title/tt11930126'}, {'Name': 'TheMovieDb', 'Url': 'https://www.themoviedb.org/movie/804251'}, {'Name': 'Trakt', 'Url': 'https://trakt.tv/search/tmdb/804251?id_type=movie'}], 'MediaSources': [{'Protocol': 'Http', 'Id': 'd3d83e1362b142a0b6db53eb9b479cec', 'Path': 'https://movietrailers.apple.com/movies/independent/alcarras/alcarras-trailer-1_h480p.mov', 'Type': 'Default', 'Size': 0, 'Name': 'Alcarràs', 'IsRemote': True, 'SupportsTranscoding': True, 'SupportsDirectStream': True, 'SupportsDirectPlay': True, 'IsInfiniteStream': False, 'RequiresOpening': False, 'RequiresClosing': False, 'RequiresLooping': False, 'SupportsProbing': False, 'MediaStreams': [], 'Formats': [], 'RequiredHttpHeaders': {}, 'ReadAtNativeFramerate': False}], 'Path': 'https://movietrailers.apple.com/movies/independent/alcarras/alcarras-trailer-1_h480p.mov', 'Taglines': [], 'Genres': [], 'Size': 0, 'PlayAccess': 'Full', 'ProductionYear': 2022, 'RemoteTrailers': [], 'ProviderIds': {'Tmdb': '804251', 'Tvdb': '332346', 'IMDB': 'tt11930126'}, 'IsFolder': False, 'ParentId': '5', 'Type': 'Trailer', 'People': [], 'Studios': [], 'GenreItems': [], 'TagItems': [], 'UserData': {'PlaybackPositionTicks': 0, 'PlayCount': 0, 'IsFavorite': False, 'Played': False}, 'DisplayPreferencesId': '98407be06d631d265a0f6048c91e7414', 'MediaStreams': [], 'ImageTags': {}, 'BackdropImageTags': [], 'Chapters': [], 'MediaType': 'Video', 'LockedFields': [], 'LockData': False}

        if trailer_id:
            details = emby.get_item_metadata(trailer_id)
            print(f'Details: {details}')

            # Get poster
            try:
                image = emby.get_item_image(trailer_id)
                print(f'Got image for {title} {image}')
            except:
                print(f'Error getting image for {title}')

                image = tmdb.get_movie_poster(details['ProviderIds']['Tmdb'])

            if image is None:
                print(f'No image found for {title}')
                continue

            root_path = config.get_root_path()
            font_path = f'{root_path}/resources/fonts/DroneRangerPro-ExtendedBold.ttf'

            # Add overlay to poster
            poster = PosterImageCreator(poster=image, font_path=font_path)

            poster.save_original(f'{config_path}/resources/original-posters/{id}.png', use_original=True)

            poster.resize(400, 600)
            poster.add_overlay_with_text('TRAILER', 'bottom-left', (100, 100, 100), (255, 255, 255), 100, 5)

            poster.save(f'{config_path}/resources/posters/{id}.png')

            emby.upload_image(trailer_id, f'{config_path}/resources/posters/{id}.png')

        print(f"Title: {title}, Type: {type_}, Description: {description}")


#     # movie_info = mdb_list_api.get_movie_info_by_imdb_id("tt0073195")
#     print('movie info =========================')
#     #print(movie_info)
#
#     # Search for a movie or show
#     #search_results = mdb_list_api.search_movie_or_show("jaws")
#     #print(search_results)
#
#     # Get user limits
#     # user_limits = mdb_list_api.get_user_limits()
#     print('user limits =========================')
#     # print(user_limits)
#
#     # Get user lists
#     # user_lists = mdb_list_api.get_user_lists()
#     print('list info =========================')
#     # print(user_lists)
#
#     # Get list information by list ID
#     #list_id = 14  # Replace with an actual list ID
#     #list_info = mdb_list_api.get_list_information(list_id)[0]
#     #print('list info =========================')
#     #print(list_info)
#
#    #  print(list_info['name'], list_info['id'], list_info['mediatype'], list_info['description'], list_info['items'])
#
#
#     # Get list items by list ID
#     #list_items = mdb_list_api.get_list_items(list_id)
#     #print('list items =========================')
#     #print(list_items)
#
#     #collection = emby.create_collection(list_info['name'], 'Movies', sort_name='!!!!____' + list_info['name'])
#     # Get list items by list ID and media type
#
#
#
#
#     # Get top lists

#     # Search public lists by title
#     #searched_lists = mdb_list_api.search_lists("Top Watched Movies of The Week")
#     print('Searched Lists ======================')
#     #print(searched_lists)
#
#     #emby.create_collection(searched_lists[0][''])
#
#
#     # Get bulk ratings for a list of media IDs
#     # media_type = "movie"
#     # return_rating = "tmdb"
#     # ids = [923, 990, 545611]
#     # provider = "tmdb"
#     # bulk_ratings = mdb_list_api.get_bulk_ratings(media_type, return_rating, ids, provider)
#     # print(bulk_ratings)

# lists= Lists(create_previously_watchedlistonfig)

# lists.create_previously_watchedlist()

# PLEX
# plex = config.get_client('plex')
# trakt = config.get_client('trakt')


# Example 1: List all unwatched movies.
# movies = plex.library.section('Movies')
# for video in movies.search(unwatched=True):
# print(video.title)


# Example 2: Mark all Game of Thrones episodes as played.
# plex.library.section('TV Shows').get('Game of Thrones').markPlayed()

# cars = movies.get('Cars')

# for session in plex.sessions():
#    print(session)

# Example 3: List all clients connected to the Server.
# for client in plex.clients():
#    print(client.title)
#    print(cars)
# client.playMedia(cars)


# client = plex.client("TV 2020")
# client.playMedia(cars)

# Example 4: Play the movie Cars on another client.
# Note: Client must be on same network as server.
# cars = movies.get('Cars')
# print("Movies")
# print(cars)
# client = plex.client("faiyts-linux-pc")
# client.playMedia(cars)

# Example 5: List all content with the word 'Game' in the title.
# for video in plex.search('Game'):
#     print(f'{video.title} ({video.TYPE})')

# Example 6: List all movies directed by the same person as Elephants Dream.
# fightClub = movies.get('Fight Club')
# director = fightClub.directors[0]
# for movie in movies.search(None, director=director):
#    print(movie.title)

# Example 7: List files for the latest episode of The 100.
# last_episode = plex.library.section('TV Shows').get('The 100').episodes()[-1]
# for part in last_episode.iterParts():
#    print(part.file)

# Example 8: Get audio/video/all playlists
# for playlist in plex.playlists():
#    print(playlist.title)

# Example 9: Rate the 100 four stars.
# plex.library.section('TV Shows').get('The 100').rate(9.5)


# def sync_collections(config):
#
#     # get the collections from the config
#     collections = config.collections
#
#     #   loop over the collections
#     for name, details in collections['lists'].items():
#         # print the collection info
#         print(f'Processing collection {name}')
#
#
#         list = ListBuilder(config, list=details)
#
#         list.build()
#

# # example call
config = ConfigManager()
examples(config)
