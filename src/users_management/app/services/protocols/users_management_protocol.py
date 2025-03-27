"""
Service protocol responsible for user management.
"""

from abc import abstractmethod
from typing import Any, Dict, Protocol, Self

from users_management.app.repositories import (
    UsersCacheRepositoryProtocol,
    UsersSQLRepositoryProtocol,
)
from users_management.app.schemas.users import SInfoUser
from users_management.core import SQLRepositoryUOW
from users_management.core.schemas import SAddInfoUser


class UsersManagementServiceProtocol(Protocol):
    users_sql_repository: UsersSQLRepositoryProtocol
    redis_users_cache: UsersCacheRepositoryProtocol
    uow: SQLRepositoryUOW

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
        data: SAddInfoUser,
    ) -> SInfoUser:
        """Add a new user.

        Args:
            data (SAddInfoUser): data to be user create.

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
