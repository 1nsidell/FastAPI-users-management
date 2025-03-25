"""
A protocol describing the methods and attributes of a repository,
that must be defined for the application to work
"""

import logging
from typing import Any, Dict, Optional, Self

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from users_management.app.models import InfoUser
from users_management.app.repositories import (
    UsersSQLRepositoryProtocol,
    handle_sql_exceptions,
)
from users_management.app.schemas.users import SInfoUser
from users_management.core.schemas import SAddInfoUser

log = logging.getLogger(__name__)


class UsersSQLRepositoryImpl(UsersSQLRepositoryProtocol):
    USER_INFO_MODEL = InfoUser

    @handle_sql_exceptions
    async def get_user(
        self: Self,
        session: AsyncSession,
        **filter_by: Any,
    ) -> Optional[SInfoUser]:
        log.info("Request user data with filter: %s.", filter_by)
        stmt = select(self.USER_INFO_MODEL).filter_by(**filter_by)
        result = await session.execute(stmt)
        user_orm = result.scalars().one_or_none()
        if not user_orm:
            log.info("User not found with filter: %s.", filter_by)
            return None
        user = SInfoUser.model_validate(user_orm, from_attributes=True)
        log.info("User data found filter by: %s.", filter_by)
        return user

    @handle_sql_exceptions
    async def get_users_list(
        self: Self,
        session: AsyncSession,
        users_id: list[int],
    ) -> Optional[list[SInfoUser]]:
        log.info("Request list of users data with IDs: %s.", users_id)
        stmt = select(self.USER_INFO_MODEL).filter(
            self.USER_INFO_MODEL.user_id.in_(users_id)
        )
        result = await session.execute(stmt)
        users_list_orm = result.scalars().all()
        if len(users_list_orm) < len(users_id):
            log.warning(
                "Not all user data was found with filter: %s.", users_id
            )
            return None
        users_list = [
            SInfoUser.model_validate(user, from_attributes=True)
            for user in users_list_orm
        ]
        log.info("Users data found with filter: %s.", users_id)
        return users_list

    @handle_sql_exceptions
    async def create_user(
        self: Self,
        session: AsyncSession,
        data: SAddInfoUser,
    ) -> SInfoUser:
        log.info(
            "Creating new user with ID: %s and nickname: %s.",
            data.user_id,
            data.nickname,
        )
        stmt = (
            insert(self.USER_INFO_MODEL)
            .values(data.model_dump())
            .returning(self.USER_INFO_MODEL)
        )
        result = await session.execute(stmt)
        user_orm = result.scalars().one_or_none()
        log.info(
            "User successfully created with ID: %s and nickname: %s.",
            data.user_id,
            data.nickname,
        )
        user = SInfoUser.model_validate(user_orm, from_attributes=True)
        return user

    @handle_sql_exceptions
    async def update_user(
        self: Self,
        session: AsyncSession,
        user_id: int,
        data: Dict[str, Any],
    ) -> SInfoUser:
        log.info(
            "User with ID: %s is trying to update the data on: %s.",
            data,
            user_id,
        )
        stmt = (
            update(self.USER_INFO_MODEL)
            .where(self.USER_INFO_MODEL.user_id == user_id)
            .values(**data)
            .returning(self.USER_INFO_MODEL)
        )
        result = await session.execute(stmt)
        user_orm = result.scalars().one_or_none()
        log.info("User with ID: %s successful updated data: %s.", user_id, data)
        user = SInfoUser.model_validate(
            user_orm["InfoUser"], from_attributes=True
        )
        return user

    @handle_sql_exceptions
    async def delete_user(
        self: Self,
        session: AsyncSession,
        user_id: int,
    ) -> None:
        log.info("User deletion with ID: %s.", user_id)
        stmt = delete(self.USER_INFO_MODEL).where(
            self.USER_INFO_MODEL.user_id == user_id
        )
        await session.execute(stmt)
        log.info("Successful deletion user with ID: %s.", user_id)
