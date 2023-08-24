from typing import List

from src.db.queries import library_queries
from src.create import ListBuilder
from src.models import MediaListType, Library, LibraryType
from src.config import ConfigManager
from src.models.libraries import LibraryClient

async def sync_all_lists_from_provider(payload):
    # Your syncing logic...
    print("Lists synced from provider!")

    payload = {
        'configId': 'APP-DEFAULT-CONFIG',
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


        print('embyLibrary',embyLibrary)
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


            print('details',details)
        # Here, I'm assuming you want to process movie lists only. Adjust this if lists can be for other media types too.
            print('About to build list')
            list_builder = ListBuilder(config, list=details, list_type=MediaListType.LIBRARY)
            await list_builder.build()
            print('List built')
        print("All libraries and their items synced!")

# More task-specific functions can be added here...

async def execute_task(task_type, payload):
    task_map = {
        "sync_provider": sync_all_lists_from_provider,
        # "another_task_type": another_function,
        # ... add more tasks as needed
    }

    await task_map[task_type](payload)
