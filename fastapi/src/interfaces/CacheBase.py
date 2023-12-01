from abc import ABC, abstractmethod


class AsyncCacheStorage(ABC):
    @abstractmethod
    async def _get_from_cache(self, key: str, **kwargs):
        pass

    @abstractmethod
    async def _put_to_cache(self, key: str, value: str, expire: int, **kwargs):
        pass
