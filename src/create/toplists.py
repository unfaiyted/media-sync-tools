from src.create.list_builder import ListBuilder


async def sync_top_lists(config):

    mdb_list_api = config.get_client('mdb')


    top_lists = mdb_list_api.get_top_lists()
    print('Top Lists ======================')
    # print(top_lists)

    for top_list in top_lists[:100]:
        print(top_list['name'], top_list['id'], top_list['description'], top_list['items'])
        details = {
            'name': top_list['name'],
            'description': top_list['description'],
            'provider': 'mdb',
            'filters': [{
                'type': 'id',
                'value': top_list['id']
            }],
            'include': ['Movies'],
            'options': {
                'add_prev_watched': False,
                'add_missing_to_library': False,
                'limit': 100,
                'sort': 'rank',
                'poster': {
                    'enabled': True,
                    'bg_image_query': top_list['name']
                }
            }
        }

        if top_list['mediatype'] == 'movie':
            list = ListBuilder(config, list=details)
            await list.build()
        # elif top_list['mediatype'] == 'tv':


