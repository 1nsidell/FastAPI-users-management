"""Module related to connection to repositories."""

import logging
from typing import Callable, Optional, Self

import redis.asyncio as redis
from redis.exceptions import RedisError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    AsyncSessionTransaction,
    async_sessionmaker,
    create_async_engine,
)

from users_management.app.exceptions import (
    RedisCacheDBException,
    SQLRepositoryException,
    TransactionException,
)
from users_management.settings import Settings

log = logging.getLogger(__name__)


class SQLDatabaseHelper:
    """Class helping to async connect to SQL database."""

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


class SQLRepositoryUOW:
    """Unit of Work for async SQL transactions."""

    def __init__(self, session_factory: Callable[[], AsyncSession]):
        """Initialize UoW with a session factory.

        Args:
            session_factory: Callable that returns an AsyncSession instance.
        """
        self.__session_factory = session_factory
        self.__session: Optional[AsyncSession]
        self.__transaction: Optional[AsyncSessionTransaction]

    async def __aenter__(self) -> AsyncSession:
        self.__session = self.__session_factory()
        self.__transaction = await self.__session.begin()
        log.info("Session [%s] started.", id(self.__session))
        return self.__session

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        session_id = id(self.__session)
        try:
            if exc_type is not None:
                log.error(
                    "Exception in session [%s]: %s: %s",
                    session_id,
                    exc_type.__name__,
                    exc_val,
                )
                await self._rollback()
            else:
                await self._commit()
        finally:
            await self._close_session()

    async def _rollback(self):
        try:
            await self.__transaction.rollback()
            log.warning(
                "Rolled back transaction for session [%s]", id(self.__session)
            )
        except Exception:
            log.exception(
                "Rollback failed for session [%s]", id(self.__session)
            )

    async def _commit(self):
        try:
            await self.__transaction.commit()
            log.debug(
                "Committed transaction for session [%s]", id(self.__session)
            )
        except Exception as e:
            log.exception("Commit failed for session [%s]", id(self.__session))
            await self._rollback()
            raise TransactionException(e) from e

    async def _close_session(self):
        try:
            await self.__session.close()
            log.info("Closed session [%s]", id(self.__session))
        except Exception:
            log.exception("Failed to close session [%s]", id(self.__session))
        finally:
            self.__session = None
            self.__transaction = None


class RedisConnectionManager:
    """A class for getting an instance of the redis pool."""

    def __init__(self: Self, settings: Settings):
        self.__settings = settings
        self.__url: str = self.__settings.redis.users_cache_url
        self.__pool: redis.ConnectionPool
        self.__redis: redis.Redis

    def startup(self: Self) -> None:
        """Redis pool creation."""
        try:
            self.__pool = redis.ConnectionPool.from_url(
                self.__url,
                decode_responses=True,
            )
            log.info("Redis conn pool [%s] is created.", id(self.__pool))
            self.__redis = redis.Redis(connection_pool=self.__pool)
            log.info("Redis instance [%s] is created.", id(self.__redis))
        except RedisError as e:
            log.error("Failed to initialize redis.", exc_info=True)
            raise RedisCacheDBException(e)

    @property
    def redis(self) -> redis.Redis:
        return self.__redis

    async def shutdown(self: Self) -> None:
        """Closing a connection to Redis."""
        if self.__redis:
            await self.__redis.aclose()
            log.info("Redis instance [%s] is closed.", id(self.__redis))
        if self.__pool:
            await self.__pool.disconnect()
            log.info("Redis conn pool [%s] is closed.", id(self.__pool))
