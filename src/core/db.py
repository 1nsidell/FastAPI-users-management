"""Module somehow related to connection to repositories."""

import logging
from typing import Callable, Optional, Protocol, Self
from abc import abstractmethod

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

log = logging.getLogger("repositories")


class DatabaseHelperProtocol(Protocol):
    """Class helping to async connect to SQL database."""

    url: str
    echo: bool
    echo_pool: bool
    pool_size: int
    max_overflow: int

    engine: Optional[AsyncEngine]
    async_session_factory: Optional[async_sessionmaker[AsyncSession]]

    @abstractmethod
    async def startup(self: Self) -> None: ...

    @abstractmethod
    async def shutdown(self: Self) -> None: ...


class DatabaseHelperImpl(DatabaseHelperProtocol):
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

    async def startup(self: Self):
        self.engine: AsyncEngine = create_async_engine(
            url=self.url,
            echo=self.echo,
            echo_pool=self.echo_pool,
            max_overflow=self.max_overflow,
            pool_size=self.pool_size,
        )
        log.info(f"Created Postgres DB engine [{id(self.engine)}].")
        self.async_session_factory: async_sessionmaker[AsyncSession] = (
            async_sessionmaker(
                bind=self.engine,
                autoflush=False,
                autocommit=False,
                expire_on_commit=False,
            )
        )
        log.info(
            f"Created Postgres DB async session factory [{id(self.async_session_factory)}]."
        )

    async def shutdown(self: Self) -> None:
        if self.engine:
            await self.engine.dispose()
            log.info("Releasing database resources.")


class SQLRepositoryUOWProtocol(Protocol):
    """UOW for working with SQL database transactions."""

    session: Optional[AsyncSession]
    transaction: Optional[AsyncSessionTransaction]

    async def __aenter__(self: Self) -> AsyncSession: ...

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None: ...


class SQLRepositoryUOWImpl(SQLRepositoryUOWProtocol):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.__session_factory: Callable[[], AsyncSession] = session_factory
        self.__session: Optional[AsyncSession] = None
        self.__transaction: Optional[AsyncSessionTransaction] = None

    async def __aenter__(self) -> AsyncSession:
        self.__session = self.__session_factory()
        self.__transaction = await self.__session.begin()
        log.info(f"Session [{id(self.__session)}] started.")
        return self.__session

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        try:
            if exc_type is not None:
                log.error(
                    f"Exception occurred in session [{id(self.__session)}]: {exc_type.__name__}: {exc_val}"
                )
                log.warning(
                    f"Rolling back transaction for session [{id(self.__session)}]."
                )
                try:
                    await self.__transaction.rollback()
                except Exception:
                    log.exception("Rollback failed.")
            else:
                try:
                    await self.__transaction.commit()
                    log.info(
                        f"Commit successful for session [{id(self.__session)}]."
                    )
                except Exception as e:
                    log.exception("Commit failed.")
                    try:
                        await self.__transaction.rollback()
                    except Exception:
                        log.exception("Rollback after commit failure failed.")
                    raise TransactionException("Commit failed") from e
        finally:
            try:
                await self.__session.close()
                log.info(f"Session [{id(self.__session)}] closed.")
            except Exception:
                log.exception(
                    f"Failed to close session [{id(self.__session)}]."
                )
            self.__session = None
            self.__transaction = None


class RedisPoolManagerImpl:
    def __init__(self: Self, settings: Settings):
        self.settings: Settings = settings
        self.pool: Optional[redis.ConnectionPool] = None
        self.redis: Optional[redis.Redis] = None

    async def startup(self: Self):
        self.pool = redis.ConnectionPool.from_url(
            self.settings.redis.users_cache_url,
            decode_responses=True,
        )
        log.info(f"Redis conn pool [{id(self.pool)}] is created.")
        self.redis = redis.Redis(connection_pool=self.pool)
        log.info(f"Redis instance [{id(self.redis)}] is created.")

    async def shutdown(self: Self):
        if self.redis:
            await self.redis.aclose()
            log.info(f"Redis instance [{id(self.redis)}] is close.")
        if self.pool:
            await self.pool.disconnect()
            log.info(f"Redis conn pool [{id(self.pool)}] is close.")
