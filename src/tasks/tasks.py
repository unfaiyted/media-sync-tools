from typing import List

from src.config import ConfigManager
from src.models.libraries import LibraryClient

async def sync_all_lists_from_provider(payload):
    # Your syncing logic...
    print("Lists synced from provider!")


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
    libraryClients: List[LibraryClient] = [
    ]

    # check if the library with the same name exists as in the clients
    # if it does exist then we will create a new list for it if it does not
    # exist then we will update the existing list with the new data.
    # Continuing from where your code left off...

    # loop through each library in the emby client
    for library in libraries:

        # Check if this library name exists in libraryClients
        matching_library_client = next((item for item in libraryClients if item['name'] == library['name']), None)

        if not matching_library_client:
            # If it doesn't exist in libraryClients, add it
            libraryClients.append({
                'name': library['name'],
                'id': library['id'],  # Assuming the library from emby also has an 'id'
                'type': library['type']  # Again, assuming the library from emby also has a 'type'
            })

        # Now, fetch the list items from emby for this library
        list_items = emby.get_items_for_library(library['id'])

        embyCollectionTypes: List = ['movies', 'tvshows',  'playlists', 'boxsets', 'folders']

        # Now, fetch the list items from emby for this library
        if library['type'] in embyCollectionTypes:


           details = {
                'name': library['Name'],
                'id': library['Id'],  # Assuming the library from emby also has an 'id'
                'type': library['Type']  # Again, assuming the library from emby also has a 'type'

           }

    details = {
        'name': library_client.libraryName,
        'description': f'{client.label} - {library_client.libraryName}',
        'provider': client.name,
        'filters': [{
            'type': 'library',
            'value': library_client.libraryName
        }],
        'include': ['Movies'],
        'options': {
            'add_prev_watched': False,
            'add_missing_to_library': False,
            'limit': 1000,
            'sort': 'rank',
            'poster': {
                'enabled': True,
            }
        }
    }
           # create a list
           # we need some way to know if we have already synced this library and if so then we need to update it
              # if not then we need to create it.




        # Sync the items to your database
        # Here, you'll probably want to check if each item exists, and either insert new or update existing records
        for item in list_items:
            existing_item = db.find_item_by_id(item['id'])  # Hypothetical method to check if an item exists in your database

            # if not existing_item:
            #     db.insert_item(item)  # Hypothetical method to insert a new item in your database
            # else:
            #     db.update_item(item)  # Hypothetical method to update an existing item in your database

    print("All libraries and their items synced!")







# More task-specific functions can be added here...

async def execute_task(task_type, payload):
    task_map = {
        "sync_provider": sync_all_lists_from_provider,
        # "another_task_type": another_function,
        # ... add more tasks as needed
    }

    await task_map[task_type](payload)
