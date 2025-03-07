"""
A protocol describing the methods and attributes of a repository,
that must be defined for the application to work
"""

import logging
from typing import Any, Dict, Self

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models import InfoUser, Role
from src.app.repositories import (
    UsersSQLRepositoryProtocol,
    handle_sql_exceptions,
)
from src.app.schemas.users import SInfoUser
from src.core.schemas import SAddInfoUser

log = logging.getLogger("app")


class UsersSQLRepositoryImpl(UsersSQLRepositoryProtocol):
    USER_INFO_MODEL = InfoUser
    ROLE_MODEL = Role

    @handle_sql_exceptions
    async def get_user(
        self: Self,
        session: AsyncSession,
        **filter_by: Any,
    ) -> SInfoUser:
        log.info("Request user information with filter: %s.", filter_by)
        stmt = (
            select(
                self.USER_INFO_MODEL.user_id,
                self.USER_INFO_MODEL.nickname,
                self.USER_INFO_MODEL.is_active,
                self.USER_INFO_MODEL.is_verified,
                self.USER_INFO_MODEL.avatar,
                self.ROLE_MODEL.role,
            )
            .filter_by(**filter_by)
            .join(
                self.ROLE_MODEL,
                self.ROLE_MODEL.role_id == self.USER_INFO_MODEL.role_id,
            )
        )
        result = await session.execute(stmt)
        user = result.mappings().one_or_none()
        if not user:
            log.info("User not found with filter: %s.", filter_by)
            return None
        log.info("User information found with filter: %s.", filter_by)
        return SInfoUser.model_validate(user, from_attributes=True)

    @handle_sql_exceptions
    async def add_user(
        self: Self,
        session: AsyncSession,
        data: SAddInfoUser,
    ) -> None:
        log.info(
            "Adding new user with ID: %s and nickname: %s.",
            data.user_id,
            data.nickname,
        )
        stmt = (
            insert(self.USER_INFO_MODEL)
            .values(data.model_dump())
            .execution_options(synchronize_session="fetch")
        )
        await session.execute(stmt)
        log.info(
            "User successfully added with ID: %s and nickname: %s.",
            data.user_id,
            data.nickname,
        )

    @handle_sql_exceptions
    async def update_user(
        self: Self,
        session: AsyncSession,
        user_id: int,
        data: Dict[str, Any],
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

    @handle_sql_exceptions
    async def delete_user(
        self: Self,
        session: AsyncSession,
        user_id: int,
    ) -> None:
        log.info("User deletion with ID: %s.", user_id)
        stmt = (
            delete(self.USER_INFO_MODEL)
            .where(self.USER_INFO_MODEL.user_id == user_id)
            .execution_options(synchronize_session="fetch")
        )
        await session.execute(stmt)
        log.info("Successful deletion user with ID: %s.", user_id)
