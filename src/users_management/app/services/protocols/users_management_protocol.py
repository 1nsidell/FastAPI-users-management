"""
Service protocol responsible for user management.
"""

from abc import abstractmethod
from typing import Any, Dict, Protocol, Self

from users_management.app.schemas.requests import CreateUserRequest
from users_management.app.schemas.users import SInfoUser
from users_management.gateways.repositories import (
    UsersCacheRepositoryProtocol,
    UsersSQLRepositoryProtocol,
)
from users_management.gateways.transactions import UnitOfWorkProtocol


class UsersManagementServiceProtocol(Protocol):
    users_repository: UsersSQLRepositoryProtocol
    users_cache: UsersCacheRepositoryProtocol
    uow: UnitOfWorkProtocol

    @abstractmethod
    async def get_user_by_id(
        self: Self,
        user_id: int,
    ) -> SInfoUser:
        """Get data about the user.

        Args:
            user_id (int): ID to search for user data

        Returns:
            SInfoUser: user data.
        """
        ...

    async def find_user_by_nickname(
        self: Self,
        nickname: str,
    ) -> None:
        """Nickname check.

        Args:
            nickname (str): user nickname.
        """
        ...

    async def get_users_list(
        self: Self,
        users_id: list[int],
    ) -> list[SInfoUser]:
        """Get list user data.

        Args:
            users_id (list[int]): list of user ID.

        Returns:
            list[SInfoUser]: list of user data.
        """
        ...

    @abstractmethod
    async def create_user(
        self: Self,
        data: CreateUserRequest,
    ) -> SInfoUser:
        """Add a new user.

        Args:
            data (CreateUserRequest): data to be user create.

        Returns:
            SInfoUser: created user data.
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
            SInfoUser: updated user data.
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
