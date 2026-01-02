from typing import Any

from redis.asyncio import Redis


class Cache:
    """单例"""
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.redis_connect = None

    def init_redis(self, redis: Redis):
        self.redis_connect = redis

    def get_redis_connect(self) -> Redis:
        return self.redis_connect

    async def set(self, key: str, value: str, ex: int = None):
        await self.redis_connect.set(key, value, ex=ex)

    async def get(self, key: str) -> Any:
        return await self.redis_connect.get(key)

# 全局实例
cache = Cache()

__all__ = ["cache"]