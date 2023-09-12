import uuid
from datetime import datetime


from src.models import MediaList, MediaListType
from src.models.filters import FilterType, MdbFilters
from src.create.list_builder import ListBuilder


async def sync_top_lists(config):
    mdb_list_api = config.get_client('mdb')
    log = config.get_logger(__name__)

    top_lists = mdb_list_api.get_top_lists()
    log.debug("Top Lists", top_lists=top_lists)

    for top_list in top_lists[:100]:
        log.debug("Top List", top_list=top_list)

        media_list = MediaList(
            mediaListId=str(uuid.uuid4()),
            name=top_list['name'],
            type=MediaListType.COLLECTION,
            description=top_list['description'],
            sortName=top_list['name'],
            createdAt=datetime.now(),
            creatorId=config.get_user().userId,
            clientId='mdb',
        )
        log.debug("Creating media list", media_list=media_list)
        media_list.filters = MdbFilters(
            filtersId=str(uuid.uuid4()),
            clientId=media_list.clientId,
            filterType=FilterType.MDB,
            listId=top_list['id']
        )
        log.debug("Adding filters to media list", media_list=media_list)

        log.debug("Creating media list", media_list=media_list)
        if top_list['mediatype'] == 'movie':
            log.info("Building movie list", media_list=media_list)
            list = ListBuilder(config, media_list=media_list)
            await list.build()
            log.info("Built movie list", media_list=media_list)
        # elif top_list['mediatype'] == 'tv':
