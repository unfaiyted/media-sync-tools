from src.create.posters import PosterImageCreator
from src.clients.plex import PlexManager
import logging
import os


# Delete all collections, reset
# TODO: Check config to see if we should delete collections
print('Deleting all collections. May take some time.')
# emby.delete_all_collections()
print('All collections deleted.')

def sync_collection(config):
    root_path = config.get_root_path()
    config_path = config.get_config_path()

    logging.basicConfig(filename=f'{config_path}/logs/collections.log', level=logging.INFO)

    plex = config.get_client('plex')
    emby = config.get_client('emby')

    libraries = config.get_libraries()

    for library in libraries:
        library = libraries[library]

        logging.info(f'Processing library {library["plex_name"]}')
        print(f'Processing library {library["plex_name"]}')

        plex_library = plex.library.section(library['plex_name'])

        for plex_collection in plex_library.collections():
            print('--------------------------------------------------------------------------')
            print(f'Collection: {plex_collection.title}')
            print(f'Type: {library["type"]}')
            print(plex_collection)
            poster_url = f'{os.getenv("PLEX_SERVER_URL")}{plex_collection.thumb}?X-Plex-Token={os.getenv("PLEX_ACCESS_TOKEN")}'
            print(f'Poster: {poster_url}')
            print('--------------------------------------------------------------------------')

            # Create movie collections. If a collection with that name already exists, we should suffix our collection
            # with the library name to avoid duplicates
            is_existing_collection = emby.does_collection_exist(plex_collection.title)

            poster_path = f'{config_path}/resources/collections/{plex_collection.title}.jpg'

            poster_response = PlexManager.save_plex_poster(poster_url, poster_path)

            emby_collection = None

            if is_existing_collection:
                emby_collection = emby.create_collection(f'{plex_collection.title} ({library["type"]})', library['type'])
            else:
                emby_collection = emby.create_collection(plex_collection.title, library['type'])

            # Upload plex poster
            try:
                emby.upload_image(emby_collection['Id'], poster_path)
            except:
                print('Error uploading poster')
                # Create a poster for it
                emby.create_poster(poster_path, plex_collection.title)
                emby.upload_image(emby_collection['Id'], poster_path)

            item_metadata = emby.get_item_metadata(emby_collection['Id'])

            item_metadata['ForcedSortName'] = plex_collection.titleSort
            item_metadata['Overview'] = plex_collection.summary
            item_metadata['SortName'] = plex_collection.titleSort
            item_metadata['LockedFields'] = ['SortName']

            print('item_metadata', item_metadata)

            emby.update_item_metadata(item_metadata)

            # Get and print all shows in the collection
            print(library['type'])

            media_type = library['type']

            for media in plex_collection.children:
                print(media_type, media)

                try:
                    # Match show to emby show
                    emby_movie = emby.search(media.title, library['type'])[0]
                    print('emby_movie', emby_movie)
                    emby_item_id = emby_movie['Id']

                    movie_metadata = emby.get_item_metadata(emby_item_id)

                    if movie_metadata['ProductionYear'] == media.year:
                        print('Year matches')

                        poster_url = f'{os.getenv("PLEX_SERVER_URL")}{media.thumb}?X-Plex-Token={os.getenv("PLEX_ACCESS_TOKEN")}'

                        # TODO: add validation for movie poster save?
                        poster_path = f'{root_path}/resources/{library["type"]}/{media.ratingKey}.jpg'
                        movie_poster = save_plex_poster(poster_url, poster_path)

                        # Upload plex poster

                        if os.path.exists(poster_path):
                            print('Poster exists')
                            emby.upload_image(emby_movie['Id'], poster_path)
                        else:
                            print('Poster does not exist. Lets make one I guess')
                            create_emby_poster(poster_path, media.title, root_path)
                            emby.upload_image(emby_movie['Id'], poster_path)

                        # TODO: if poster is not found in plex, create a poster based on the name of the collection
                        # poster should have a clean gradient background with large words of the collection name
                        # that represent a movie or tv show collection

                        emby.add_item_to_collection(emby_collection['Id'], emby_item_id)
                        print(f'Plex - ID: {media.ratingKey} Title: {media.title}')
                except:
                    print(f'********** {library["type"]} Not found in Emby', media.title, media.year, " *********")
