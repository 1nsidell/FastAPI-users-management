"""
A protocol describing the methods and attributes of a repository, 
that must be defined for the application to work
"""

import logging
from abc import abstractmethod
from typing import Any, Protocol, Self

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.exceptions import UserNotFoundException
from src.app.repositories.exceptions_handler import handle_repository_exceptions
from src.app.schemas.users import SInfoUser
from src.core.schemas import SAddInfoUser
from src.app.models import InfoUser, Role


log = logging.getLogger("repositories")


class RepositoryProtocol(Protocol):

    @abstractmethod
    async def get_user(
        self: Self,
        session: AsyncSession,
        user_id: int,
    ) -> SInfoUser:
        """Get information about the user.

        Args:
            session (AsyncSession): transaction session.
            user_id (int): argument to search for user data

        Returns:
            SUser: user model.
        """
        ...

    @abstractmethod
    async def add_user(
        self: Self,
        session: AsyncSession,
        **data: SAddInfoUser,
    ) -> None:
        """Add a new user.

        Args:
            session (AsyncSession): transaction session.
            **data (SAddInfoUser): data to be added.
        """
        ...

    @abstractmethod
    async def update_user(
        self: Self,
        session: AsyncSession,
        user_id: int,
        **data: Any,
    ) -> None:
        """Update user information by user ID.

        Args:
            session (AsyncSession): transaction session.
            user_id (int): user id.
            **data (Any): Data set to be updated.
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


class RepositoryImpl(RepositoryProtocol):
    USER_INFO_MODEL = InfoUser
    ROLE_MODEL = Role

    @handle_repository_exceptions
    async def get_user(
        self: Self,
        session: AsyncSession,
        user_id: int,
    ) -> SInfoUser:
        log.info("Request user information with ID: %s.", user_id)
        stmt = (
            select(
                self.USER_INFO_MODEL.user_id,
                self.USER_INFO_MODEL.nickname,
                self.USER_INFO_MODEL.is_active,
                self.USER_INFO_MODEL.is_verified,
                self.USER_INFO_MODEL.avatar,
                self.ROLE_MODEL.role,
            )
            .where(self.USER_INFO_MODEL.user_id == user_id)
            .join(
                self.ROLE_MODEL,
                self.ROLE_MODEL.id == self.USER_INFO_MODEL.role_id,
            )
        )
        result = await session.execute(stmt)
        user = result.mappings().one_or_none()
        if not user:
            log.info("User not found with ID: %s.", user_id)
            raise UserNotFoundException()
        log.info("User information found with ID: %s.", user_id)
        return SInfoUser.model_validate(user, from_attributes=True)

    @handle_repository_exceptions
    async def add_user(
        self: Self,
        session: AsyncSession,
        data: SAddInfoUser,
    ) -> None:
        log.info("Adding new user.")
        stmt = (
            insert(self.USER_INFO_MODEL)
            .values(data.model_dump())
            .execution_options(synchronize_session="fetch")
        )
        await session.execute(stmt)
        log.info("User successfully added with ID: %s.", data.user_id)

    @handle_repository_exceptions
    async def update_user(
        self: Self,
        session: AsyncSession,
        user_id: int,
        **data: Any,
    ) -> None:
        log.info("User data update: %s.", user_id)
        stmt = (
            update(self.USER_INFO_MODEL)
            .where(self.USER_INFO_MODEL.user_id == user_id)
            .values(**data)
            .execution_options(synchronize_session="fetch")
        )
        await session.execute(stmt)
        log.info("Successful update user with ID: %s.", user_id)

    @handle_repository_exceptions
    async def delete_user(
        self: Self,
        session: AsyncSession,
        user_id: int,
    ) -> None:
        log.info("user deletion with ID: %s.", user_id)
        stmt = (
            delete(self.USER_INFO_MODEL)
            .where(self.USER_INFO_MODEL.user_id == user_id)
            .execution_options(synchronize_session="fetch")
        )
        await session.execute(stmt)
        log.info("Successful deletion user with ID: %s.", user_id)
