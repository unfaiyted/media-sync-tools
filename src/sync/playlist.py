import random
import logging
from utils.posters import PosterImageCreator
from config import ConfigManager


logging.basicConfig(filename='/config/plex-to-emby-sync-errors.log', level=logging.INFO)
config = ConfigManager()

plex = config.get_client('plex')
emby = config.get_client('emby')


shows = [
    'How I Met Your Mother',
    # 'Ancient Aliens',
    'Bob\'s Burgers',
    'Forensic Files',
    'Downton Abbey',
    'Parks and Recreation',
    '30 Rock',
    'Daria',
    'The Good Place',
    'The Office (US)',
    'Friends',
    'Rick and Morty'
]

all_media = []

playlists = emby.get_playlists()
print(playlists)

emby.delete_playlist(playlists[0]['Id'])
playlist = emby.create_playlist('Sleeping Shows','Series')
# Fetch all episodes from each show
for show_name in shows:
    print(f'Fetching episodes for {show_name}')
    show = emby.search(show_name,'Series')[0]
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
playlist_items = all_media[:2000] if len(all_media) > 2000 else all_media
# plex.createPlaylist('Sleeping Shows', 'TV Shows', playlist_items)

print(all_media)

for item in playlist_items:
    emby.add_item_to_playlist(playlist['Id'], item )

def create_emby_poster(path, text, icon_path = './resources/tv.png'):
    width, height = 400, 600
    start, end = (233, 0, 4), (88, 76, 76)
    angle = -160
    font_path = './resources/OpenSans-SemiBold.ttf'  # path to your .ttf font file

    gradient_creator = PosterImageCreator(width, height, start, end, angle, font_path)
    img = gradient_creator.create_gradient().add_icon_with_text(icon_path, text)

    img.save(path)
    return img
# emby.upload_image(emby_watchlist['Id'], 'watchlist.png')

image = create_emby_poster('./resources/sleeping.png', 'Sleeping Shows')
emby.upload_image(playlist['Id'], './resources/sleeping.png')
