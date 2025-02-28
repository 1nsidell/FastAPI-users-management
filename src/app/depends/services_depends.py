from typing import Annotated

from fastapi import Depends

from src.app.depends import SQLRepository
from src.app.services import UsersManagementServiceProtocol
from src.core import UoW

from ..services.impls.users_management_service import UsersManagementServiceImpl


def get_users_service(
    users_sql_repository: SQLRepository,
    uow: UoW,
) -> UsersManagementServiceProtocol:
    return UsersManagementServiceImpl(users_sql_repository, uow)


UsersService = Annotated[
    UsersManagementServiceProtocol, Depends(get_users_service)
]
