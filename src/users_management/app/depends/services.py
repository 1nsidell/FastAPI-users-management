from typing import Annotated

from fastapi import Depends

from users_management.app.depends import RepositoryManager
from users_management.app.depends.repositories import RedisUsersCacheRepository
from users_management.app.depends.utils_factory import KeyByUserIdBuilder
from users_management.app.services import UsersServiceProtocol

from ..services.impls.users import UsersServiceImpl


def get_users_management_service(
    repository_manager: RepositoryManager,
    users_cache: RedisUsersCacheRepository,
    key_builder: KeyByUserIdBuilder,
) -> UsersServiceProtocol:
    return UsersServiceImpl(
        repository_manager=repository_manager,
        users_cache=users_cache,
        key_builder=key_builder,
    )


UsersService = Annotated[
    UsersServiceProtocol, Depends(get_users_management_service)
]
