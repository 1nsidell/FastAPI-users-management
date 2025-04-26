from abc import abstractmethod
from types import TracebackType
from typing import Optional, Protocol, Self, Type

from users_management.gateways.repositories import UsersRepositoryProtocol


class RepositoryManagerProtocol(Protocol):
    """Protocol for Unit of Work pattern implementation."""

    users_repository: UsersRepositoryProtocol

    @abstractmethod
    async def __aenter__(self: Self) -> Self:
        """Start transaction and return session."""
        ...

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Commit or rollback transaction."""
        ...
