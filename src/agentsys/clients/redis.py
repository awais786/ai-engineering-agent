from __future__ import annotations


class RedisClient:
    """STUB. TODO: implement Redis cache/queue."""

    async def get(self, key: str) -> str | None:
        raise NotImplementedError("RedisClient.get is not implemented yet")

    async def set(self, key: str, value: str) -> None:
        raise NotImplementedError("RedisClient.set is not implemented yet")
