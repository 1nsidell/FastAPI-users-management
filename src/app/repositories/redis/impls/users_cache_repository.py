"""
A module that describes an implementation for interacting with cache storage.
"""

import json
import logging
from datetime import timedelta
from typing import Any, Dict, List, Optional, Self

import redis.asyncio as redis

from src.app.exceptions import RedisCacheDBException
from src.app.repositories import (
    CacheRepositoryProtocol,
    handle_redis_exceptions,
)
from src.settings import Settings

log = logging.getLogger("app")


class RedisUsersCacheImpl(CacheRepositoryProtocol):
    def __init__(self: Self, redis: redis.Redis, settings: Settings) -> None:
        self.redis = redis
        self.settings = settings

    @handle_redis_exceptions
    async def add_user(self: Self, key: str, data: Dict[str, Any]) -> None:
        log.info("Adding cache by key: %s.", key)
        expiration = int(
            timedelta(
                minutes=self.settings.redis.USERS_CACHE_LIFETIME
            ).total_seconds()
        )
        json_data = json.dumps(data)
        await self.redis.set(key, json_data, ex=expiration)

    @handle_redis_exceptions
    async def get_user(self: Self, key: str) -> Optional[Dict[str, Any]]:
        log.info("Searching the cache by key: %s.", key)
        value = await self.redis.get(key)
        return json.loads(value) if value else None

    @handle_redis_exceptions
    async def delete_user(self: Self, key: str) -> None:
        log.info("Deleting the cache by key: %s.", key)
        await self.redis.delete(key)

    @handle_redis_exceptions
    async def add_list_users(
        self,
        keys: List[str],
        data_list: List[Dict],
    ) -> None:
        if len(keys) != len(data_list):
            raise RedisCacheDBException(
                "Keys and data_list must have the same length."
            )

        expiration = int(
            timedelta(
                minutes=self.settings.redis.USERS_CACHE_LIFETIME
            ).total_seconds()
        )
        pipeline = self.redis.pipeline()

        for key, data in zip(keys, data_list):
            pipeline.set(key, json.dumps(data), ex=expiration)

        await pipeline.execute()
        log.info("Cached %d items: %s.", len(keys), keys)

    @handle_redis_exceptions
    async def get_list_users(self, keys: List[str]) -> Optional[List[Dict]]:
        values = await self.redis.mget(keys)

        if any(v is None for v in values):
            log.info("Some keys not found in cache: %s.", keys)
            return None

        return [json.loads(v) for v in values]

    @handle_redis_exceptions
    async def delete_list_users(self, keys: List[str]) -> None:
        await self.redis.delete(*keys)
        log.info("Deleted %d items: %s.", len(keys), keys)
