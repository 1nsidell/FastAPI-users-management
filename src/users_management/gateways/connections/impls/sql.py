"""Module related to connection to repositories."""

import logging
from typing import Optional, Self

from sqlalchemy import URL
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
from users_management.core.settings import SQLDatabaseConfig
from users_management.gateways.connections import (
    GatewayConnectionProtocol,
)


log = logging.getLogger(__name__)


class SQLDatabaseManagerImpl(
    GatewayConnectionProtocol[async_sessionmaker[AsyncSession]]
):
    """Class helping to async connect to SQL database.

    Args:
        config (SQLDatabaseConfig): SQL config.
    """

    def __init__(self: Self, config: SQLDatabaseConfig):
        self._config = config
        self._url: URL = self._config.url
        self._echo: bool = self._config.ECHO
        self._echo_pool: bool = self._config.ECHO_POOL
        self._pool_size: int = self._config.POOL_SIZE
        self._max_overflow: int = self._config.MAX_OVERFLOW

        self._engine: Optional[AsyncEngine] = None
        self._session_maker: Optional[async_sessionmaker[AsyncSession]] = None

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
            raise SQLRepositoryException(str(e))

    def get_connection(self) -> async_sessionmaker[AsyncSession]:
        return self._async_session_factory

    async def shutdown(self: Self) -> None:
        """Dispose of the database engine and release resources."""
        if self._engine:
            await self._engine.dispose()
            log.info("Disposing database engine.")
