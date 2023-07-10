import logging

def sync_watchlist(config):
    config_path = config.get_config_path()
    root_dir = config.get_root_path()

    logging.basicConfig(filename=f'{config_path}/logs/watchlist.log', level=logging.INFO)

    emby = config.get_client('emby')

    account = config.get_account('myplex')

    plex_watchlist = account.watchlist()

    watchlist_collection_name = 'Watchlist'  # Replace with your watchlist library's name if different

    # Create a new collection in Emby for the watchlist
    # emby.delete_collection_by_name('Watchlist') # Delete any existing watchlist collection
    emby_watchlist = emby.create_collection('Watchlist', 'Mixed', '!000_Watchlist')  # 'Mixed' type to allow both movies and series

    print(emby_watchlist)

    # Create poster
    icon_path = f'{root_dir}/resources/to-do-list.png'

    emby.create_poster(f'{config_path}/watchlist.png', watchlist_collection_name, root_dir, icon_path)
    emby.upload_image(emby_watchlist['Id'], f'{config_path}/watchlist.png')

    for media in plex_watchlist:
        print(f'Processing media: {media.title}')

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

