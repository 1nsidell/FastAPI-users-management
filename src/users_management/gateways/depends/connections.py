from typing import Annotated, Callable, Final

from fastapi import Depends
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession

from users_management.core.settings import Settings, settings
from users_management.gateways.connections import (
    RedisConnectionManagerProtocol,
    SQLDatabaseHelperProtocol,
)
from users_management.gateways.connections.impls.redis import (
    RedisConnectionManagerImpl,
)
from users_management.gateways.connections.impls.sql import (
    SQLDatabaseHelperImpl,
)
from users_management.gateways.transactions import SQLRepositoryUOW


# ================== Global Instances (for lifespan) ==================
def get_sql_db_helper(settings: Settings) -> SQLDatabaseHelperProtocol:
    return SQLDatabaseHelperImpl(settings=settings)


SQLDBHelper: Final[SQLDatabaseHelperProtocol] = get_sql_db_helper(settings)


def get_redis_manager(settings: Settings) -> RedisConnectionManagerProtocol:
    return RedisConnectionManagerImpl(settings)


RedisManager: Final[RedisConnectionManagerProtocol] = get_redis_manager(
    settings
)


# ================== SQL Database Dependencies ==================
def get_async_session_factory() -> Callable[[], AsyncSession]:
    """Getting async session factory for Depends object."""
    return SQLDBHelper.async_session_factory


AsyncSessionFactory = Annotated[
    Callable[[], AsyncSession], Depends(get_async_session_factory)
]


def get_uow(async_session_factory: AsyncSessionFactory) -> SQLRepositoryUOW:
    """Create a Depends instance of uow."""
    return SQLRepositoryUOW(async_session_factory)


UoW = Annotated[SQLRepositoryUOW, Depends(get_uow)]


# ================== Redis Dependencies ==================
def get_redis_pool() -> redis.Redis:
    """Create a Depends instance of Redis connection."""
    return RedisManager.redis


RedisPool = Annotated[redis.Redis, Depends(get_redis_pool)]
