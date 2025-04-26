from typing import Annotated, Callable, Final

from fastapi import Depends
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from users_management.core.settings import (
    RedisConfig,
    SQLDatabaseConfig,
    settings,
)
from users_management.gateways.connections import (
    GatewayConnectionProtocol,
)
from users_management.gateways.connections.impls.redis import (
    RedisConnectionManagerImpl,
)
from users_management.gateways.connections.impls.sql import (
    SQLDatabaseManagerImpl,
)


# ================== Global Instances (for lifespan) ==================
def get_sql_db_helper(
    config: SQLDatabaseConfig,
) -> GatewayConnectionProtocol[async_sessionmaker[AsyncSession]]:
    return SQLDatabaseManagerImpl(config=config)


SQLDBHelper: Final[
    GatewayConnectionProtocol[async_sessionmaker[AsyncSession]]
] = get_sql_db_helper(config=settings.sql_db)


def get_redis_manager(
    config: RedisConfig,
) -> GatewayConnectionProtocol[redis.Redis]:
    return RedisConnectionManagerImpl(config=config)


RedisManager: Final[GatewayConnectionProtocol[redis.Redis]] = get_redis_manager(
    config=settings.redis
)


# ================== SQL Database Dependencies ==================
def get_async_session_factory() -> async_sessionmaker[AsyncSession]:
    """Getting async session factory for Depends object."""
    return SQLDBHelper.get_connection()


AsyncSessionFactory = Annotated[
    Callable[[], AsyncSession], Depends(get_async_session_factory)
]


# ================== Redis Dependencies ==================
def get_redis_pool() -> redis.Redis:
    """Create a Depends instance of Redis connection."""
    return RedisManager.get_connection()


RedisPool = Annotated[redis.Redis, Depends(get_redis_pool)]
