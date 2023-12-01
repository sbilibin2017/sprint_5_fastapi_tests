import random
import uuid
from http import HTTPStatus

import pytest

from conftest import test_settings
from test_data.test_director import es_generate_director_data
from utils.compare_answer import compare_answer

rnd = random.Random()
rnd.seed(test_settings.SEED + 2)
random_uuid = str(uuid.UUID(int=rnd.getrandbits(128), version=4))

es_director_data = es_generate_director_data()


@pytest.mark.parametrize(
    'es_data, query_data, expected_answer',
    [
        (
            es_director_data,
            {'directors': None},
            {'status': HTTPStatus.OK, 'length': 10, 'page': 1, 'size': 10}

        ),
        (
            es_director_data,
            {f'directors/{random_uuid}': None},
            {'status': HTTPStatus.OK, 'id': random_uuid}

        ),
        (
            es_director_data,
            {'directors/wrong_uuid': None},
            {'status': HTTPStatus.NOT_FOUND, 'detail': 'director not found'}
        ),
    ]
)
@ pytest.mark.asyncio
async def test_director(make_get_request, es_write_data, es_data: list[dict], query_data: dict, expected_answer: dict):
    await es_write_data(es_data, test_settings.ELASTIC_DIRECTOR_INDEX)
    anwers = await make_get_request('/actors', query_data)
    for status, body in anwers:
        compare_answer(status, body, expected_answer)
