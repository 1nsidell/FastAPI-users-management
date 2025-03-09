"""
ioc container for creating repositories.
"""

from typing import Annotated

from fastapi import Depends

from src.app.repositories import (
    CacheRepositoryProtocol,
    UsersSQLRepositoryProtocol,
)
from src.app.repositories.impls.users_cache_repository import (
    UsersCacheRepositoryImpl,
)
from app.repositories.impls.users_sql_repository import (
    UsersSQLRepositoryImpl,
)
from src.core import SettingsService, UsersRedisPool


def get_users_sql_repository() -> UsersSQLRepositoryProtocol:
    return UsersSQLRepositoryImpl()


UsersSQLRepository = Annotated[
    UsersSQLRepositoryProtocol, Depends(get_users_sql_repository)
]


def get_users_cache_repository(
    redis_pool: UsersRedisPool,
    settings: SettingsService,
) -> CacheRepositoryProtocol:
    return UsersCacheRepositoryImpl(redis_pool, settings)


RedisUsersCacheRepository = Annotated[
    CacheRepositoryProtocol, Depends(get_users_cache_repository)
]
