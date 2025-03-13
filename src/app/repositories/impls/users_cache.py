"""
A module that describes an implementation for interacting with cache storage.
"""

import json
import logging
from datetime import timedelta
from typing import Any, Dict, List, Optional, Self

import redis.asyncio as redis

from src.app.repositories import (
    UsersCacheRepositoryProtocol,
    handle_redis_exceptions,
)
from src.app.schemas.users import SInfoUser
from src.settings import Settings

log = logging.getLogger("app")


class UsersCacheRepositoryImpl(UsersCacheRepositoryProtocol):
    def __init__(self: Self, redis: redis.Redis, settings: Settings) -> None:
        self.redis = redis
        self.settings = settings
        self.expiration = int(
            timedelta(
                minutes=self.settings.redis.CACHE_LIFETIME
            ).total_seconds()
        )

    @handle_redis_exceptions
    async def add_user(self: Self, key: int, data: Dict[str, Any]) -> None:
        log.info("Adding cache by key: %s.", key)
        json_data = json.dumps(data)
        await self.redis.set(key, json_data, ex=self.expiration)

    @handle_redis_exceptions
    async def get_user(self: Self, key: int) -> Optional[Dict[str, Any]]:
        log.info("Searching the cache by key: %s.", key)
        value = await self.redis.get(key)
        return json.loads(value) if value else None

    @handle_redis_exceptions
    async def delete_user(self: Self, key: int) -> None:
        log.info("Deleting the cache by key: %s.", key)
        await self.redis.delete(key)

    @handle_redis_exceptions
    async def add_list_users(
        self,
        data_list: List[SInfoUser],
    ) -> None:
        pipeline = self.redis.pipeline()
        for user in data_list:
            key = user.user_id
            value = user.model_dump_json()
            pipeline.set(key, value, ex=self.expiration)
        await pipeline.execute()

    @handle_redis_exceptions
    async def get_list_users(self, keys: List[int]) -> Optional[List[Dict]]:
        values = await self.redis.mget(keys)

        if any(v is None for v in values):
            log.info("Some keys not found in cache: %s.", keys)
            return None

        return [json.loads(v) for v in values]
