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
        self.__settings = settings
        self.__url: str = self.__settings.redis.users_cache_url
        self.__pool: redis.ConnectionPool
        self.__redis: redis.Redis

    def startup(self: Self) -> None:
        """Redis pool creation."""
        try:
            self.__pool = redis.ConnectionPool.from_url(
                self.__url,
                decode_responses=True,
            )
            log.info("Redis conn pool [%s] is created.", id(self.__pool))
            self.__redis = redis.Redis(connection_pool=self.__pool)
            log.info("Redis instance [%s] is created.", id(self.__redis))
        except RedisError as e:
            log.error("Failed to initialize redis.", exc_info=True)
            raise RedisCacheDBException(e)

    @property
    def redis(self) -> redis.Redis:
        return self.__redis

    async def shutdown(self: Self) -> None:
        """Closing a connection to Redis."""
        if self.__redis:
            await self.__redis.aclose()
            log.info("Redis instance [%s] is closed.", id(self.__redis))
        if self.__pool:
            await self.__pool.disconnect()
            log.info("Redis conn pool [%s] is closed.", id(self.__pool))
