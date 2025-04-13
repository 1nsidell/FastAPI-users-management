"""
ioc container for creating repositories.
"""

from typing import Annotated

from fastapi import Depends

from users_management.core.settings import SettingsService
from users_management.gateways.depends import RedisPool
from users_management.gateways.repositories import (
    UsersCacheRepositoryProtocol,
    UsersSQLRepositoryProtocol,
)
from users_management.gateways.repositories.impls.users_cache import (
    UsersCacheRepositoryImpl,
)
from users_management.gateways.repositories.impls.users_sql import (
    UsersSQLRepositoryImpl,
)


def get_users_repository() -> UsersSQLRepositoryProtocol:
    return UsersSQLRepositoryImpl()


UsersSQLRepository = Annotated[
    UsersSQLRepositoryProtocol, Depends(get_users_repository)
]


def get_users_cache_repository(
    redis_pool: RedisPool,
    settings: SettingsService,
) -> UsersCacheRepositoryProtocol:
    return UsersCacheRepositoryImpl(redis_pool, settings)


RedisUsersCacheRepository = Annotated[
    UsersCacheRepositoryProtocol, Depends(get_users_cache_repository)
]
