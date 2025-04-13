from abc import abstractmethod
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWorkProtocol(Protocol):
    """Protocol for Unit of Work pattern implementation."""

    @abstractmethod
    async def __aenter__(self) -> AsyncSession:
        """Start transaction and return session."""
        ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Commit or rollback transaction."""
        ...
