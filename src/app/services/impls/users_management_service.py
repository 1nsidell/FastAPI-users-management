import logging
from typing import Any, Dict, Self

from core.db import SQLRepositoryUOWProtocol
from src.app.exceptions import RedisCacheDBException
from src.app.repositories import (
    CacheRepositoryProtocol,
    UsersSQLRepositoryProtocol,
)
from src.app.schemas.users import SInfoUser
from src.app.services import UsersManagementServiceProtocol
from src.core.exceptions import UserAlreadyExistException, UserNotFoundException
from src.core.schemas import SAddInfoUser

log = logging.getLogger("app")


class UsersManagementServiceImpl(UsersManagementServiceProtocol):

    def __init__(
        self,
        users_sql_repository: UsersSQLRepositoryProtocol,
        redis_users_cache: CacheRepositoryProtocol,
        uow: SQLRepositoryUOWProtocol,
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

    async def create_user(
        self: Self,
        data: SAddInfoUser,
    ) -> None:
        async with self.uow as session:
            if await self.users_sql_repository.get_user(
                session, nickname=data.nickname
            ):
                raise UserAlreadyExistException()
            await self.users_sql_repository.add_user(session, data)
            user = await self.users_sql_repository.get_user(
                session, user_id=data.user_id
            )
        try:
            await self.redis_users_cache.add_user(
                data.user_id, user.model_dump()
            )
        except RedisCacheDBException:
            log.warning("Cache operation failed.", exc_info=True)

    async def update_user(
        self: Self,
        user_id: int,
        data: Dict[str, Any],
    ) -> None:
        async with self.uow as session:
            await self.users_sql_repository.update_user(session, user_id, data)
            user = await self.users_sql_repository.get_user(
                session, user_id=user_id
            )
        try:
            await self.redis_users_cache.add_user(user_id, user.model_dump())
        except RedisCacheDBException:
            log.warning("Cache operation failed.", exc_info=True)

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
