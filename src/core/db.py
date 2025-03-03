"""Module somehow related to connection to repositories."""

import logging
from typing import Callable, Optional, Protocol, Self

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    AsyncSessionTransaction,
    async_sessionmaker,
    create_async_engine,
)
import redis.asyncio as redis

from src.app.exceptions import TransactionException
from src.settings import settings, Settings

log = logging.getLogger("repositories")


class DatabaseHelperProtocol(Protocol):
    url: str
    echo: bool
    echo_pool: bool
    pool_size: int
    max_overflow: int

    engine: AsyncEngine
    async_session_factory: async_sessionmaker[AsyncSession]

    async def dispose(self: Self) -> None: ...


class DatabaseHelperImpl(DatabaseHelperProtocol):
    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ):
        log.info("Creating DB engine: %s.", settings.db.NAME)
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            max_overflow=max_overflow,
            pool_size=pool_size,
        )
        self.async_session_factory: async_sessionmaker[AsyncSession] = (
            async_sessionmaker(
                bind=self.engine,
                autoflush=False,
                autocommit=False,
                expire_on_commit=False,
            )
        )

    async def dispose(self):
        log.info("Releasing database resources.")
        await self.engine.dispose()


class SQLRepositoryUOWProtocol(Protocol):
    session: Optional[AsyncSession]
    transaction: Optional[AsyncSessionTransaction]

    async def __aenter__(self: Self) -> AsyncSession: ...

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None: ...


class SQLRepositoryUOWImpl(SQLRepositoryUOWProtocol):
    def __init__(self, session_factory: AsyncSession):
        self.__session_factory: Callable[[], AsyncSession] = session_factory
        self.session: Optional[AsyncSession] = None
        self.transaction: Optional[AsyncSessionTransaction] = None

    async def __aenter__(self) -> AsyncSession:
        self.session = self.__session_factory()
        self.transaction = await self.session.begin()
        log.info(f"Session [{id(self.session)}] started.")
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        try:
            if self.session is None:
                raise TransactionException("Session not initialized.")
            if exc_type is not None:
                log.warning(
                    f"Rolling back transaction for session [{id(self.session)}]."
                )
                await self.transaction.rollback()
                log.debug(
                    f"Rollback complete for session [{id(self.session)}]."
                )
            else:
                try:
                    await self.transaction.commit()
                    log.info(
                        f"Commit successful for session [{id(self.session)}]."
                    )
                except Exception as commit_error:
                    log.exception(f"Commit failed.")
                    await self.session.rollback()
                    raise TransactionException()
        finally:
            log.info(f"Session [{id(self.session)}] is closed.")
            await self.session.close()


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
