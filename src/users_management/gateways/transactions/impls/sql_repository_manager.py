import logging
from types import TracebackType
from typing import (
    Callable,
    Optional,
    Self,
    Type,
)

from sqlalchemy.ext.asyncio import AsyncSession

from users_management.app.exceptions import (
    TransactionException,
)
from users_management.gateways.repositories.protocols.users_protocol import (
    UsersRepositoryProtocol,
)
from users_management.gateways.transactions import RepositoryManagerProtocol


log = logging.getLogger(__name__)


class SQLTransactionsManagerImpl(RepositoryManagerProtocol):
    """Unit of Work for async SQL transactions."""

    def __init__(
        self: Self,
        async_session_factory: Callable[[], AsyncSession],
        users_repo_factory: Callable[[AsyncSession], UsersRepositoryProtocol],
    ):
        """Initialize UoW with a session factory."""

        self._async_session_factory = async_session_factory
        self._users_repo_factory = users_repo_factory
        self._session: Optional[AsyncSession] = None
        self.users_repository: Optional[UsersRepositoryProtocol] = None

    async def __aenter__(self) -> Self:
        self._session = self._async_session_factory()
        await self._session.begin()
        self.users_repository = self._users_repo_factory(self._session)
        log.info("Session [%s] started.", id(self._session))
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        try:
            if exc_type is not None:
                log.error(
                    "Exception in session [%s]: %s: %s",
                    id(self._session),
                    exc_type.__name__,
                    exc_val,
                )
                await self._rollback()
            else:
                await self._commit()
        finally:
            await self._close_session()

    async def _rollback(self) -> None:
        if self._session:
            try:
                await self._session.rollback()
                log.warning(
                    "Rolled back transaction for session [%s]",
                    id(self._session),
                )
            except Exception:
                log.exception(
                    "Rollback failed for session [%s]", id(self._session)
                )

    async def _commit(self) -> None:
        if self._session:
            try:
                await self._session.commit()
                log.debug(
                    "Committed transaction for session [%s]", id(self._session)
                )
            except Exception as e:
                log.exception(
                    "Commit failed for session [%s]", id(self._session)
                )
                await self._rollback()
                raise TransactionException(str(e)) from e

    async def _close_session(self) -> None:
        if self._session:
            try:
                await self._session.close()
                log.info("Closed session [%s]", id(self._session))
            except Exception:
                log.exception("Failed to close session [%s]", id(self._session))
