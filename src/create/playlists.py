import random
import logging
import uuid

from src.create.posters import MediaPosterImageCreator
from src.models import MediaPoster, MediaPosterBorderOptions, MediaPosterTextOptions, MediaPosterGradientOptions, \
    MediaImageType


def create_emby_playlist(config, name, shows, if_exists_delete=True):
    root_path = config.get_root_path()
    config_path = config.get_config_path()
    log = config.get_logger(__name__)

    log.info(f'Creating playlist {name} with {len(shows)} shows')
    emby = config.get_client('emby')

    all_media = []

    playlists = emby.get_playlists()

    if if_exists_delete:
        try:
            log.info('Attempting to delete existing playlist')
            emby.delete_playlist(playlists[0]['Id'])
        except:
            log.info('No playlist to delete')

    playlist = emby.create_playlist(name, 'Series')
    # Fetch all episodes from each show
    for show_name in shows:
        log.info(f'Fetching episodes for {show_name}')
        show = emby.search(show_name, 'Series')[0]
        seasons = emby.get_seasons(show['Id'])


        for season in seasons:
            episodes = emby.get_episodes(show['Id'], season['Id'])
            log.info(f'Fetched {len(episodes)} episodes for {show_name}')
            for episode in episodes:
                log.debug(f'Adding episode {episode["Name"]} to playlist', episode=episode)
                all_media.append(episode['Id'])

    log.info(f'Total number of media items: {len(all_media)}')

    # Shuffle all the media items
    random.shuffle(all_media)
    # Create a new playlist with the first 500 media items, or all items if there are less than 500
    playlist_items = all_media[:3000] if len(all_media) > 3000 else all_media

    # plex.createPlaylist('Sleeping Shows', 'TV Shows', playlist_items)
    def create_emby_poster(path, text, icon_path=f'{root_path}/resources/icons/tv.png', bg_image_query=None):
        start, end = (233, 0, 4), (88, 76, 76)
        angle = -160

        font_path = f'{root_path}/resources/fonts/DroneRangerPro-ExtendedBold.ttf'  # path to your .ttf font file
        # poster = PosterImageCreator(400, 600, "red-darkred", angle, font_path)
        # img = poster.create_gradient()\
        #     .add_background_image_from_query(search_query=bg_image_query).add_icon_with_text(icon_path, text)

        media_poster = MediaPoster(
            mediaPosterId=str(uuid.uuid4()),
            width=400,
            height=600,
            type=MediaImageType.POSTER,
            gradient=MediaPosterGradientOptions(
                enabled=True,
                colors=[start, end],
                angle=angle
            ),
            border=MediaPosterBorderOptions(
                enabled=True,
                width=5,
                height=5,
                color=[255, 255, 255]
            ),
            text=MediaPosterTextOptions(
                enabled=True,
                text=text,
                font=font_path,
                color=[255, 255, 255],
            )

        )
        log.debug("Creating poster", poster=media_poster)

        poster = MediaPosterImageCreator(media_poster=media_poster, get_logger=config.get_logger)
        log.debug("Saving poster", poster=poster)
        poster.save(path)
        log.debug("Save complete. Returning", poster=poster)
        return poster

    log.debug("Creating playlist", name=name, shows=shows, playlist=playlist)
    create_emby_poster(f'{config_path}/resources/sleeping.png', 'Sleeping Shows', bg_image_query='bedtime')
    log.debug("Uploading image", playlist=playlist)
    emby.upload_image(playlist['Id'], f'{config_path}/resources/sleeping.png')

    for item in playlist_items:
        log.debug("Adding item to playlist", item=item)
        emby.add_item_to_playlist(playlist['Id'], item)
