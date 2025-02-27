from src.app.depends import SQLRepository
from src.app.repositories import SQLRepositoryProtocol
from src.app.services import UsersManagementServiceProtocol
from src.core.db import UOWFactory
from src.core.depends import uow_factory

from ..services.impls.users_management_service import UsersManagementServiceImpl


def get_users_service(
    sql_repository: SQLRepositoryProtocol,
    uow_factory: UOWFactory,
) -> UsersManagementServiceProtocol:
    return UsersManagementServiceImpl(sql_repository, uow_factory)


UsersService: UsersManagementServiceProtocol = get_users_service(
    SQLRepository,
    uow_factory,
)
