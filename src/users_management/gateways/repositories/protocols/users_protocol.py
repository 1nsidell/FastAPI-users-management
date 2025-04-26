"""
A protocol describing the methods and attributes of a repository,
that must be defined for the application to work.
"""

from abc import abstractmethod
from typing import Any, Dict, Protocol, Self

from users_management.app.schemas.requests import CreateUserRequest
from users_management.app.schemas.users import SInfoUser


class UsersRepositoryProtocol(Protocol):
    @abstractmethod
    async def get_user(
        self: Self,
        **filter_by: Any,
    ) -> SInfoUser:
        """Get information about the user.

        Args:
            **filter_by (Any): argument to search for user data.

        Returns:
            SInfoUser: user data.
        """
        ...

    async def get_users_list(
        self: Self,
        users_id: list[int],
    ) -> list[SInfoUser]:
        """Getting information about the list of user.

        Args:
            users_id (list[int]): list of user.

        Returns:
            list[SInfoUser]: list of requested user data.
        """
        ...

    @abstractmethod
    async def create_user(
        self: Self,
        data: CreateUserRequest,
    ) -> SInfoUser:
        """Add a new user.

        Args:
            data (CreateUserRequest): data to be added.

        Returns:
            SInfoUser: user data.
        """
        ...

    @abstractmethod
    async def update_user(
        self: Self,
        user_id: int,
        data: Dict[str, Any],
    ) -> SInfoUser:
        """Update user information by user ID.

        Args:
            user_id (int): user id.
            data (Dict[str, Any]): Data set to be updated.

        Returns:
            SInfoUser: user data.
        """
        ...

    @abstractmethod
    async def delete_user(
        self: Self,
        user_id: int,
    ) -> None:
        """Deleting a user account by ID.

        Args:
            user_id (int): user id.
        """
        ...
