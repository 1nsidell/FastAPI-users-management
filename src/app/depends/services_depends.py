from src.app.depends import SQLRepository
from src.app.repositories import SQLRepositoryProtocol
from src.app.services import UsersManagementServiceProtocol
from src.core.db import RepositoryUOW
from src.core.depends import db_uow

from ..services.impls.users_management_service import UsersManagementServiceImpl


def get_users_service(
    sql_repository: SQLRepositoryProtocol,
    db_uow: RepositoryUOW,
) -> UsersManagementServiceProtocol:
    return UsersManagementServiceImpl(sql_repository, db_uow)


UsersService: UsersManagementServiceProtocol = get_users_service(
    SQLRepository,
    db_uow,
)
