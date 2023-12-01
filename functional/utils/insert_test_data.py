
import json

from settings import test_settings

# async def insert_test_data(es_cur: AsyncElasticsearch, data: list[dict], index: str) -> dict:
#     for row in data:
#         yield {"_index": index, "_type": "_doc", "_id": row['id'], "_source": row}


def get_es_bulk_query(es_data) -> str:
    bulk_query = []
    for row in es_data:
        bulk_query.extend([
            json.dumps({'index': {'_index': test_settings.ELASTIC_SEARCH_INDEX,
                       '_id': row[test_settings.ELASTIC_ID_KEY]}}),
            json.dumps(row)
        ])
    str_query = '\n'.join(bulk_query) + '\n'
    return str_query
