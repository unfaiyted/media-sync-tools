
from create import PosterImageCreator

def trailer_poster(config):

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

# config = ConfigManager()
# examples(config)
