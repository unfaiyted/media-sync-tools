from src.clients.trakt import TraktClient
from src.create.list_builder import ListBuilder

async def sync_trakt_lists(config, fetch_function, list_type_name):
    trakt_api: TraktClient = config.get_client('trakt')
    lists = fetch_function()

    print(f'Trakt {list_type_name} Lists ======================')
    # print(lists)

    for lst in lists:
        if(lst['list']):
            print('----xxx---------', lst)
            lst = lst['list']

        print('----xxx---------', lst)

        print(lst['name'], lst['ids']['slug'], lst.get('description', ''), lst['item_count'])

        details = {
            'name': lst['name'],
            'description': lst.get('description', ''),
            'provider': 'trakt',
            'filters': [{
                'type': 'list_slug',
                'value': lst['ids']['trakt']
            }],
            'include': ['Movies'],  # assuming lists are for movies only
            'options': {
                'add_prev_watched': False,
                'add_missing_to_library': False,
                'limit': 100,
                'sort': 'rank',
                'poster': {
                    'enabled': True,
                    'bg_image_query': lst['name']
                }
            }
        }
        # Adjust for user-specific lists
        if list_type_name == "User":
            details['filters'].append({
                'type': 'username',
                'value': 'faiyt'  # Assuming function name ends with username
            })

        list_builder = ListBuilder(config, list=details)
        await list_builder.build()


async def sync_trakt_user_lists(config, username):
   await sync_trakt_lists(config, lambda: config.get_client('trakt').get_user_lists(username), "User")


async def sync_trakt_trending_lists(config):
    await sync_trakt_lists(config, lambda: config.get_client('trakt').get_trending_lists(), "Trending")


async def sync_trakt_popular_lists(config):
    await sync_trakt_lists(config, lambda: config.get_client('trakt').get_popular_lists(), "Popular")
