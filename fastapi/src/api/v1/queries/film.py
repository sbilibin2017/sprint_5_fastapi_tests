from core.config import Settings

CONFIG = Settings()

QUERY_ALL = \
    {
        "size": CONFIG.elastic.scroll_size,
        "query": {"match_all": {}}
    }


def _add_filter_genres(genres: list[str]) -> dict:
    return {
        "size": CONFIG.elastic.scroll_size,
        "query": {
            "bool": {
                "filter": {
                    "terms": {
                        "genre_name": genres
                    }
                }
            }
        }
    }


def _add_sort(sort_key: str, sort_order: str) -> dict:
    return {"sort": [{sort_key: {"order": sort_order}}]}

##########################################################################


def query_films() -> dict:
    return QUERY_ALL


def query_films_with_sort(sort: str) -> dict:
    if '-' in sort:
        sort_key = sort.split('-')[1]
        sort_order = 'desc'
    else:
        sort_key = sort
        sort_order = 'asc'
    q = {}
    q.update(QUERY_ALL)
    q.update(_add_sort(sort_key, sort_order))
    return q


def query_films_by_genre(genres: list[str]) -> dict:
    q = {}
    q.update(_add_filter_genres(genres))
    return q


def query_films_by_genre_with_sort(genres: list[str], sort: str) -> dict:
    if '-' in sort:
        sort_key = sort.split('-')[1]
        sort_order = 'desc'
    else:
        sort_key = sort
        sort_order = 'asc'
    q = {}
    q.update(_add_filter_genres(genres))
    q.update(_add_sort(sort_key, sort_order))
    return q
