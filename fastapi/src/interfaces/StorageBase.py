from abc import ABC, abstractmethod


class AsyncDetailStorage(ABC):
    @abstractmethod
    async def get_item_by_id():
        pass

    @abstractmethod
    async def _get_item_from_storage():
        pass


class AsyncCollectionStorage(ABC):
    @abstractmethod
    async def get_item_collection():
        pass

    @abstractmethod
    async def _get_item_collection_from_storage():
        pass
