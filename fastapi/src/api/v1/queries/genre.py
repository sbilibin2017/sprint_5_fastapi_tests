from core.config import Settings

CONFIG = Settings()


def query_genre() -> dict:
    return {
        "size": CONFIG.elastic.scroll_size,
        "query": {"match_all": {}},
    }
