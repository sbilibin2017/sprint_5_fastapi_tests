import random
import uuid
from http import HTTPStatus

import pytest

from conftest import test_settings
from test_data.test_genre import es_generate_genre_data
from utils.compare_answer import compare_answer

rnd = random.Random()
rnd.seed(test_settings.SEED + 3)
random_uuid = str(uuid.UUID(int=rnd.getrandbits(128), version=4))

es_genre_data = es_generate_genre_data()


@pytest.mark.parametrize(
    'es_data, query_data, expected_answer',
    [
        (
            es_genre_data,
            {'genres': None},
            {'status': HTTPStatus.OK, 'length': 10, 'page': 1, 'size': 10}

        ),
        (
            es_genre_data,
            {f'genres/{random_uuid}': None},
            {'status': HTTPStatus.OK, 'id': random_uuid}

        ),
        (
            es_genre_data,
            {'genres/wrong_uuid': None},
            {'status': HTTPStatus.NOT_FOUND, 'detail': 'genre not found'}
        ),
    ]
)
@ pytest.mark.asyncio
async def test_genre(make_get_request, es_write_data, es_data: list[dict], query_data: dict, expected_answer: dict):
    await es_write_data(es_data, test_settings.ELASTIC_GENRE_INDEX)
    anwers = await make_get_request('/genres', query_data)
    for status, body in anwers:
        compare_answer(status, body, expected_answer)
