"""
ioc container for creating services.
"""

from typing import Annotated

from fastapi import Depends

from users_management.app.services import UsersManagementServiceProtocol
from users_management.gateways.depends import UoW
from users_management.gateways.depends.repositories import (
    RedisUsersCacheRepository,
    UsersSQLRepository,
)

from ..services.impls.users_management import UsersManagementServiceImpl


def get_users_management_service(
    users_repository: UsersSQLRepository,
    users_cache: RedisUsersCacheRepository,
    uow: UoW,
) -> UsersManagementServiceProtocol:
    return UsersManagementServiceImpl(
        users_repository,
        users_cache,
        uow,
    )


UsersService = Annotated[
    UsersManagementServiceProtocol, Depends(get_users_management_service)
]
