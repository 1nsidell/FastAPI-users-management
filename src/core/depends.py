from src.core.db import DatabaseHelper, RepositoryUOW
from src.settings import settings


def get_db_helper(url: str) -> DatabaseHelper:
    return DatabaseHelper(url)


db_helper: DatabaseHelper = get_db_helper(settings.db.url)


def get_db_uow(db_helper: DatabaseHelper) -> RepositoryUOW:
    return RepositoryUOW(db_helper)


db_uow: RepositoryUOW = get_db_uow(db_helper)
