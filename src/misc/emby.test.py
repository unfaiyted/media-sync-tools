from utils.emby import Emby

# def filter_array_by_key_value(array, key, value):
#     filtered_array = [item for item in array if item.get(key) == value]
#     return filtered_array


# Replace these with your actual values

from config import ConfigManager

config = ConfigManager()

plex = config.get_client('plex')
emby = config.get_client('emby')

sessions = emby.get_sessions()
# print('Sessions: ', sessions)


for session in sessions:
    # print(session['Id'], session['Client'], session['DeviceName'])
    # emby.stop_session(session['Id'])


#
# # Get all the collections
# collections = emby.get_collections()
# print('Collections: ', collections)
#
#
# test_collection_name = 'Test Collection'
#
# # Get collection if exists
# collection = filter_array_by_key_value(collections, 'Name', test_collection_name)[0]
# print('Filtered collection: ', collection)
#
# if collection:
#     print('Deleting collection: ', collection)
#     emby.delete_collection(collection['Id'])
#
# # Create a new collection
# new_collection = emby.create_collection(test_collection_name)
#
# # Get the collection
# collection = emby.get_collection(new_collection['Id'])
#
# # Print the collection
# print('Collection: ', collection)
#
# # Get the collection poster
# # poster_response = emby.getCollectionPoster(new_collection['Id'])
# # with open('poster.jpg', 'wb') as f:
# #     f.write(poster_response.content)
# #
# # # Update the collection poster
# # with open('output.png', 'rb') as f:
# #     emby.updateCollectionPoster(new_collection['Id'], f)
#
#
#
# Search a Series
# showName = "The Office (US)"
# results = emby.search(showName, "Series")
# print('Results: ', results)
#
#
# series_id = results[0]['Id']
# seasons = emby.get_seasons(series_id)
#
# print('Seasons: ', seasons)

# Get all episodes in a season


# for season in seasons:
#     episodes = emby.get_episodes(series_id, season['Id'])
#     print('Episodes: ', episodes)

# episodes = emby.get_episodes(seasons[0]['Id'])
# print('Episodes: ', episodes)


# get collections
collections = emby.get_collections()

for collection in collections:
    print(collection['Name'])

    items =  emby.get_items_in_collection(collection['Id'])

    for item in items:
        print(item['Name'])
        print(item)

        if(item['Type'] == 'Series'):
            series_id = item['Id']
            seasons = emby.get_seasons(series_id)

            print('Seasons: ', seasons)

            for season in seasons:
                episodes = emby.get_episodes(series_id, season['Id'])
                #print('Episodes: ', episodes)


                for episode in episodes:
                    print(episode['Name'])
                    print(episode['Type'])
                    print(episode['PremiereDate'])

plex_collections = plex.library.section('TV Shows').collections()

for collection in plex_collections:
    print(collection.title)

    for item in collection.items():
        print(item.title)
        print(item.type)
        print(item.year)





# # Adding Items to a Collection
# emby.add_search_results_to_collection(new_collection['Id'], results)
#
#
# # Get series from collection
# collection_items = emby.get_items_in_collection(new_collection['Id'])
# print('Collection Items: ', collection_items)
#
#
#
# # Delete Series from a Collection
# remove_show = "Forensic Files"
# results = emby.search(remove_show, "Series")
# print('Results: ', results)
#
# # Deleting items that match search results
# emby.delete_search_results_from_collection(new_collection['Id'], results)
#
#
# # Create a new collection
# new_collection = emby.create_collection("Deleted Collection")
#
# # Get the collection
# collection = emby.get_collection(new_collection['Id'])
# print('Deleted Collection: ', collection)
#
# # Delete the collection
# emby.delete_collection(new_collection['Id'])
#
#
# # emby.remove_item_from_collection(new_collection['Id'], item['Id'])
#
#
# # Add an item to the collection
# # emby.add_item_to_collection(new_collection['Id'], 'item_id')
#
# # Remove an item from the collection
# #
# emby.send_message('1395ab86775d563ca529104910dd146c', 'TESTING')
