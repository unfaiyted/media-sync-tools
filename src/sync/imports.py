
import logging
import uuid
from datetime import datetime

from src.config import ConfigManager
from src.create import ListBuilder
from src.models import MediaList, MediaListType, TraktFilters
from src.models.filters import TvdbFilters, TmdbFilters, FilterType
from src.utils.url import identify_url_type, get_list_details_from_url


async def import_url(config: ConfigManager, url) -> MediaList:
    config_path = config.get_config_path()
    log = config.get_logger(__name__)
    root_dir = config.get_root_path()

    url_type = identify_url_type(url)
    filters = None

    log.info(f"Filter type set: {type(filters)}", filter=filters, type=type(filters))
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
        log.info(f'Found Trakt list', url=url)

        media_list.filters = TraktFilters(
            clientId=url_type,
            filterType=FilterType.TRAKT,
            filterTypeId=str(uuid.uuid4()),
            filtersId=str(uuid.uuid4()),
            listSlug=get_list_details_from_url(url)
        )
    elif url_type == 'imdb':
        log.info(f'Found IMDB list', url=url)
        filters = None
    elif url_type == 'tvdb':
        log.info(f'Found TVDb list', url=url)
        media_list.filters = TvdbFilters(
            clientId=url_type,
            filterType=FilterType.TVDB,
            filterTypeId=str(uuid.uuid4()),
            filtersId=str(uuid.uuid4()),
            listId=get_list_details_from_url(url)
        )
    elif url_type == 'tmdb':
        log.info(f'Found TmDb list', url=url)
        media_list.filters = TmdbFilters(
            clientId=url_type,
            filterType=FilterType.TMDB,
            filterTypeId=str(uuid.uuid4()),
            filtersId=str(uuid.uuid4()),
            listId=get_list_details_from_url(url)
        )
    else:
        log.error(f'Unknown URL type', url=url)
        return

    if media_list.filters.listId:
        log.info(f'Found source list id: {media_list.filters.listId}')
        media_list.sourceListId = media_list.filters.listId

    log.info(f'Created media list', media_list=media_list.dict())

    list = ListBuilder(config, media_list=media_list)
    media_list = (await list.build()).get_media_list()
    return media_list

