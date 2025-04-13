"""
A module that describes an implementation for interacting with cache storage.
"""

from datetime import timedelta
import logging
from typing import List, Optional, Self

import redis.asyncio as redis

from users_management.app.schemas.users import SInfoUser
from users_management.core.settings import Settings
from users_management.gateways.repositories import (
    UsersCacheRepositoryProtocol,
    handle_redis_exceptions,
)

log = logging.getLogger(__name__)


class UsersCacheRepositoryImpl(UsersCacheRepositoryProtocol):
    def __init__(self: Self, redis: redis.Redis, settings: Settings) -> None:
        self.__redis = redis
        self.__settings = settings
        self.__expiration = int(
            timedelta(
                minutes=self.__settings.redis.CACHE_LIFETIME
            ).total_seconds()
        )

    @handle_redis_exceptions
    async def add_user(self: Self, key: int, data: SInfoUser) -> None:
        log.info("Adding cache by key: %s.", key)
        json_data = data.model_dump_json()
        await self.__redis.set(key, json_data, ex=self.__expiration)

    @handle_redis_exceptions
    async def get_user(self: Self, key: int) -> Optional[SInfoUser]:
        log.info("Searching the cache by key: %s.", key)
        value = await self.__redis.get(key)
        return SInfoUser.model_validate_json(value) if value else None

    @handle_redis_exceptions
    async def delete_user(self: Self, key: int) -> None:
        log.info("Deleting the cache by key: %s.", key)
        await self.__redis.delete(key)

    @handle_redis_exceptions
    async def add_list_users(
        self,
        data_list: List[SInfoUser],
    ) -> None:
        pipeline = self.__redis.pipeline()
        for user in data_list:
            key = user.user_id
            value = user.model_dump_json()
            pipeline.set(key, value, ex=self.__expiration)
        await pipeline.execute()

    @handle_redis_exceptions
    async def get_list_users(
        self, keys: List[int]
    ) -> Optional[List[SInfoUser]]:
        values = await self.__redis.mget(keys)

        if any(v is None for v in values):
            log.info("Some keys not found in cache: %s.", keys)
            return None

        return [SInfoUser.model_validate_json(v) for v in values if v]
