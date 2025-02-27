from src.app.repositories import SQLRepositoryProtocol
from src.app.repositories.sql.impls.sql_repository import SQLRepositoryImpl


def get_sql_repository() -> SQLRepositoryProtocol:
    return SQLRepositoryImpl()


SQLRepository: SQLRepositoryProtocol = get_sql_repository()
