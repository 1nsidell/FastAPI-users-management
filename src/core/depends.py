from src.core.db import DatabaseHelper, UOWFactory
from src.settings import settings


def get_db_helper(url: str) -> DatabaseHelper:
    return DatabaseHelper(url)


db_helper: DatabaseHelper = get_db_helper(settings.db.url)


def get_uow_factory(db_helper: DatabaseHelper) -> UOWFactory:
    return UOWFactory(db_helper)


uow_factory: UOWFactory = get_uow_factory(db_helper)
