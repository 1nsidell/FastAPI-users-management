"""
A protocol describing the methods and attributes of a repository,
that must be defined for the application to work.
"""

from abc import abstractmethod
from typing import Any, Dict, Protocol, Self

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.schemas.users import SInfoUser
from src.core.schemas import SAddInfoUser


class UsersSQLRepositoryProtocol(Protocol):

    @abstractmethod
    async def get_user(
        self: Self,
        session: AsyncSession,
        **filter_by: Any,
    ) -> SInfoUser:
        """Get information about the user.

        Args:
            session (AsyncSession): transaction session.
            **filter_by (Any): argument to search for user data

        Returns:
            SUser: user model.
        """
        ...

    @abstractmethod
    async def add_user(
        self: Self,
        session: AsyncSession,
        data: SAddInfoUser,
    ) -> None:
        """Add a new user.

        Args:
            session (AsyncSession): transaction session.
            data (SAddInfoUser): data to be added.
        """
        ...

    @abstractmethod
    async def update_user(
        self: Self,
        session: AsyncSession,
        user_id: int,
        data: Dict[str, Any],
    ) -> None:
        """Update user information by user ID.

        Args:
            session (AsyncSession): transaction session.
            user_id (int): user id.
            data (Dict[str, Any]): Data set to be updated.
        """
        ...

    @abstractmethod
    async def delete_user(
        self: Self,
        session: AsyncSession,
        user_id: int,
    ) -> None:
        """Deleting a user account by ID.

        Args:
            session (AsyncSession): transaction session.
            user_id (int): user id.
        """
        ...
