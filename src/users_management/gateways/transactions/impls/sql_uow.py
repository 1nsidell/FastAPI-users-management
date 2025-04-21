import logging
from typing import Callable, Optional, Self

from sqlalchemy.ext.asyncio import AsyncSession

from users_management.app.exceptions import (
    TransactionException,
)
from users_management.gateways.transactions import UnitOfWorkProtocol


log = logging.getLogger(__name__)


class SQLRepositoryUOW(UnitOfWorkProtocol):
    """Unit of Work for async SQL transactions."""

    def __init__(self: Self, session_factory: Callable[[], AsyncSession]):
        """Initialize UoW with a session factory.

        Args:
            session_factory: Callable that returns an AsyncSession instance.
        """
        self._session_factory = session_factory
        self._session: Optional[AsyncSession]

    async def __aenter__(self) -> AsyncSession:
        self._session = self._session_factory()
        log.info("Session [%s] started.", id(self._session))
        return self._session

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        session_id = id(self._session)
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
            await self._session.rollback()
            log.warning(
                "Rolled back transaction for session [%s]", id(self._session)
            )
        except Exception:
            log.exception("Rollback failed for session [%s]", id(self._session))

    async def _commit(self):
        try:
            await self._session.commit()
            log.debug(
                "Committed transaction for session [%s]", id(self._session)
            )
        except Exception as e:
            log.exception("Commit failed for session [%s]", id(self._session))
            await self._rollback()
            raise TransactionException(e) from e

    async def _close_session(self):
        try:
            await self._session.close()
            log.info("Closed session [%s]", id(self._session))
        except Exception:
            log.exception("Failed to close session [%s]", id(self._session))
        finally:
            self._session = None
