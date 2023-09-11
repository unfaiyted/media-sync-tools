from datetime import datetime

from src.clients.emby import Emby
from src.db.queries import media_list_queries
from typing import Optional
from typing import List

from src.models.tasks import TaskType
from src.db.queries import library_queries
from src.create import ListBuilder
from src.models import MediaListType, Library, LibraryType, MediaList
from src.config import ConfigManager
from src.models.libraries import LibraryClient

async def sync_libraries_from_provider(payload):
    print("Lists synced from provider!")

    payload = {
        'configId': 'APP-DEFAULT-CONFIG',
        'provider': 'emby'
        # config client id
    }
    # lets start with emby.
    # starting with the main library list and then get all the the sub lists.
    # then we can get the items from each list and sync them to our database MediaLists and MediaListItems

    config = ConfigManager().get_manager()
    db = config.get_db()  # Get your database connection, similar to what's in your routes

    # get the emby client
    emby = config.get_client('emby')

    # get the main library list
    libraries = emby.get_libraries()


    # create a list for each sub list that is part of this LibraryClient array
    libraryClients: List[Library] = await library_queries.get_libraries_with_clients_by_config_id(db, payload['configId'])
    # check if the library with the same name exists as in the clients
    # if it does exist then we will create a new list for it if it does not
    # exist then we will update the existing list with the new data.
    # Continuing from where your code left off...

    embyCollectionTypes: List = ['movies', 'tvshows']
    # loop through each library in the emby client
    for embyLibrary in libraries:

        # Check if this embyLibrary name exists in libraryClients
        matching_library_client = next((item for item in libraryClients if item.name == embyLibrary['Name']), None)

        # Only create collections for movies and tvshows

        if embyLibrary.get('CollectionType', None) not in embyCollectionTypes:
            continue

        if not matching_library_client:
            # If it doesn't exist in libraryClients, add it

            if(embyLibrary['CollectionType'] == 'movies'):
                library = await library_queries.create_library(db, embyLibrary['Name'], LibraryType.MOVIES, 'EMBYCLIENTID')
            elif(embyLibrary['CollectionType'] == 'tvshows'):
                library = await library_queries.create_library(db, embyLibrary['Name'], LibraryType.SHOWS, 'EMBYCLIENTID')

            # Create new list with listBuilder
        # list_items = emby.get_items_for_library(embyLibrary['id'])


        # print('embyLibrary',embyLibrary)
        # Now, fetch the list items from emby for thisembyLibrary
        if embyLibrary['CollectionType'] in embyCollectionTypes:

            # Create new list with listBuilder
            details = {
                'name': embyLibrary['Name'],
                'description': embyLibrary['Name'] + " / " + embyLibrary['Type'],  # assuming the description might be optional
                'provider': 'emby',
                'type': MediaListType.LIBRARY,
                'filters': [{
                    'type': 'list_id',
                    'value': embyLibrary['Id']
                }],
                'include': ['Movies'],  # assuming lists are for movies only, adjust if necessary
                'options': {
                    'add_prev_watched': False,
                    'add_missing_to_library': False,
                    'limit': 5000,  # adjust as necessary
                    'sort': 'rank',  # adjust as necessary
                    'poster': {
                        'enabled': True,
                    }
                }
            }


            # print('details',details)
            # Here, I'm assuming you want to process movie lists only. Adjust this if lists can be for other media types too.
            print('About to build list')
            list_builder = ListBuilder(config, list=details, list_type=MediaListType.LIBRARY)
            await list_builder.build()
            print('List built')
        print("All libraries and their items synced!")


# More task-specific functions can be added here...


async def sync_all_collections_from_provider(payload):
    print("Syncing all collections from provider!")

    embyCollectionTypes: List = ['boxsets']

    # Your initial config and database setup
    config = ConfigManager().get_manager()
    db = config.get_db()

    # get the emby client
    emby = config.get_client('emby')
    libraries = emby.get_libraries()
    # print('libraries',libraries)

    # Retrieve collections of type "Collection" from Emby.
    # Assuming emby has a method like `get_collections_of_type`

    boxset_libraries = [lib for lib in libraries if lib.get('CollectionType') == 'boxsets']
    print(boxset_libraries)

    # Loop through the Emby collections
    for library in boxset_libraries:

        print('Looking at library')
        # print('library', library)
        # Check if the collection already exists in the database
        boxsets, boxset_count = emby.get_items_from_parent(library['Id'])
        print('Boxset found.', boxset_count)
        print('boxsets', boxsets)

        for boxset in boxsets:
            print('Looking at boxset', boxset['Name'], boxset['Id'])
            # print('boxset', boxset)

            matching_collection: Optional[MediaList] = await media_list_queries.get_media_list_by_source_id(db, boxset['Id'])

        # get the items from the boxset
            if not matching_collection:
                print('No matching collection found')
                # If the collection isn't in the database, add it.
                new_media_list = MediaList(
                    sourceListId=boxset['Id'],
                    clientId='EMBYCLIENTID',
                    creatorId="YOUR_CREATOR_ID", # Adjust this accordingly
                    name=boxset['Name'],
                    type=MediaListType.COLLECTION,
                    sortName=boxset['SortName'] if 'SortName' in boxset else boxset['Name'],
                    createdAt=datetime.now()
                    # Add more fields if necessary
                )

                await media_list_queries.create_media_list(db, new_media_list)
                print('Created new collection')
            elif boxset['Name'] != matching_collection.name:
                matching_collection.name = boxset['Name']
                matching_collection = await media_list_queries.update_media_list(db, matching_collection.mediaListId, matching_collection)

            # Loop through the items in the boxset
                    # Create new list with listBuilder
            details = {
                        'name': boxset['Name'],
                        'description': boxset['Name'] + " / " + boxset['Type'],  # assuming the description might be optional
                        'provider': 'emby',
                        'type': MediaListType.COLLECTION,
                        'filters': [{
                            'type': 'list_id',
                            'value': boxset['Id']
                        }],
                        'include': ['Movies'],  # assuming lists are for movies only, adjust if necessary
                        'options': {
                            'add_prev_watched': False,
                            'add_missing_to_library': False,
                            'limit': 5000,  # adjust as necessary
                            'sort': 'rank',  # adjust as necessary
                            'poster': {
                                'enabled': True,
                            }
                        }
                    }
            print('details',details)
                    # Here, I'm assuming you want to process movie lists only. Adjust this if lists can be for other media types too.
            print('About to build list')
            try:
                list_builder = ListBuilder(config, list=details, list_type=MediaListType.COLLECTION)
                await list_builder.build()
            except:
                print('Error building list')
        print("All collections synced!")


# To make this one function I need a method that will get all collections by client type


async def sync_media_list_to_provider(payload):
    print("Syncing media list to provider!")

    # Extract necessary payload details.
    list_id = payload.get('list_id', None)
    if not list_id:
        print("No list_id provided in payload.")
        return

    config = ConfigManager().get_manager()
    db = config.get_db()

    # Fetch the media list from your local database
    media_list = await media_list_queries.get_media_list_with_items(db, list_id)
    if not media_list:
        print(f"No media list found for id: {list_id}")
        return

    # get the emby client
    emby: Emby = config.get_client('emby')

    embyListId = media_list['sourceListId']
    # Assuming that the media_list model has a 'clientType' field
    is_from_emby = media_list.get('clientConfigId') == 'emby' # TODO: implment client selection logic and such
    # If the list doesn't originate from emby or has no source ID, assume it's a new list
    if not embyListId or not is_from_emby:
        emby_list = None
    else:
        # Fetch the list from emby using the sourceListId
        emby_list = emby.get_list(embyListId)

    # Determine media list type and perform relevant actions
    media_list_type = media_list.get('type')


    if(media_list is None):
        print('No media list found')
        return

    media_list = MediaList(**media_list)

    if media_list_type == MediaListType.COLLECTION:
        if not emby_list:
            emby.create_collection_from_list(media_list)
        else:
            emby.update_collection_from_list(media_list)
    elif media_list_type == MediaListType.PLAYLIST:
        if not emby_list:
            emby.create_playlist_from_list(media_list)
        else:
            emby.update_playlist_from_list(media_list)
    elif media_list_type == MediaListType.LIBRARY:
        print("Ignoring libraries, not syncing to provider.")
        return
    else:
        print(f"Unknown media list type: {media_list_type}")
        return

    print("Media list synced to provider!")

# async def sync_media_list_to_provider(payload):


async def execute_task(task_type, payload):
    task_map = {
        TaskType.SYNC_PROVIDER.value: sync_libraries_from_provider,
        TaskType.SYNC_COLLECTIONS.value: sync_all_collections_from_provider,
        TaskType.SYNC_MEDIA_LIST.value: sync_media_list_to_provider,
        # ... add more tasks as needed
    }

    await task_map[task_type](payload)
