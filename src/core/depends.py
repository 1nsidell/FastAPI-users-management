"""Module core IOC container."""

from typing import Annotated, Callable

import redis.asyncio as redis
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import RedisConnectionManager, SQLDatabaseHelper, SQLRepositoryUOW
from src.settings import Settings, get_settings, settings

# Depends Settings instance
SettingsService = Annotated[Settings, Depends(get_settings)]


def get_sql_db_helper(settings: Settings) -> SQLDatabaseHelper:
    """Create an singleton instance of DB helper."""
    return SQLDatabaseHelper(
        url=settings.db.url,
        echo=settings.db.ECHO,
        echo_pool=settings.db.ECHO_POOL,
        pool_size=settings.db.POOL_SIZE,
        max_overflow=settings.db.MAX_OVERFLOW,
    )


# Singleton DBHelper instance
DBHelper: SQLDatabaseHelper = get_sql_db_helper(settings)


def get_async_session_factory() -> Callable[[], AsyncSession]:
    """Getting async session factory for Depends object."""
    return DBHelper.async_session_factory


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
    """Create an singleton instance of Redis pool connection."""
    return RedisConnectionManager(settings)


RedisManager: RedisConnectionManager = get_redis_pool_manager(settings)


def get_users_redis_pool() -> redis.Redis:
    """Create a Depends instance of Redis."""
    return RedisManager.redis


UsersRedisPool = Annotated[redis.Redis, Depends(get_users_redis_pool)]
