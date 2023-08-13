from src.create.list_builder import ListBuilder

def sync_trakt_user_lists(config, username):

    trakt_api = config.get_client('trakt')

    user_lists = trakt_api.get_user_lists(username)
    print('Trakt User Lists ======================')
    print(user_lists)

    for user_list in user_lists:
        print(user_list['name'], user_list['ids']['slug'], user_list['description'], user_list['item_count'])

        details = {
            'name': user_list['name'],
            'description': user_list.get('description', ''),  # assuming the description might be optional
            'provider': 'trakt',
            'filters': [{
                'type': 'list_slug',
                'value': user_list['ids']['slug']
            }, {
                'type': 'username',
                'value': username
            }],
            'include': ['Movies'],  # assuming lists are for movies only, adjust if necessary
            'options': {
                'add_prev_watched': False,
                'add_missing_to_library': False,
                'limit': 100,  # adjust as necessary
                'sort': 'rank',  # adjust as necessary
                'poster': {
                    'enabled': True,
                    'bg_image_query': user_list['name']
                }
            }
        }

        # Here, I'm assuming you want to process movie lists only. Adjust this if lists can be for other media types too.
        list_builder = ListBuilder(config, list=details)
        list_builder.build()
