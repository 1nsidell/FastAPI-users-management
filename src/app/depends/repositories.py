"""
ioc container for creating repositories.
"""

from typing import Annotated

from fastapi import Depends

from src.app.repositories import (
    UsersCacheRepositoryProtocol,
    UsersSQLRepositoryProtocol,
)
from src.app.repositories.impls.users_cache import (
    UsersCacheRepositoryImpl,
)
from src.app.repositories.impls.users_sql import (
    UsersSQLRepositoryImpl,
)
from src.core import RedisPool, SettingsService


def get_users_sql_repository() -> UsersSQLRepositoryProtocol:
    return UsersSQLRepositoryImpl()


UsersSQLRepository = Annotated[
    UsersSQLRepositoryProtocol, Depends(get_users_sql_repository)
]


def get_users_cache_repository(
    redis_pool: RedisPool,
    settings: SettingsService,
) -> UsersCacheRepositoryProtocol:
    return UsersCacheRepositoryImpl(redis_pool, settings)


RedisUsersCacheRepository = Annotated[
    UsersCacheRepositoryProtocol, Depends(get_users_cache_repository)
]
