import random
import logging
from src.create.posters import PosterImageCreator

def create_emby_playlist(config, name, shows, if_exists_delete=True):
    root_path = config.get_root_path()
    config_path = config.get_config_path()

    logging.basicConfig(filename=f'{config_path}/logs/playlist.log', level=logging.INFO)

    print('Creating Emby playlist')

    emby = config.get_client('emby')

    all_media = []

    playlists = emby.get_playlists()
    print(playlists)

    if if_exists_delete:
        try:
            emby.delete_playlist(playlists[0]['Id'])
        except:
            print('No playlist to delete')

    playlist = emby.create_playlist(name, 'Series')
    # Fetch all episodes from each show
    for show_name in shows:
        print(f'Fetching episodes for {show_name}')
        show = emby.search(show_name, 'Series')[0]
        seasons = emby.get_seasons(show['Id'])

        # print(seasons)

        for season in seasons:
            episodes = emby.get_episodes(show['Id'], season['Id'])
            print(f'Fetched {len(episodes)} episodes for {show_name}')
            for episode in episodes:
                # print(episode)
                all_media.append(episode['Id'])

    print(f'Total number of media items: {len(all_media)}')

    # Shuffle all the media items
    random.shuffle(all_media)
    # Create a new playlist with the first 500 media items, or all items if there are less than 500
    playlist_items = all_media[:3000] if len(all_media) > 3000 else all_media
    # plex.createPlaylist('Sleeping Shows', 'TV Shows', playlist_items)
    def create_emby_poster(path, text, icon_path=f'{root_path}/resources/icons/tv.png', bg_image_query=None):
        width, height = 400, 600
        start, end = (233, 0, 4), (88, 76, 76)
        angle = -160

        font_path = f'{root_path}/resources/fonts/DroneRangerPro-ExtendedBold.ttf'  # path to your .ttf font file
        poster = PosterImageCreator(400, 600, "red-darkred", angle, font_path)
        img = poster.create_gradient()\
            .add_background_image_from_query(search_query=bg_image_query).add_icon_with_text(icon_path, text)

        img.save(path, quality=95)
        return img

    print(all_media)
    image = create_emby_poster(f'{config_path}/resources/sleeping.png', 'Sleeping Shows', bg_image_query='bedtime')
    emby.upload_image(playlist['Id'], f'{config_path}/resources/sleeping.png')

    for item in playlist_items:
        emby.add_item_to_playlist(playlist['Id'], item)


    # emby.upload_image(emby_watchlist['Id'], 'watchlist.png')



# Test
