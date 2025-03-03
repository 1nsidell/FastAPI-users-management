"""
Service protocol responsible for user management.
"""

from abc import abstractmethod
from typing import Any, Dict, Protocol, Self

from src.app.schemas.users import SInfoUser
from src.core.db import SQLRepositoryUOWProtocol
from src.core.schemas import SAddInfoUser
from src.app.repositories import (
    UsersSQLRepositoryProtocol,
    CacheRepositoryProtocol,
)


class UsersManagementServiceProtocol(Protocol):

    users_sql_repository: UsersSQLRepositoryProtocol
    redis_users_cache: CacheRepositoryProtocol
    uow: SQLRepositoryUOWProtocol

    @abstractmethod
    async def get_user_by_id(
        self: Self,
        data: Any,
    ) -> SInfoUser:
        """Get information about the user.

        Args:
            user_id (int): argument to search for user data

        Returns:
            SUser: user model.
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
