"""Module related to connection to repositories."""

import logging
from typing import Callable, Optional, Self


import redis.asyncio as redis
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    AsyncSessionTransaction,
    async_sessionmaker,
    create_async_engine,
)

from src.app.exceptions import TransactionException
from src.settings import Settings

log = logging.getLogger("app")


class SQLDatabaseHelper:
    """Class helping to async connect to SQL database."""

    def __init__(
        self,
        url: str,
        echo: bool,
        echo_pool: bool,
        pool_size: int,
        max_overflow: int,
    ):
        self.url = url
        self.echo = echo
        self.echo_pool = echo_pool
        self.pool_size = pool_size
        self.max_overflow = max_overflow

        self.engine: Optional[AsyncEngine] = None
        self.async_session_factory: Optional[async_sessionmaker[AsyncSession]]

    def startup(self: Self) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url=self.url,
            echo=self.echo,
            echo_pool=self.echo_pool,
            max_overflow=self.max_overflow,
            pool_size=self.pool_size,
        )
        log.info("Created Postgres DB engine [%s].", id(self.engine))
        self.async_session_factory: async_sessionmaker[AsyncSession] = (
            async_sessionmaker(
                bind=self.engine,
                autoflush=False,
                autocommit=False,
                expire_on_commit=False,
            )
        )
        log.info(
            "Created Postgres DB async session factory [%s].",
            id(self.async_session_factory),
        )

    async def shutdown(self: Self) -> None:
        if self.engine:
            await self.engine.dispose()
            log.info("Releasing database resources.")


class SQLRepositoryUOW:
    """Unit of Work for async SQL transactions."""

    def __init__(self, session_factory: Callable[[], AsyncSession]):
        """Initialize UoW with a session factory.

        Args:
            session_factory: Callable that returns an AsyncSession instance.
        """
        self.__session_factory = session_factory
        self.__session: Optional[AsyncSession] = None
        self.__transaction: Optional[AsyncSessionTransaction] = None

    async def __aenter__(self) -> AsyncSession:
        self.__session = self.__session_factory()
        self.__transaction = await self.__session.begin()
        log.info("Session [%s] started.", id(self.__session))
        return self.__session

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        try:
            if exc_type is not None:
                log.error(
                    "Exception occurred in session [%s]: %s: %s.",
                    id(self.__session),
                    exc_type.__name__,
                    exc_val,
                )
                log.warning(
                    "Rolling back transaction for session [%s].",
                    id(self.__session),
                )
                try:
                    await self.__transaction.rollback()
                except Exception:
                    log.exception("Rollback failed.")
            else:
                try:
                    await self.__transaction.commit()
                    log.debug(
                        "Commit successful for session [%s].",
                        id(self.__session),
                    )
                except Exception as e:
                    log.exception("Commit failed.")
                    try:
                        await self.__transaction.rollback()
                    except Exception:
                        log.exception("Rollback after commit failure failed.")
                    raise TransactionException(e) from e
        finally:
            try:
                await self.__session.close()
                log.info("Session [] closed.", id(self.__session))
            except Exception:
                log.exception(
                    "Failed to close session [%s].", id(self.__session)
                )
            self.__session = None
            self.__transaction = None


class RedisConnectionManager:
    """A class for getting an instance of the redis pool."""

    def __init__(self: Self, settings: Settings):
        self.settings = settings
        self.pool: redis.ConnectionPool
        self.redis: redis.Redis

    def startup(self: Self) -> None:
        self.pool = redis.ConnectionPool.from_url(
            self.settings.redis.users_cache_url,
            decode_responses=True,
        )
        log.info("Redis conn pool [%s] is created.", id(self.pool))
        self.redis = redis.Redis(connection_pool=self.pool)
        log.info("Redis instance [%s] is created.", id(self.redis))

    async def shutdown(self: Self) -> None:
        if self.redis:
            await self.redis.aclose()
            log.info("Redis instance [%s] is close.", id(self.redis))
        if self.pool:
            await self.pool.disconnect()
            log.info("Redis conn pool [%s] is close.", id(self.pool))
