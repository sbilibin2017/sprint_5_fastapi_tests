from typing import Any

from redis.asyncio import Redis


class State:
    """Class for fixing and receiving etl status."""

    def __init__(self, redisclient: Redis) -> None:
        self.redisclient = redisclient

    async def set_state(self, key: str, values: list[str]) -> None:
        """Update status."""
        await self.redisclient.sadd(key, *values)
        await self.redisclient.save()

    async def get_state(self, key: str) -> Any:
        """Get status."""
        try:
            return tuple([i.decode('ascii') for i in await self.redisclient.smembers(key)])
        except Exception:
            return None
