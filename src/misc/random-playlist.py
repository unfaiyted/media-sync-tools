# from plexapi.myplex import MyPlexAccount
# import random
# from utils.posters import PosterImageCreator
#
# plex = account.resource('FAIYT-SERVER').connect()
#
# shows = [
#     'How I Met Your Mother',
#     # 'Ancient Aliens',
#     'Bob\'s Burgers',
#     'Forensic Files',
#     'Downton Abbey',
#     'Parks and Recreation',
#     '30 Rock',
#     'Daria',
#     'The Good Place',
#     'The Office',
#     'Friends',
#     'Rick and Morty'
# ]
#
# all_media = []
#
# # Fetch all episodes from each show
# for show_name in shows:
#     print(f'Fetching episodes for {show_name}')
#     show = plex.library.section('TV Shows').get(show_name)
#     episodes = show.episodes()
#     print(f'Fetched {len(episodes)} episodes for {show_name}')
#     for episode in episodes:
#         all_media.extend(episode)
#
# print(f'Total number of media items: {len(all_media)}')
#
# # Shuffle all the media items
# random.shuffle(all_media)
#
# # Create a new playlist with the first 500 media items, or all items if there are less than 500
# playlist_items = all_media[:2000] if len(all_media) > 2000 else all_media
# plex.createPlaylist('Sleeping Shows', 'TV Shows', playlist_items)
#
# def create_emby_poster(path, text, icon_path = './resources/tv.png'):
#     width, height = 400, 600
#     start, end = (233, 0, 4), (88, 76, 76)
#     angle = -160
#     font_path = './resources/OpenSans-SemiBold.ttf'  # path to your .ttf font file
#
#     gradient_creator = PosterImageCreator(width, height, start, end, angle, font_path)
#     img = gradient_creator.create_gradient().add_icon_with_text(icon_path, text)
#
#     img.save(path)
#     return img
# # emby.upload_image(emby_watchlist['Id'], 'watchlist.png')
#
# image = create_emby_poster('./resources/sleeping.png', 'Sleeping Shows')
# emby.upload_image(playlist['Id'], './resources/sleeping.png')
