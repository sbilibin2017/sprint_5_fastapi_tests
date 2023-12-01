import json
from http import HTTPStatus
from pathlib import Path

import backoff
import psycopg
import pydantic
from conftest import test_settings
from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis

from utils.logger import logger
from utils.validator import ElasticPydantic

BASE_DIR = Path(__file__).resolve().parent


@backoff.on_exception(backoff.expo, Exception, max_tries=5)
async def get_es_conn(EsPydantic: pydantic.BaseModel) -> AsyncElasticsearch:
    """Get elasticsearch instance."""
    d = {"host": test_settings.ELASTIC_HOST,
         "port": test_settings.ELASTIC_PORT}
    d = EsPydantic(**d).dict()
    try:
        conn = AsyncElasticsearch(retry_on_timeout=True, **d)
        return conn
    except Exception as e:
        logger.error(e)


@backoff.on_exception(backoff.expo, Exception, max_tries=5)
async def get_redis_conn(RedisPydantic: pydantic.BaseModel) -> Redis.client:
    """Get redis instance."""
    d = {"host": test_settings.REDIS_HOST, "port": test_settings.REDIS_PORT}
    d = RedisPydantic(**d).dict()
    try:
        conn = await Redis(**d)
        return conn
    except Exception as e:
        logger.error(e)


async def prepare_es_cursor(mapping: str, index: str, es_cur: AsyncElasticsearch) -> AsyncElasticsearch:
    with open(BASE_DIR / "es_mapping" / mapping, "r") as f:
        mapping = json.load(f)
    indices = await es_cur.indices.get_alias()
    if index not in indices.keys():
        await es_cur.indices.create(index=index,
                                    ignore=HTTPStatus.BAD_REQUEST, body=mapping)
    await es_cur.indices.get_mapping(index)
    return es_cur


async def set_es_index(es_cur: AsyncElasticsearch) -> AsyncElasticsearch:
    """Set elasticsearch index."""
    for mapping, index in [
        (test_settings.ELASTIC_FILM_MAPPING_FILENAME,
         test_settings.ELASTIC_FILM_INDEX),
        (test_settings.ELASTIC_SEARCH_MAPPING_FILENAME,
         test_settings.ELASTIC_SEARCH_INDEX),
        (test_settings.ELASTIC_GENRE_MAPPING_FILENAME,
         test_settings.ELASTIC_GENRE_INDEX),
        (test_settings.ELASTIC_DIRECTOR_MAPPING_FILENAME,
         test_settings.ELASTIC_DIRECTOR_INDEX),
        (test_settings.ELASTIC_WRITER_MAPPING_FILENAME,
         test_settings.ELASTIC_WRITER_INDEX),
        (test_settings.ELASTIC_ACTOR_MAPPING_FILENAME,
         test_settings.ELASTIC_ACTOR_INDEX)
    ]:
        es_cur = await prepare_es_cursor(mapping, index, es_cur)
    return es_cur


async def init_es_index() -> AsyncElasticsearch:
    """Set connections to postgres, redis, elasticsearch, init state."""
    es_cur = await set_es_index(await get_es_conn(ElasticPydantic))
    # redis_conn = await get_redis_conn(RedisPydantic)
    # state = State(redis_conn)
    return es_cur


async def get_film_total_count(postgres_cur: psycopg.AsyncConnection.cursor) -> dict:
    """Get min and max date from postgres."""
    await postgres_cur.execute("""SELECT count(id) as count FROM film""")
    data = await postgres_cur.fetchall()
    count = data[0]['count']
    return count


async def close_connections(postgres_cur, es_cur):
    await postgres_cur.close()
    await es_cur.transport.close()
