from typing import Any, Self

from src.app.schemas.users import SInfoUser
from src.core.schemas import SAddInfoUser
from src.app.services import UsersServiceProtocol
from src.app.repositories import SQLRepositoryProtocol
from src.core.db import RepositoryUOW


class UsersServiceImpl(UsersServiceProtocol):

    def __init__(
        self,
        sql_repository: SQLRepositoryProtocol,
        db_uow: RepositoryUOW,
    ):
        self.sql_repository = sql_repository
        self.db_uow = db_uow

    async def get_user(
        self: Self,
        user_id: int,
    ) -> SInfoUser:
        async with self.db_uow as uow:
            user = await self.sql_repository.get_user(uow, user_id)
        return user

    async def create_user(
        self: Self,
        **data: SAddInfoUser,
    ) -> None:
        async with self.db_uow as uow:
            await self.sql_repository.add_user(uow, **data)

    async def update_user(
        self: Self,
        user_id: int,
        **data: Any,
    ) -> None:
        async with self.db_uow as uow:
            await self.sql_repository.update_user(uow, user_id, **data)

    async def delete_user(
        self: Self,
        user_id: int,
    ) -> None:
        async with self.db_uow as uow:
            await self.sql_repository.delete_user(uow, user_id)
