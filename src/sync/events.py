import logging

from src.clients.plex import PlexManager


def sync_event(event, config):
    config_path = config.get_config_path()
    root_dir = config.get_root_path()

    logging.basicConfig(filename=f'{config_path}/logs/events.log', level=logging.INFO)

    plex = config.get_client('plex')
    emby = config.get_client('emby')

    print(f'Syncing event: {event.get("Event")}')

    title = event.get("Title")
    description = event.get("Description")
    date = event.get("Date")
    event_name = event.get("Event")
    # server = event.get("Server")
    # print(title, description, date, event_name)

    if event_name == "item.rate": # liked or not boolean value
        print("Item rated", event)
        # Sync item rating in plex
        # Train AI Recommendations based on rating
        # Create a collection based on recently rated items
        item_id = event['Item']['Id']

        data = emby.get_item_metadata(item_id)

        print('item-metadata', data['UserData'])
        isFavorite = data['UserData']['IsFavorite']


        tv = plex.library.section('TV Shows')

        series_name = data['SeriesName']
        episode_index = data['IndexNumber']

        # print(series_name, episode_index)

        imdb_id = data['ProviderIds'].get('Imdb') or None
        tvdb_id = data['ProviderIds'].get('Tvdb') or None
        tvrage_id = data['ProviderIds'].get('TvRage') or None
        tmdb_id = data['ProviderIds'].get('Tmdb') or None


        season_number = data['ParentIndexNumber']
        episode_number = data['IndexNumber']
        year = data['ProductionYear']
        # results = plex.search(tvdb_id=tvdb_id, year=year, limit=1)

        # tv_show = tv.get(tvdb_id=tvdb_id)
        episode_title = data['Name']

        # print('episode_title', episode_title, series_name)
        # results = plex.library.section('TV Shows') #.getGuid(f'tvdb://{tvdb_id}')

        plex_manager = PlexManager(config)

        results= plex_manager.get_by_guid(f'tvdb://{tvdb_id}')

        episode = None
        print('result=>', results)
        for result in results:
            print(result, result.guid)
            if result.guid.startswith(f'tvdb://{tvdb_id}'):
                episode = result
                break


        # episode = tv_show.episode(season_number, episode_number)
        # <Guid id="imdb://tt2362659"/>
        # <Guid id="tmdb://170308"/>
        # <Guid id="tvdb://4292647"/>
        # plex_results = plex.library.search(title=title, year=year, limit=1)

        if episode is not None:
            print(episode.title, episode.year, episode.isWatched, episode.isFavorite)
            if isFavorite:
                episode.markFavorite()
            else:
                episode.markUnfavorite()

            # plex_item.rate(event['Item']['CommunityRating'])



    if event_name == "item.played":
        print("Item played")
        # Sync item as played in plex
        # Train AI Recommendations based on watched items
        # Create a collection based on recently watched items

    if event_name == "item.markplayed":
        print("Item watched status changed")
        # Resync watchlist collection
        from create.lists import Lists
        list_maker = Lists(config)
        list_maker.create_previously_watchedlist()
    if event_name == "playback.stop":
        print("Playback stopped")
        # Check if the item was watched for more than 75% of the duration
        # If so, add it to the previously watched collection
        # Resync watchlist collection
        list_maker = Lists(config)
        list_maker.create_previously_watchedlist()

        # Smart collections based on recently watched
        # Smart collections based on recently added

