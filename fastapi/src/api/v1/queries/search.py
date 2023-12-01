def query_film_by_title(title: str) -> dict:
    return {
        "query": {
            "match": {
                "title": {
                    "query": title,
                    "fuzziness": "AUTO"
                }
            }
        }
    }
