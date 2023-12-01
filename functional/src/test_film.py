import random
import uuid
from http import HTTPStatus

import pytest

from conftest import test_settings
from test_data.test_film import es_generate_film_data
from utils.compare_answer import compare_answer

rnd = random.Random()
rnd.seed(test_settings.SEED + 6)
random_uuid = str(uuid.UUID(int=rnd.getrandbits(128), version=4))

es_film_data = es_generate_film_data()


@pytest.mark.parametrize(
    'es_data, query_data, expected_answer',
    [
        (
            es_film_data,
            {'films': None},
            {'status': HTTPStatus.OK, 'length': 10, 'page': 1, 'size': 10}

        ),
        (
            es_film_data,
            {'films': '?sort=-imdb_rating'},
            {'status': HTTPStatus.OK, 'length': 10, 'page': 1, 'size': 10}

        ),
        (
            es_film_data,
            {'films': '?genres=Family'},
            {'status': HTTPStatus.OK, 'length': 10, 'page': 1, 'size': 10}

        ),
        (
            es_film_data,
            {f'films/{random_uuid}': None},
            {'status': HTTPStatus.OK, 'id': random_uuid}

        ),
        (
            es_film_data,
            {'films/wrong_uuid': None},
            {'status': HTTPStatus.NOT_FOUND, 'detail': 'film not found'}
        ),
    ]
)
@ pytest.mark.asyncio
async def test_film(make_get_request, es_write_data, es_data: list[dict], query_data: dict, expected_answer: dict):
    await es_write_data(es_data, test_settings.ELASTIC_FILM_INDEX)
    anwers = await make_get_request('/films', query_data)
    for status, body in anwers:
        compare_answer(status, body, expected_answer)
