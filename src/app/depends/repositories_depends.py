from src.app.repositories import SQLRepositoryImpl, SQLRepositoryProtocol


def get_sql_repository() -> SQLRepositoryProtocol:
    return SQLRepositoryImpl()


SQLRepository: SQLRepositoryProtocol = get_sql_repository()
