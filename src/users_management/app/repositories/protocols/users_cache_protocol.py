"""
Module describing the interface for interacting with the cache repository.
"""

from abc import abstractmethod
from typing import Any, Dict, List, Optional, Protocol, Self

from users_management.app.schemas.users import SInfoUser


class UsersCacheRepositoryProtocol(Protocol):
    @abstractmethod
    async def add_user(self: Self, key: Any, data: Dict[str, Any]) -> None:
        """Add user information to the cache.
        Args:
            key (Any): the key is the user id.
            data (Dict[str, Any]): user information.
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
    async def get_user(self: Self, key: Any) -> Dict[str, Any]:
        """Get user information from the cache.

        Args:
            key (Any): the key is the user id.

        Returns:
            Dict[str, Any]: user information.
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
    async def get_list_users(self, keys: List[Any]) -> Optional[List[Dict]]:
        """Get list user data from the cache

        Args:
            keys (List[Any]): list of user ID.

        Returns:
            Optional[List[Dict]]: user data list.
        """
