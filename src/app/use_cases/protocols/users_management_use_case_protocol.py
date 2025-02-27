from abc import abstractmethod
from typing import Any, Protocol, Self

from src.app.schemas.users import SInfoUser
from src.app.services import UsersServiceProtocol
from src.core.schemas import SAddInfoUser


class UsersUseCaseProtocol(Protocol):

    UsersService: UsersServiceProtocol

    @abstractmethod
    async def get_user(
        self: Self,
        user_id: int,
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
            **data (SAddInfoUser): data to be user create.
        """
        ...

    @abstractmethod
    async def update_user(
        self: Self,
        user_id: int,
        data: Any,
    ) -> None:
        """Update user information by user ID.

        Args:
            user_id (int): user id.
            **data (Any): Data set to be updated.
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
