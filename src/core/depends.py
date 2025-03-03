"""Module core IOC container."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.core import DatabaseHelperProtocol, SQLRepositoryUOWProtocol
from src.core.db import (
    DatabaseHelperImpl,
    SQLRepositoryUOWImpl,
    RedisPoolManagerImpl,
)
from src.settings import Settings, get_settings, settings

# Depends Settings instance
SettingsService = Annotated[Settings, Depends(get_settings)]


def get_db_helper(settings: Settings) -> DatabaseHelperProtocol:
    """Create an singleton instance of DB helper."""
    return DatabaseHelperImpl(
        url=settings.db.url,
        echo=settings.db.ECHO,
        echo_pool=settings.db.ECHO_POOL,
        pool_size=settings.db.POOL_SIZE,
        max_overflow=settings.db.MAX_OVERFLOW,
    )


# Singleton DBHelper instance
DBHelper: DatabaseHelperProtocol = get_db_helper(settings)


def get_async_session_factory() -> async_sessionmaker[AsyncSession]:
    """Getting async session factory for Depends object."""
    return DBHelper.async_session_factory


AsyncSessionFactory = Annotated[
    async_sessionmaker[AsyncSession], Depends(get_async_session_factory)
]


def get_uow(
    async_session_factory: AsyncSessionFactory,
) -> SQLRepositoryUOWProtocol:
    """Create a Depends instance of uow."""
    return SQLRepositoryUOWImpl(async_session_factory)


UoW = Annotated[SQLRepositoryUOWImpl, Depends(get_uow)]


def get_redis_pool_manager(settings: Settings) -> RedisPoolManagerImpl:
    """Create an singleton instance of Redis pool connection."""
    return RedisPoolManagerImpl(settings)


RedisPoolManager: RedisPoolManagerImpl = get_redis_pool_manager(settings)
