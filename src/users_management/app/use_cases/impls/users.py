"""
Module for users use case implementation.
"""

from typing import Any, Dict, Self

from users_management.app.schemas.requests import CreateUserRequest
from users_management.app.schemas.users import SInfoUser
from users_management.app.services import UsersServiceProtocol
from users_management.app.use_cases import UsersUseCaseProtocol


class UsersUseCaseImpl(UsersUseCaseProtocol):
    def __init__(
        self,
        users_service: UsersServiceProtocol,
    ):
        self._users_service = users_service

    async def get_user_by_id(
        self: Self,
        user_id: int,
    ) -> SInfoUser:
        user = await self._users_service.get_user_by_id(user_id)
        return user

    async def find_user_by_nickname(
        self: Self,
        nickname: str,
    ) -> None:
        await self._users_service.find_user_by_nickname(nickname)

    async def get_list_users_by_id(
        self: Self,
        users_id: list[int],
    ) -> list[SInfoUser]:
        users_data = await self._users_service.get_users_list(users_id)
        return users_data

    async def create_user(
        self: Self,
        data: CreateUserRequest,
    ) -> SInfoUser:
        return await self._users_service.create_user(data)

    async def update_user(
        self: Self,
        user_id: int,
        data: Dict[str, Any],
    ) -> SInfoUser:
        return await self._users_service.update_user(user_id, data)

    async def delete_user(
        self: Self,
        user_id: int,
    ) -> None:
        await self._users_service.delete_user(user_id)
