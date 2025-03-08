"""
Service protocol responsible for user management.
"""

from abc import abstractmethod
from typing import Any, Dict, Protocol, Self

from src.app.repositories import (
    CacheRepositoryProtocol,
    UsersSQLRepositoryProtocol,
)
from src.app.schemas.users import SInfoUser
from src.core.db import SQLRepositoryUOW
from src.core.schemas import SAddInfoUser


class UsersManagementServiceProtocol(Protocol):

    users_sql_repository: UsersSQLRepositoryProtocol
    redis_users_cache: CacheRepositoryProtocol
    uow: SQLRepositoryUOW

    @abstractmethod
    async def get_user_by_id(
        self: Self,
        user_id: int,
    ) -> SInfoUser:
        """Get information about the user.

        Args:
            user_id (int): ID to search for user data

        Returns:
            SInfoUser: user model.
        """
        ...

    @abstractmethod
    async def create_user(
        self: Self,
        data: SAddInfoUser,
    ) -> None:
        """Add a new user.

        Args:
            data (SAddInfoUser): data to be user create.
        """
        ...

    @abstractmethod
    async def update_user(
        self: Self,
        user_id: int,
        data: Dict[str, Any],
    ) -> None:
        """Update user information by user ID.

        Args:
            user_id (int): user id.
            data (Dict[str, Any]): Data set to be updated.
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
