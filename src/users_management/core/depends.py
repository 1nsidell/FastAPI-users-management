"""Module core IOC container."""

from typing import Annotated, Callable

import redis.asyncio as redis
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from users_management.core import (
    RedisConnectionManager,
    SQLDatabaseHelper,
    SQLRepositoryUOW,
)
from users_management.settings import Settings, get_settings, settings

# Depends Settings
SettingsService = Annotated[Settings, Depends(get_settings)]


def get_sql_db_helper(settings: Settings) -> SQLDatabaseHelper:
    """Create an singleton instance of SQL DB helper."""
    return SQLDatabaseHelper(settings=settings)


# Singleton SQLDBHelper instance
SQLDBHelper: SQLDatabaseHelper = get_sql_db_helper(settings)


def get_async_session_factory() -> Callable[[], AsyncSession]:
    """Getting async session factory for Depends object."""
    return SQLDBHelper.async_session_factory


AsyncSessionFactory = Annotated[
    Callable[[], AsyncSession], Depends(get_async_session_factory)
]


def get_uow(
    async_session_factory: AsyncSessionFactory,
) -> SQLRepositoryUOW:
    """Create a Depends instance of uow."""
    return SQLRepositoryUOW(async_session_factory)


UoW = Annotated[SQLRepositoryUOW, Depends(get_uow)]


def get_redis_pool_manager(settings: Settings) -> RedisConnectionManager:
    """Create an singleton instance of Redis pool connection manager."""
    return RedisConnectionManager(settings)


RedisManager: RedisConnectionManager = get_redis_pool_manager(settings)


def get_redis_pool() -> redis.Redis:
    """Create a Depends instance of Redis connection."""
    return RedisManager.redis


RedisPool = Annotated[redis.Redis, Depends(get_redis_pool)]
