from typing import Annotated

from fastapi import Depends
import redis.asyncio as redis

from src.app.repositories.sql.impls.users_repository import (
    UsersSQLRepositoryImpl,
)
from src.app.repositories.redis.impls.users_cache_repository import (
    RedisUsersCacheImpl,
)
from src.app.repositories import (
    UsersSQLRepositoryProtocol,
    CacheRepositoryProtocol,
)
from src.core import SettingsService


def get_users_sql_repository() -> UsersSQLRepositoryProtocol:
    return UsersSQLRepositoryImpl()


UsersSQLRepository = Annotated[
    UsersSQLRepositoryProtocol, Depends(get_users_sql_repository)
]


def get_users_redis_pool(settings: SettingsService) -> redis.ConnectionPool:
    return redis.ConnectionPool.from_url(
        settings.redis.users_cache_url,
        decode_responses=True,
    )


UsersRedisPool = Annotated[redis.ConnectionPool, Depends(get_users_redis_pool)]


def get_users_cache_repository(
    redis_pool: UsersRedisPool,
) -> CacheRepositoryProtocol:
    return RedisUsersCacheImpl(redis_pool)


RedisUsersCacheRepository = Annotated[
    CacheRepositoryProtocol, Depends(get_users_cache_repository)
]
