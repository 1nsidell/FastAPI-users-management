from abc import abstractmethod
from typing import Callable, Protocol


class SQLDatabaseHelperProtocol(Protocol):
    """Protocol defining the interface for SQL database helper classes."""

    @abstractmethod
    def startup(self) -> None:
        """Initialize the database engine and session factory."""
        ...

    @abstractmethod
    def async_session_factory(self) -> Callable:
        """Factory for get async database sessions."""
        ...

    @abstractmethod
    async def shutdown(self) -> None:
        """Dispose of the database engine and release resources."""
        ...
