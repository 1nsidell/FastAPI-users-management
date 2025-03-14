"""
ioc container for creating services.
"""

from typing import Annotated

from fastapi import Depends

from users_management.app.depends.repositories import (
    RedisUsersCacheRepository,
    UsersSQLRepository,
)
from users_management.app.services import UsersManagementServiceProtocol
from users_management.core import UoW

from ..services.impls.users_management import UsersManagementServiceImpl


def get_users_management_service(
    users_sql_repository: UsersSQLRepository,
    redis_users_cache: RedisUsersCacheRepository,
    uow: UoW,
) -> UsersManagementServiceProtocol:
    return UsersManagementServiceImpl(
        users_sql_repository,
        redis_users_cache,
        uow,
    )


UsersService = Annotated[
    UsersManagementServiceProtocol, Depends(get_users_management_service)
]
