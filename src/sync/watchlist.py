from src.utils.posters import PosterImageCreator
import logging
import os

logging.basicConfig(filename='/config/logs/watchlist.log', level=logging.INFO)
def sync_watchlist(config):
    emby = config.get_client('emby')

    root_dir = config.get_root_path()
    print(root_dir)

    account = config.get_account('myplex')

    plex_watchlist = account.watchlist()

    watchlist_library_name = 'Watchlist'  # Replace with your watchlist library's name if different

    # Create a new collection in Emby for the watchlist
    # emby.delete_collection_by_name('Watchlist') # Delete any existing watchlist collection
    emby_watchlist = emby.create_collection('Watchlist', 'Mixed')  # 'Mixed' type to allow both movies and series

    print(emby_watchlist)

    # Adjust the SortName attribute to move the collection to the top
    emby_watchlist_metadata = emby.get_item_metadata(emby_watchlist['Id'])

    emby_watchlist_metadata['ForcedSortName'] = '!000_Watchlist'
    emby_watchlist_metadata['SortName'] = '!000_Watchlist'
    emby_watchlist_metadata['LockedFields'] = ['SortName']

    emby.update_item_metadata(emby_watchlist_metadata)

    # Create poster
    width, height = 400, 600
    start, end = (233, 0, 4), (88, 76, 76)
    angle = -160
    font_path = f'{root_dir}/resources/OpenSans-SemiBold.ttf'  # path to your .ttf font file

    gradient_creator = PosterImageCreator(width, height, start, end, angle, font_path)
    img = gradient_creator.create_gradient().add_icon_with_text(f'{root_dir}/resources/to-do-list.png', 'Watchlist')

    img.save('./watchlist.png')

    emby.upload_image(emby_watchlist['Id'], 'watchlist.png')

    for media in plex_watchlist:
        print(f'Processing media: {media.title}')
        logging.info(f'Processing media: {media.title}')

        print(media.type, media, media.year, media.title)

        emby_type = 'Series' if (media.type == 'episode' or media.type == 'show') else 'Movie'      # Emby uses 'Series' instead of 'Show'

        # Try to find the same media item in Em
        emby_media_items = emby.search(media.title, emby_type)

        #TODO: If the media is a series I would like to add the series Id and not the episodes
        for emby_media in emby_media_items:
            try:
                if emby_media['ProductionYear'] == media.year:
                    # If we find a match, add it to the Emby watchlist
                    print(f'Adding {media.title} to Emby Watchlist {emby_media["Type"]}')
                    if emby_media['Type'] == 'Episode':
                        print(emby_media)
                        emby.add_item_to_collection(emby_watchlist['Id'], emby_media['SeriesId'])
                    else:
                        emby.add_item_to_collection(emby_watchlist['Id'], emby_media['Id'])
                    continue
                else:
                    print(f'No match found in Emby for {media.title}')
                    logging.warning(f'No match found in Emby for {media.title}')

            except KeyError:
                print(f'KEY ERROR: No match found in Emby for {media.title}')

