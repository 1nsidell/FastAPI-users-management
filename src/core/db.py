import logging
from typing import Callable, Optional

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    AsyncSessionTransaction,
    async_sessionmaker,
    create_async_engine,
)

from src.settings import settings

log = logging.getLogger("repositories")


class DatabaseHelper:
    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: bool = False,
        max_overflow: int = 10,
        pool_size: int = 50,
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
        self.transaction: Optional[AsyncSessionTransaction] = None
        self.session: Optional[AsyncSession] = None

    async def __aenter__(self) -> AsyncSession:
        self.session = self.__session_factory()
        self.transaction = await self.session.begin()
        log.info("New database session and transaction started.")
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        try:
            if exc_type is not None:
                log.warning("Error occurred. Rolling back transaction.")
                await self.transaction.rollback()
                raise
            else:
                await self.transaction.commit()
                log.info("Transaction committed successfully.")
        finally:
            await self.session.close()
            log.info("Session closed.")
