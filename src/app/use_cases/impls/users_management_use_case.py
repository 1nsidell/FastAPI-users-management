from typing import Any, Self

from src.app.schemas.users import SInfoUser
from src.app.services import UsersServiceProtocol
from src.app.use_cases import UsersUseCaseProtocol
from src.core.schemas import SAddInfoUser


class UsersUseCaseImpl(UsersUseCaseProtocol):

    def __init__(
        self,
        UsersService: UsersServiceProtocol,
    ):
        self.users_service = UsersService

    async def get_user(
        self: Self,
        user_id: int,
    ) -> SInfoUser:
        user = await self.users_service.get_user(user_id)
        return user

    async def create_user(
        self: Self,
        data: SAddInfoUser,
    ) -> None:
        await self.users_service.create_user(data)

    async def update_user(
        self: Self,
        user_id: int,
        data: Any,
    ) -> None:
        await self.users_service.update_user(user_id, data)

    async def delete_user(
        self: Self,
        user_id: int,
    ) -> None:
        await self.users_service.delete_user(user_id)
