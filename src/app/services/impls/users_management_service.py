"""
Service implementation responsible for user management.
"""

import logging
from typing import Any, Dict, Self

from src.app.exceptions import (
    DataNotTransmitted,
    RedisCacheDBException,
    UserAlreadyExistException,
    UserNotFoundException,
)
from src.app.repositories import (
    UsersCacheRepositoryProtocol,
    UsersSQLRepositoryProtocol,
)
from src.app.schemas.users import SInfoUser
from src.app.services import UsersManagementServiceProtocol
from src.core.db import SQLRepositoryUOW
from src.core.schemas import SAddInfoUser

log = logging.getLogger("app")


class UsersManagementServiceImpl(UsersManagementServiceProtocol):

    def __init__(
        self,
        users_sql_repository: UsersSQLRepositoryProtocol,
        redis_users_cache: UsersCacheRepositoryProtocol,
        uow: SQLRepositoryUOW,
    ):
        self.users_sql_repository = users_sql_repository
        self.redis_users_cache = redis_users_cache
        self.uow = uow

    async def get_user_by_id(
        self: Self,
        user_id: int,
    ) -> SInfoUser:
        try:
            user = await self.redis_users_cache.get_user(user_id)
        except RedisCacheDBException:
            user = None
            log.warning("Cache operation failed.", exc_info=True)
        if user:
            return user
        async with self.uow as session:
            user = await self.users_sql_repository.get_user(
                session, user_id=user_id
            )
        if not user:
            raise UserNotFoundException()
        try:
            await self.redis_users_cache.add_user(user_id, user.model_dump())
        except RedisCacheDBException:
            log.warning("Cache operation failed.", exc_info=True)
        return user

    async def get_users_list(
        self: Self,
        users_id: list[int],
    ) -> list[SInfoUser]:
        try:
            users = await self.redis_users_cache.get_list_users(users_id)
        except RedisCacheDBException:
            users = None
            log.warning("Cache operation failed.", exc_info=True)
        if users:
            return users
        async with self.uow as session:
            users = await self.users_sql_repository.get_users_list(
                session, users_id=users_id
            )
        if not users:
            raise UserNotFoundException()
        try:
            await self.redis_users_cache.add_list_users(users)
        except RedisCacheDBException:
            log.warning("Cache operation failed.", exc_info=True)
        return users

    async def find_user_by_nickname(
        self: Self,
        nickname: str,
    ) -> None:
        async with self.uow as session:
            user = await self.users_sql_repository.get_user(
                session, nickname=nickname
            )
        if user:
            raise UserAlreadyExistException()

    async def create_user(
        self: Self,
        data: SAddInfoUser,
    ) -> SInfoUser:
        if not data:
            raise DataNotTransmitted()
        async with self.uow as session:
            user = await self.users_sql_repository.add_user(session, data)
        try:
            await self.redis_users_cache.add_user(
                data.user_id, user.model_dump()
            )
        except RedisCacheDBException:
            log.warning("Cache operation failed.", exc_info=True)
        return user

    async def update_user(
        self: Self,
        user_id: int,
        data: Dict[str, Any],
    ) -> SInfoUser:
        if not data:
            raise DataNotTransmitted()
        async with self.uow as session:
            user = await self.users_sql_repository.update_user(
                session, user_id, data
            )
        try:
            await self.redis_users_cache.add_user(user_id, user.model_dump())
        except RedisCacheDBException:
            log.warning("Cache operation failed.", exc_info=True)
        return user

    async def delete_user(
        self: Self,
        user_id: int,
    ) -> None:
        async with self.uow as session:
            await self.users_sql_repository.delete_user(session, user_id)
        try:
            await self.redis_users_cache.delete_user(user_id)
        except RedisCacheDBException:
            log.warning("Cache operation failed.", exc_info=True)
