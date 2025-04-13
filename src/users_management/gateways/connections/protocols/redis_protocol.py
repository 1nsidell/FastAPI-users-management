"""Module related to connection to repositories."""

from abc import abstractmethod
from typing import Protocol, Self

import redis.asyncio as redis


class RedisConnectionManagerProtocol(Protocol):
    """A class for getting an instance of the redis pool."""

    @abstractmethod
    def startup(self: Self) -> None:
        """Redis pool creation."""
        ...

    @abstractmethod
    def redis(self) -> redis.Redis: ...

    @abstractmethod
    async def shutdown(self: Self) -> None: ...
