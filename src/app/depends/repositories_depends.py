from src.app.repositories import SQLRepositoryProtocol, SQLRepositoryImpl


def get_sql_repository() -> SQLRepositoryProtocol:
    return SQLRepositoryImpl()


SQLRepository: SQLRepositoryProtocol = get_sql_repository()
