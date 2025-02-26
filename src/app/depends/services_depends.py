from src.app.depends import SQLRepository
from src.app.repositories import SQLRepositoryProtocol
from src.app.services import UsersServiceImpl, UsersServiceProtocol
from src.core.db import RepositoryUOW
from src.core.depends import db_uow


def get_users_service(
    sql_repository: SQLRepositoryProtocol,
    db_uow: RepositoryUOW,
) -> UsersServiceProtocol:
    return UsersServiceImpl(sql_repository, db_uow)


UsersService: UsersServiceProtocol = get_users_service(SQLRepository, db_uow)
