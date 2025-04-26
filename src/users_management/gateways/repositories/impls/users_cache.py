"""
A module that describes an implementation for interacting with cache storage.
"""

from datetime import timedelta
import logging
from typing import List, Optional, Self

import redis.asyncio as redis

from users_management.app.schemas.users import SInfoUser
from users_management.core.settings import RedisConfig
from users_management.gateways.repositories import (
    CacheRepositoryProtocol,
    handle_redis_exceptions,
)


log = logging.getLogger(__name__)


class UsersCacheRepositoryImpl(CacheRepositoryProtocol[SInfoUser]):
    def __init__(self: Self, redis: redis.Redis, config: RedisConfig) -> None:
        self._redis = redis
        self._config = config
        self._expiration = int(
            timedelta(minutes=self._config.CACHE_LIFETIME).total_seconds()
        )

    @handle_redis_exceptions
    async def add(self: Self, key: str, data: SInfoUser) -> None:
        log.info("Adding cache by key: %s.", key)
        json_data = data.model_dump_json()
        await self._redis.set(key, json_data, ex=self._expiration)

    @handle_redis_exceptions
    async def get(self: Self, key: str) -> Optional[SInfoUser]:
        log.info("Searching the cache by key: %s.", key)
        value = await self._redis.get(key)
        return SInfoUser.model_validate_json(value) if value else None

    @handle_redis_exceptions
    async def delete(self: Self, key: str) -> None:
        log.info("Deleting the cache by key: %s.", key)
        await self._redis.delete(key)

    @handle_redis_exceptions
    async def add_list(
        self,
        data_list: List[SInfoUser],
    ) -> None:
        pipeline = self._redis.pipeline()
        for user in data_list:
            key = self.get_key_by_user_id(user.user_id)
            value = user.model_dump_json()
            pipeline.set(key, value, ex=self._expiration)
        await pipeline.execute()

    @handle_redis_exceptions
    async def get_list(self, keys: List[str]) -> Optional[List[SInfoUser]]:
        values = await self._redis.mget(keys)

        if any(v is None for v in values):
            log.info("Some keys not found in cache: %s.", keys)
            return None

        return [SInfoUser.model_validate_json(v) for v in values if v]
