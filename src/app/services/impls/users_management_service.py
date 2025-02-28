from typing import Any, Dict, Self

from core.db import RepositoryUOWProtocol
from src.app.repositories import UsersSQLRepositoryProtocol
from src.app.schemas.users import SInfoUser
from src.app.services import UsersManagementServiceProtocol
from src.core.exceptions import UserAlreadyExistException, UserNotFoundException
from src.core.schemas import SAddInfoUser


class UsersManagementServiceImpl(UsersManagementServiceProtocol):

    def __init__(
        self,
        users_sql_repository: UsersSQLRepositoryProtocol,
        uow: RepositoryUOWProtocol,
    ):
        self.users_sql_repository = users_sql_repository
        self.uow = uow

    async def get_user_by_id(
        self: Self,
        user_id: int,
    ) -> SInfoUser:
        async with self.uow as session:
            user = await self.users_sql_repository.get_user_by_id(
                session, user_id
            )
        if not user:
            raise UserNotFoundException()
        return user

    async def create_user(
        self: Self,
        data: SAddInfoUser,
    ) -> None:
        async with self.uow as session:
            if self.users_sql_repository.user_exists(session, data.nickname):
                raise UserAlreadyExistException()
            await self.users_sql_repository.add_user(session, data)

    async def update_user(
        self: Self,
        user_id: int,
        data: Dict[str, Any],
    ) -> None:
        async with self.uow as session:
            await self.users_sql_repository.update_user(session, user_id, data)

    async def delete_user(
        self: Self,
        user_id: int,
    ) -> None:
        async with self.uow as session:
            await self.users_sql_repository.delete_user(session, user_id)
