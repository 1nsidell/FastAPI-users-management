"""
Service implementation responsible for user management.
"""

import logging
from typing import Any, Callable, Dict, Self

from users_management.app.exceptions import (
    DataNotTransmitted,
    RedisCacheDBException,
    UserAlreadyExist_Nickname,
    UserAlreadyExistException,
    UserNotFoundException,
)
from users_management.app.schemas.requests import CreateUserRequest
from users_management.app.schemas.users import SInfoUser
from users_management.app.services import UsersManagementServiceProtocol
from users_management.gateways.repositories import (
    UsersCacheRepositoryProtocol,
    UsersSQLRepositoryProtocol,
)
from users_management.gateways.transactions import UnitOfWorkProtocol


log = logging.getLogger(__name__)


class UsersManagementServiceImpl(UsersManagementServiceProtocol):
    def __init__(
        self,
        users_repository: UsersSQLRepositoryProtocol,
        users_cache: UsersCacheRepositoryProtocol,
        uow: UnitOfWorkProtocol,
    ):
        self.users_repository = users_repository
        self.users_cache = users_cache
        self.uow = uow

    async def _with_cache_fallback(self, operation: Callable, *args, **kwargs):
        try:
            return await operation(*args, **kwargs)
        except RedisCacheDBException:
            log.warning("Cache operation failed.", exc_info=True)
            return None

    async def get_user_by_id(
        self: Self,
        user_id: int,
    ) -> SInfoUser:
        user = await self._with_cache_fallback(
            self.users_cache.get_user, key=user_id
        )
        if user:
            return user
        async with self.uow as session:
            user = await self.users_repository.get_user(
                session, user_id=user_id
            )
        if not user:
            raise UserNotFoundException()
        await self._with_cache_fallback(
            self.users_cache.add_user, key=user_id, data=user
        )
        return user

    async def get_users_list(
        self: Self,
        users_id: list[int],
    ) -> list[SInfoUser]:
        users = await self._with_cache_fallback(
            self.users_cache.get_list_users, keys=users_id
        )
        if users:
            return users
        async with self.uow as session:
            users = await self.users_repository.get_users_list(
                session, users_id=users_id
            )
        if not users:
            raise UserNotFoundException()
        await self._with_cache_fallback(
            self.users_cache.add_list_users,
            keys=users_id,
            data_list=users,
        )

        return users

    async def find_user_by_nickname(
        self: Self,
        nickname: str,
    ) -> None:
        async with self.uow as session:
            user = await self.users_repository.get_user(
                session, nickname=nickname
            )
        if user:
            raise UserAlreadyExistException()

    async def create_user(
        self: Self,
        data: CreateUserRequest,
    ) -> SInfoUser:
        async with self.uow as session:
            if await self.users_repository.get_user(
                session, nickname=data.nickname
            ):
                raise UserAlreadyExist_Nickname()
            user = await self.users_repository.create_user(session, data)
        await self._with_cache_fallback(
            self.users_cache.add_user,
            key=user.user_id,
            data=user,
        )
        return user

    async def update_user(
        self: Self,
        user_id: int,
        data: Dict[str, Any],
    ) -> SInfoUser:
        if not data:
            raise DataNotTransmitted()
        async with self.uow as session:
            user = await self.users_repository.update_user(
                session, user_id, data
            )
        await self._with_cache_fallback(
            self.users_cache.add_user,
            key=user_id,
            data=user,
        )
        return user

    async def delete_user(
        self: Self,
        user_id: int,
    ) -> None:
        async with self.uow as session:
            await self.users_repository.delete_user(session, user_id)
        await self._with_cache_fallback(
            self.users_cache.delete_user, key=user_id
        )
