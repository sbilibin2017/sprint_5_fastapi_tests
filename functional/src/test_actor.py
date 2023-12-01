import random
import uuid
from http import HTTPStatus

import pytest

from conftest import test_settings
from test_data.test_actor import es_generate_actor_data
from utils.compare_answer import compare_answer

rnd = random.Random()
rnd.seed(test_settings.SEED + 1)
random_uuid = str(uuid.UUID(int=rnd.getrandbits(128), version=4))

es_actor_data = es_generate_actor_data()


@pytest.mark.parametrize(
    'es_data, query_data, expected_answer',
    [
        (
            es_actor_data,
            {'actors': None},
            {'status': HTTPStatus.OK, 'length': 10, 'page': 1, 'size': 10}

        ),
        (
            es_actor_data,
            {f'actors/{random_uuid}': None},
            {'status': HTTPStatus.OK, 'id': random_uuid}

        ),
        (
            es_actor_data,
            {'actors/wrong_uuid': None},
            {'status': HTTPStatus.NOT_FOUND, 'detail': 'actor not found'}
        ),
    ]
)
@ pytest.mark.asyncio
async def test_actor(make_get_request, es_write_data, es_data: list[dict], query_data: dict, expected_answer: dict):
    await es_write_data(es_data, test_settings.ELASTIC_ACTOR_INDEX)
    anwers = await make_get_request('/actors', query_data)
    for status, body in anwers:
        compare_answer(status, body, expected_answer)
