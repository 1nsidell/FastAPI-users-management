"""
Service implementation responsible for user management.
"""

import logging
from typing import Any, Callable, Dict, Self

from users_management.app.exceptions import (
    DataNotTransmitted,
    UserAlreadyExist_Nickname,
    UserAlreadyExistException,
    UserNotFoundException,
)
from users_management.app.schemas.requests import CreateUserRequest
from users_management.app.schemas.users import SInfoUser
from users_management.app.services import UsersServiceProtocol
from users_management.gateways.repositories import CacheRepositoryProtocol
from users_management.gateways.transactions import RepositoryManagerProtocol


log = logging.getLogger(__name__)


class UsersServiceImpl(UsersServiceProtocol):
    def __init__(
        self,
        repository_manager: RepositoryManagerProtocol,
        users_cache: CacheRepositoryProtocol[SInfoUser],
        key_builder: Callable[[int], str],
    ) -> None:
        self._repository_manager = repository_manager
        self._users_cache = users_cache
        self._key_builder = key_builder

    async def get_user_by_id(
        self: Self,
        user_id: int,
    ) -> SInfoUser:
        key = self._key_builder(user_id)
        if user := await self._users_cache.get(key):
            log.info("User found in cache: %s.", user_id)
            return user
        async with self._repository_manager as uow:
            user = await uow.users_repository.get_user(user_id=user_id)
        if not user:
            raise UserNotFoundException()
        await self._users_cache.add(key, user)
        return user

    async def get_users_list(
        self: Self,
        users_id: list[int],
    ) -> list[SInfoUser]:
        keys = [self._key_builder(user_id) for user_id in users_id]
        if users := await self._users_cache.get_list(keys):
            log.info("Users found in cache: %s.", users_id)
            return users
        async with self._repository_manager as uow:
            users = await uow.users_repository.get_users_list(users_id=users_id)
        if not users:
            raise UserNotFoundException()
        await self._users_cache.add_list(users)
        return users

    async def find_user_by_nickname(
        self: Self,
        nickname: str,
    ) -> None:
        async with self._repository_manager as uow:
            user = await uow.users_repository.get_user(nickname=nickname)
        if user:
            raise UserAlreadyExistException()

    async def create_user(
        self: Self,
        data: CreateUserRequest,
    ) -> SInfoUser:
        async with self._repository_manager as uow:
            if await uow.users_repository.get_user(nickname=data.nickname):
                raise UserAlreadyExist_Nickname()
            user = await uow.users_repository.create_user(data)
        key = self._key_builder(user.user_id)
        await self._users_cache.add(key, user)
        return user

    async def update_user(
        self: Self,
        user_id: int,
        data: Dict[str, Any],
    ) -> SInfoUser:
        if not data:
            raise DataNotTransmitted()
        async with self._repository_manager as uow:
            user = await uow.users_repository.update_user(user_id, data)
        key = self._key_builder(user.user_id)
        await self._users_cache.add(key, user)
        return user

    async def delete_user(
        self: Self,
        user_id: int,
    ) -> None:
        async with self._repository_manager as uow:
            await uow.users_repository.delete_user(user_id)
        key = self._key_builder(user_id)
        await self._users_cache.delete(key)
