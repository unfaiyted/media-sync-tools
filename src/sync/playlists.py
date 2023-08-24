import logging


def sync_playlists(config):
    config_path = config.get_config_path()
    root_dir = config.get_root_path()

    logging.basicConfig(filename=f'{config_path}/logs/playlists.log', level=logging.INFO)

    plex = config.get_client('plex')


    playlists = plex.playlists()

    print(f'Found {len(playlists)} playlists')

    for playlist in playlists:
        print(f'Syncing playlist: {playlist.title}')
        logging.info(f'Syncing playlist: {playlist.title}')

        # Create the playlist in Emby
        #emby_playlist = emby.create_playlist(playlist.title)

        # Adjust the SortName attribute to move the playlist to the top
        #emby_playlist_metadata = emby.get_item_metadata(emby_playlist['Id'])
        #TODO: get the sort name from the plex playlist and use that sort name in emby

        #emby.update_item_metadata(emby_playlist_metadata)

        for item in playlist.items():
            print(f'Processing item: {item.title}')
            # try:
                # Find the corresponding item in Emby
            #   emby_items = emby.search(item.title)
#
            #    for emby_item in emby_items:
            #        # Add the item to the Emby playlist
            #        emby.add_item_to_playlist(emby_playlist['Id'], emby_item['Id'])
            #        print(f'Added item: {item.title}')
            #        logging.info(f'Added item: {item.title}')
            #except Exception as e:
            #    print(f'Error syncing item: {item.title}')
            #    logging.error(f'Error syncing item: {item.title}: {str(e)}')


