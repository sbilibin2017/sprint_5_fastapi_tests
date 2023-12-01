from functools import lru_cache

import pydantic
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from api.v1.schemas.film import FilmDetailSchema
from api.v1.schemas.genre import GenreDetailSchema
from api.v1.schemas.person import PersonDetailSchema
from core.config import Settings
from db.elastic import get_elastic
from db.redis import get_redis
from interfaces.CacheBase import AsyncCacheStorage
from interfaces.StorageBase import AsyncDetailStorage

CONFIG = Settings()


class DetailService(AsyncCacheStorage, AsyncDetailStorage):
    """Class for one film representation."""

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_item_by_id(
        self, model: pydantic.BaseModel, index: str, id: str
    ) -> GenreDetailSchema | PersonDetailSchema | FilmDetailSchema | None:
        """Gets film from_elastic by id."""
        item = await self._get_from_cache(model, id)
        if not item:
            item = await self._get_item_from_storage(model, index, id)
        if item is not None:
            await self._put_to_cache(item)
        return item

    async def _get_item_from_storage(
        self, model: pydantic.BaseModel, index: str, id: str
    ) -> GenreDetailSchema | PersonDetailSchema | FilmDetailSchema | None:
        """Gets film if not cached."""
        try:
            doc = await self.elastic.get(index, id)
        except NotFoundError:
            return None

        return model(**doc["_source"])

    async def _get_from_cache(
        self, model: pydantic.BaseModel, id: str
    ) -> GenreDetailSchema | PersonDetailSchema | FilmDetailSchema | None:
        """Gets film if cached."""
        data = await self.redis.get(id)
        if not data:
            return None
        return model.parse_raw(data)

    async def _put_to_cache(self, item: pydantic.BaseModel):
        """Update cache."""
        await self.redis.set(item.id, item.json(), CONFIG.cache_expire_in_seconds)


@lru_cache()
def get_detail_service(
    cache: AsyncCacheStorage = Depends(get_redis), storage: AsyncDetailStorage = Depends(get_elastic)
) -> DetailService:
    return DetailService(cache, storage)
