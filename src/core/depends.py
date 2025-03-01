"""Module core IOC container."""

from typing import Annotated

from fastapi import Depends

from src.core import DatabaseHelperProtocol, RepositoryUOWProtocol
from src.core.db import DatabaseHelperImpl, RepositoryUOWImpl
from src.settings import Settings, get_settings


SettingsService = Annotated[Settings, Depends(get_settings)]


def get_db_helper(settings: SettingsService) -> DatabaseHelperProtocol:
    return DatabaseHelperImpl(
        url=settings.db.url,
        echo=settings.db.ECHO,
        echo_pool=settings.db.ECHO_POOL,
        pool_size=settings.db.POOL_SIZE,
        max_overflow=settings.db.MAX_OVERFLOW,
    )


DBHelper = Annotated[DatabaseHelperProtocol, Depends(get_db_helper)]


def get_uow(db_helper: DBHelper) -> RepositoryUOWProtocol:
    return RepositoryUOWImpl(db_helper)


UoW = Annotated[RepositoryUOWProtocol, Depends(get_uow)]
