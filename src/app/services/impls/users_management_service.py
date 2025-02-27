from typing import Any, Dict, Self

from core.db import UOWFactory
from src.app.repositories import SQLRepositoryProtocol
from src.app.schemas.users import SInfoUser
from src.app.services import UsersManagementServiceProtocol
from src.core.exceptions import UserNotFoundException
from src.core.schemas import SAddInfoUser


class UsersManagementServiceImpl(UsersManagementServiceProtocol):

    def __init__(
        self,
        sql_repository: SQLRepositoryProtocol,
        uow_factory: UOWFactory,
    ):
        self.sql_repository = sql_repository
        self.uow_factory = uow_factory

    async def get_user(
        self: Self,
        user_id: int,
    ) -> SInfoUser:
        async with self.uow_factory() as session:
            user = await self.sql_repository.get_user(session, user_id)
        if not user:
            raise UserNotFoundException()
        return user

    async def create_user(
        self: Self,
        data: SAddInfoUser,
    ) -> None:
        async with self.uow_factory() as session:
            await self.sql_repository.add_user(session, data)

    async def update_user(
        self: Self,
        user_id: int,
        data: Dict[str, Any],
    ) -> None:
        async with self.uow_factory() as session:
            await self.sql_repository.update_user(session, user_id, data)

    async def delete_user(
        self: Self,
        user_id: int,
    ) -> None:
        async with self.uow_factory() as session:
            await self.sql_repository.delete_user(session, user_id)
