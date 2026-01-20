from typing import Any, Optional

from redis.asyncio import Redis

from core.utils.JSONUtils import JSONUtils


class Cache:
    """单例"""
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.redis_connect: Optional[Redis] = None

    def init_redis(self, redis: Redis):
        self.redis_connect = redis

    def get_redis_connect(self) -> Redis:
        return self.redis_connect

    async def set(self, key: str, value: str, ex: int = None):
        """
        设置缓存
        :param key: key值
        :param value:  缓存值
        :param ex: 过期时间,单位毫秒
        :return:
        """
        await self.redis_connect.set(key, value, ex=ex)

    async def get(self, key: str) -> Any:
        return await self.redis_connect.get(key)

    async def delete(self, key: str) -> Any:
        return await self.redis_connect.delete(key)

    async def fetch_like(self, pattern) -> Any:
        self.redis_connect.keys()
        keys = await self.redis_connect.keys(pattern)
        data_list = []
        for key in keys:
            cache_data = await self.get(key)
            data_list.append(JSONUtils.loads(cache_data))
        return data_list

# 全局实例
cache = Cache()

__all__ = ["cache"]