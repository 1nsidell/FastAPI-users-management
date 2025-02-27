import logging
from typing import Optional, Callable

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    AsyncSessionTransaction,
    async_sessionmaker,
    create_async_engine,
)

from app.exceptions import TransactionException
from src.settings import settings

log = logging.getLogger("repositories")


class DatabaseHelper:
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


class RepositoryUOW:
    def __init__(self, db_helper: DatabaseHelper):
        self.__session_factory: Callable[[], AsyncSession] = (
            db_helper.async_session_factory
        )
        self.session: Optional[AsyncSession] = None
        self.transaction: Optional[AsyncSessionTransaction] = None

    async def __aenter__(self) -> AsyncSession:
        self.session = self.__session_factory()
        self.transaction = await self.session.begin()
        log.info(f"Session [{id(self.session)}] started")
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        try:
            if self.session is None:
                raise TransactionException("Session not initialized")
            if exc_type is not None:
                log.warning(
                    f"Rolling back transaction for session [{id(self.session)}]"
                )
                await self.transaction.rollback()
                log.debug(f"Rollback complete for session [{id(self.session)}]")
            else:
                try:
                    await self.transaction.commit()
                    log.info(
                        f"Commit successful for session [{id(self.session)}]"
                    )
                except Exception as commit_error:
                    log.error(f"Commit failed: {commit_error}")
                    await self.session.rollback()
                    raise TransactionException(commit_error)
        finally:
            log.info(f"Session [{id(self.session)}] is closed.")
            await self.session.close()


class UOWFactory:
    def __init__(self, db_helper: DatabaseHelper):
        self.db_helper = db_helper

    def __call__(self) -> RepositoryUOW:
        return RepositoryUOW(self.db_helper)
