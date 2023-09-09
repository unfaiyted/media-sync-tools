
import logging
import uuid
from datetime import datetime

from src.create import ListBuilder
from src.models import MediaList, MediaListType, TraktFilters
from src.models.filters import TvdbFilters, TmdbFilters, FilterType
from src.utils.url import identify_url_type, get_list_details_from_url


async def import_url(config, url) -> MediaList:
    config_path = config.get_config_path()
    root_dir = config.get_root_path()

    url_type = identify_url_type(url)
    filters = None

    print(f"Filter type set: {type(filters)}")
    media_list = MediaList(
        mediaListId=str(uuid.uuid4()),
        # sourceListId=filters.listId if filters.listId else None,
        name='',
        type=MediaListType.COLLECTION,
        description='',
        sortName='',
        clientId=url_type,
        createdAt=datetime.now(),
        creatorId=config.get_user().userId,
        filters=filters
    )

    if url_type == 'trakt':
        print(f'Found Trakt list: {url}')
        media_list.filters = TraktFilters(
            clientId=url_type,
            filterType=FilterType.TRAKT,
            filterTypeId=str(uuid.uuid4()),
            filtersId=str(uuid.uuid4()),
            listSlug=get_list_details_from_url(url)
        )
    elif url_type == 'imdb':
        print(f'Found IMDB list: {url}')
        filters = None
    elif url_type == 'tvdb':
        print(f'Found TVDb list: {url}')
        media_list.filters = TvdbFilters(
            clientId=url_type,
            filterType=FilterType.TVDB,
            filterTypeId=str(uuid.uuid4()),
            filtersId=str(uuid.uuid4()),
            listId=get_list_details_from_url(url)
        )
    elif url_type == 'tmdb':
        print(f'Found TmDb list: {url}')
        media_list.filters = TmdbFilters(
            clientId=url_type,
            filterType=FilterType.TMDB,
            filterTypeId=str(uuid.uuid4()),
            filtersId=str(uuid.uuid4()),
            listId=get_list_details_from_url(url)
        )
    else:
        print(f'Unknown URL type: {url_type}')
        return

    if media_list.filters.listId:
        print(f'Found source list id: {media_list.filters.listId}')
        media_list.sourceListId = media_list.filters.listId

    print(f'Created media list: {media_list}')

    list = ListBuilder(config, media_list=media_list)
    return await list.build()

