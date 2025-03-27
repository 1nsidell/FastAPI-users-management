"""
Module describing the interface for interacting with the cache repository.
"""

from abc import abstractmethod
from typing import Any, List, Optional, Protocol, Self

from users_management.app.schemas.users import SInfoUser


class UsersCacheRepositoryProtocol(Protocol):
    @abstractmethod
    async def add_user(self: Self, key: Any, data: SInfoUser) -> None:
        """Add user information to the cache.
        Args:
            key (Any): the key is the user id.
            data (SInfoUser): user information.
        """
        ...

    @abstractmethod
    async def delete_user(self: Self, key: Any) -> None:
        """Delete user information from the cache.

        Args:
            key (Any): the key is the user id.
        """
        ...

    @abstractmethod
    async def get_user(self: Self, key: Any) -> Optional[SInfoUser]:
        """Get user information from the cache.

        Args:
            key (Any): the key is the user id.

        Returns:
            Optional[SInfoUser]: user information.
        """
        ...

    @abstractmethod
    async def add_list_users(
        self,
        data_list: List[SInfoUser],
    ) -> None:
        """Cache the user list.

        Args:
            data_list (List[SInfoUser]): list of user data.
        """
        ...

    @abstractmethod
    async def get_list_users(
        self, keys: List[Any]
    ) -> Optional[List[SInfoUser]]:
        """Get list user data from the cache

        Args:
            keys (List[Any]): list of user ID.

        Returns:
            Optional[List[SInfoUser]]: user data list.
        """
