import json
from functools import lru_cache

import pydantic
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from api.v1.schemas.film import FilmDetailSchema
from api.v1.schemas.genre import GenreDetailSchema
from api.v1.schemas.person import PersonDetailSchema
from core.config import Settings
from db.elastic import get_elastic
from db.redis import get_redis
from interfaces.CacheBase import AsyncCacheStorage
from interfaces.StorageBase import AsyncCollectionStorage

CONFIG = Settings()


class SearchService(AsyncCacheStorage, AsyncCollectionStorage):
    """Class for one film representation."""

    def __init__(self, cache: AsyncCacheStorage, storage: AsyncCollectionStorage):
        self.cache = cache
        self.storage = storage

    async def get_item_collection(
        self, body: dict, model: pydantic.BaseModel, index: str
    ) -> list[GenreDetailSchema] | list[PersonDetailSchema] | list[FilmDetailSchema] | None:
        """Gets all films."""
        title = body['query']['match']['title']['query']
        items = await self._get_from_cache(model, title)
        if items is None:
            resp = await self.storage.search(index=index, body=body, scroll=CONFIG.elastic.scroll)
            items = await self._get_item_collection_from_storage(model, resp)
            await self._put_to_cache(title, items)
        return items

    async def _get_item_collection_from_storage(
        self, model: pydantic.BaseModel, resp: AsyncElasticsearch.search
    ) -> list[GenreDetailSchema] | list[PersonDetailSchema] | list[FilmDetailSchema] | None:
        """Iterates elastic index and collects documents."""
        arr = []
        old_scroll_id = resp["_scroll_id"]
        for doc in resp["hits"]["hits"]:
            arr.append(model(**doc["_source"]))
        while len(resp["hits"]["hits"]):
            resp = await self.storage.scroll(scroll_id=old_scroll_id, scroll=CONFIG.elastic.scroll)
            old_scroll_id = resp["_scroll_id"]
            for doc in resp["hits"]["hits"]:
                arr.append(model(**doc["_source"]))
        return arr

    async def _get_from_cache(
        self, model: pydantic.BaseModel, title: str
    ) -> GenreDetailSchema | PersonDetailSchema | FilmDetailSchema | None:
        """Gets film if cached."""
        items = await self.cache.get(title)
        if items is not None:
            items = json.loads(items)
            return [model(**item) for item in items]

    async def _put_to_cache(self, title: str, items: list[pydantic.BaseModel]):
        """Update cache."""
        items = json.dumps([i.dict() for i in items])
        await self.cache.set(title, items, CONFIG.cache_expire_in_seconds)


@lru_cache()
def get_search_service(
    cache: AsyncCacheStorage = Depends(get_redis), storage: AsyncCollectionStorage = Depends(get_elastic)
) -> SearchService:
    return SearchService(cache, storage)
