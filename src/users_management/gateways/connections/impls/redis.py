"""Module related to connection to repositories."""

import logging
from typing import Self

import redis.asyncio as redis
from redis.exceptions import RedisError

from users_management.app.exceptions import (
    RedisCacheDBException,
)
from users_management.core.settings import Settings
from users_management.gateways.connections import (
    RedisConnectionManagerProtocol,
)


log = logging.getLogger(__name__)


class RedisConnectionManagerImpl(RedisConnectionManagerProtocol):
    """A class for getting an instance of the redis pool.

    Args:
        __settings (Settings): Application config.
    """

    def __init__(self: Self, settings: Settings):
        self._settings = settings
        self._url: str = self._settings.redis.users_cache_url
        self._pool: redis.ConnectionPool
        self._redis: redis.Redis

    def startup(self: Self) -> None:
        """Redis pool creation."""
        try:
            self._pool = redis.ConnectionPool.from_url(
                self._url,
                decode_responses=True,
            )
            log.info("Redis conn pool [%s] is created.", id(self._pool))
            self._redis = redis.Redis(connection_pool=self._pool)
            log.info("Redis instance [%s] is created.", id(self._redis))
        except RedisError as e:
            log.error("Failed to initialize redis.", exc_info=True)
            raise RedisCacheDBException(e)

    @property
    def redis(self) -> redis.Redis:
        return self._redis

    async def shutdown(self: Self) -> None:
        """Closing a connection to Redis."""
        if self._redis:
            await self._redis.aclose()
            log.info("Redis instance [%s] is closed.", id(self._redis))
        if self._pool:
            await self._pool.disconnect()
            log.info("Redis conn pool [%s] is closed.", id(self._pool))
