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
        self._settings = settings
        self._url: str = self._settings.sql_db.url
        self._echo: bool = self._settings.sql_db.ECHO
        self._echo_pool: bool = self._settings.sql_db.ECHO_POOL
        self._pool_size: int = self._settings.sql_db.POOL_SIZE
        self._max_overflow: int = self._settings.sql_db.MAX_OVERFLOW

        self._engine: Optional[AsyncEngine]
        self._async_session_factory: Optional[async_sessionmaker[AsyncSession]]

    def startup(self: Self) -> None:
        """Initialize the database engine and session factory."""
        try:
            self._engine = create_async_engine(
                url=self._url,
                echo=self._echo,
                echo_pool=self._echo_pool,
                max_overflow=self._max_overflow,
                pool_size=self._pool_size,
            )
            log.info("Created SQL database engine [%s].", id(self._engine))
            self._async_session_factory = async_sessionmaker(
                bind=self._engine,
                autoflush=False,
                autocommit=False,
                expire_on_commit=False,
            )
            log.info(
                "Created SQL database async session factory [%s].",
                id(self._async_session_factory),
            )
        except SQLAlchemyError as e:
            log.error("Failed to initialize SQL database.", exc_info=True)
            raise SQLRepositoryException(e)

    @property
    def async_session_factory(self) -> Callable[[], AsyncSession]:
        return self._async_session_factory

    async def shutdown(self: Self) -> None:
        """Dispose of the database engine and release resources."""
        if self._engine:
            await self._engine.dispose()
            log.info("Disposing database engine.")
