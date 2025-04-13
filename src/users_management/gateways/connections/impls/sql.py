"""Module related to connection to repositories."""

import logging
from typing import Callable, Optional, Self

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from users_management.app.exceptions import (
    SQLRepositoryException,
)
from users_management.core.settings import Settings
from users_management.gateways.connections import (
    SQLDatabaseHelperProtocol,
)

log = logging.getLogger(__name__)


class SQLDatabaseHelperImpl(SQLDatabaseHelperProtocol):
    """Class helping to async connect to SQL database.

    Args:
        __settings (Settings): Application config.
    """

    def __init__(self: Self, settings: Settings):
        self.__settings = settings
        self.__url: str = self.__settings.sql_db.url
        self.__echo: bool = self.__settings.sql_db.ECHO
        self.__echo_pool: bool = self.__settings.sql_db.ECHO_POOL
        self.__pool_size: int = self.__settings.sql_db.POOL_SIZE
        self.__max_overflow: int = self.__settings.sql_db.MAX_OVERFLOW

        self.__engine: Optional[AsyncEngine]
        self.__async_session_factory: Optional[async_sessionmaker[AsyncSession]]

    def startup(self: Self) -> None:
        """Initialize the database engine and session factory."""
        try:
            self.__engine = create_async_engine(
                url=self.__url,
                echo=self.__echo,
                echo_pool=self.__echo_pool,
                max_overflow=self.__max_overflow,
                pool_size=self.__pool_size,
            )
            log.info("Created SQL database engine [%s].", id(self.__engine))
            self.__async_session_factory = async_sessionmaker(
                bind=self.__engine,
                autoflush=False,
                autocommit=False,
                expire_on_commit=False,
            )
            log.info(
                "Created SQL database async session factory [%s].",
                id(self.__async_session_factory),
            )
        except SQLAlchemyError as e:
            log.error("Failed to initialize SQL database.", exc_info=True)
            raise SQLRepositoryException(e)

    @property
    def async_session_factory(self) -> Callable[[], AsyncSession]:
        return self.__async_session_factory

    async def shutdown(self: Self) -> None:
        """Dispose of the database engine and release resources."""
        if self.__engine:
            await self.__engine.dispose()
            log.info("Disposing database engine.")
