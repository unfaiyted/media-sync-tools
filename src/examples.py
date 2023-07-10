from src.create.watchedlists import WatchedListCreator
from src.config import ConfigManager


def examples(config):

    wlCreator = WatchedListCreator(config)

    wlCreator.create_previously_watchedlist()

    # PLEX
    #plex = config.get_client('plex')
    # trakt = config.get_client('trakt')



    # Example 1: List all unwatched movies.
    #movies = plex.library.section('Movies')
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


# # example call
# config = ConfigManager()
#
# examples(config)
