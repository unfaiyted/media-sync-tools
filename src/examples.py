# import os
# import sys
from src.create.list_builder import ListBuilder
from src.create.lists import Lists
from src.config import ConfigManager
# src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))

# Add the 'src' folder to the sys.path list
# sys.path.append(src_path)

def examples(config):

    mdb_list_api = config.get_client('mdb')

    emby = config.get_client('emby')

    emby_movies = emby.get_media(external_id='imdb.tt6718170')

    print(emby_movies)

    poster = emby.get_item_image(emby_movies[0]['Id'])

    print(f'poster: {poster}')

    # Get list information by list ID

    mdb_list_api = config.get_client('mdb')




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

    #cars = movies.get('Cars')

    # for session in plex.sessions():
    #    print(session)

    # Example 3: List all clients connected to the Server.
    #for client in plex.clients():
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
    #fightClub = movies.get('Fight Club')
    #director = fightClub.directors[0]
    #for movie in movies.search(None, director=director):
    #    print(movie.title)

    # Example 7: List files for the latest episode of The 100.
    #last_episode = plex.library.section('TV Shows').get('The 100').episodes()[-1]
    #for part in last_episode.iterParts():
    #    print(part.file)

    # Example 8: Get audio/video/all playlists
    #for playlist in plex.playlists():
    #    print(playlist.title)

    # Example 9: Rate the 100 four stars.
    #plex.library.section('TV Shows').get('The 100').rate(9.5)


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



