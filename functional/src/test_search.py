import random
import uuid
from http import HTTPStatus

import pytest
from conftest import test_settings
from test_data.test_search import es_generate_search_data

from utils.compare_answer import compare_answer

rnd = random.Random()
rnd.seed(test_settings.SEED + 7)
random_uuid = str(uuid.UUID(int=rnd.getrandbits(128), version=4))

es_search_data = es_generate_search_data()


@pytest.mark.parametrize(
    'es_data, query_data, expected_answer',
    [
        (
            es_search_data,
            {'search': '?title=The Star'},
            {'status': HTTPStatus.OK, 'length': 10, 'page': 1, 'size': 10}

        ),
        (
            es_search_data,
            {'search': '?title=The Star&page=2'},
            {'status': HTTPStatus.OK, 'length': 10, 'page': 2, 'size': 10}

        ),
        (
            es_search_data,
            {'search': '?title=The Star&page=2&size=100'},
            {'status': HTTPStatus.OK, 'length': 100, 'page': 2, 'size': 100}

        ),
        (
            es_search_data,
            {'search': '?title=Wrong title'},
            {'status': HTTPStatus.NOT_FOUND, 'detail': 'film not found'}
        ),
    ]
)
@ pytest.mark.asyncio
async def test_search(make_get_request, es_write_data, es_data: list[dict], query_data: dict, expected_answer: dict):
    await es_write_data(es_data, test_settings.ELASTIC_SEARCH_INDEX)
    anwers = await make_get_request('/search', query_data)
    for status, body in anwers:
        compare_answer(status, body, expected_answer)
