"""
Module for users use case description.
"""

from abc import abstractmethod
from typing import Any, Dict, Protocol, Self

from src.app.schemas.users import SInfoUser
from src.app.services import UsersManagementServiceProtocol
from src.core.schemas import SAddInfoUser


class UsersManagementUseCaseProtocol(Protocol):

    UsersService: UsersManagementServiceProtocol

    @abstractmethod
    async def get_user_by_id(
        self: Self,
        user_id: int,
    ) -> SInfoUser:
        """Get information about the user.

        Args:
            user_id (int): argument to search for user data

        Returns:
            SInfoUser: user model.
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

    @abstractmethod
    async def get_list_users_by_id(
        self: Self,
        users_id: list[int],
    ) -> list[SInfoUser]:
        """Get information about the users.

        Args:
            user_id (list[int]): arguments to search for users data

        Returns:
            SInfoUser: list of users data.
        """
        ...

    @abstractmethod
    async def create_user(
        self: Self,
        data: SAddInfoUser,
    ) -> SInfoUser:
        """Add a new user.

        Args:
            **data (SAddInfoUser): data to be user create.

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
            **data (Dict[str, Any]): Data set to be updated.

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
