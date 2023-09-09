import re


def identify_url_type(url):
    if re.search(r'trakt\.tv', url):
        return 'trakt'
    elif re.search(r'imdb\.com', url):
        return 'imdb'
    elif re.search(r'thetvdb\.com', url):
        return 'tvdb'
    elif re.search(r'tmdb\.com', url):
        return 'tmdb'
    elif re.search(r'mdblist\.com', url):
        return 'mdb'
    else:
        return None


def get_list_from_trakt_url(url):
    match = re.search(r'lists\/([^\/?]+)', url)
    if match:
        return match.group(1)
    return None


def get_list_from_imdb_url(url):
    match = re.search(r'list\/([^\/?]+)', url)
    if match:
        return match.group(1)
    return None


def get_list_from_tvdb_url(url):
    match = re.search(r'lists\/([^\/?]+)', url)
    if match:
        return match.group(1)
    return None


def get_list_from_tmdb_url(url):
    match = re.search(r'list\/([^\/?]+)', url)
    if match:
        return match.group(1)
    return None

def get_list_from_mdb_url(url):
    match = re.search(r'lists\/([^\/]+)\/([^\/?]+)', url)
    if match:
        return {"user_id": match.group(1), "list_slug": match.group(2)}
    return None




def get_list_details_from_url(url):
    type = identify_url_type(url)
    if type == 'trakt':
        return get_list_from_trakt_url(url)
    elif type == 'imdb':
        return get_list_from_imdb_url(url)
    elif type == 'tvdb':
        return get_list_from_tvdb_url(url)
    elif type == 'tmdb':
        return get_list_from_tvdb_url(url)
    elif type == 'mdb':
        return get_list_from_mdb_url(url)
    else:
        return None

# Test examples
# trakt_url = "https://trakt.tv/users/lish408/lists/rotten-tomatoes-the-best-tv-of-2023?sort=rank,asc"
# imdb_url = "https://www.imdb.com/list/ls046877132/?ref_=otl_2"
# tvdb_url = "https://thetvdb.com/lists/star-wars"
# mdb_url = "https://mdblist.com/lists/linaspurinis/top-watched-movies-of-the-week"
#
# print("Trakt List Slug:", get_list_from_url(trakt_url))
# print("IMDB List ID:", get_list_from_url(imdb_url))
# print("TVDB List Slug:", get_list_from_url(tvdb_url))
# print("MDB List Info:", get_list_from_url(mdb_url))
