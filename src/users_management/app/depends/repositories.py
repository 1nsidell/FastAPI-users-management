"""
ioc container for creating repositories.
"""

from typing import Annotated, Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from users_management.app.depends.config_factory import RedisConfigService
from users_management.app.depends.connections import (
    AsyncSessionFactory,
    RedisPool,
)
from users_management.app.schemas.users import SInfoUser
from users_management.gateways.repositories import (
    CacheRepositoryProtocol,
    UsersRepositoryProtocol,
)
from users_management.gateways.repositories.impls.users import (
    UsersRepositoryImpl,
)
from users_management.gateways.repositories.impls.users_cache import (
    UsersCacheRepositoryImpl,
)
from users_management.gateways.transactions import RepositoryManagerProtocol
from users_management.gateways.transactions.impls.sql_repository_manager import (
    SQLTransactionsManagerImpl,
)


# Repositories manager --------------------------


def users_repo_factory(session: AsyncSession) -> UsersRepositoryProtocol:
    return UsersRepositoryImpl(session=session)


def get_users_repo_factory() -> (
    Callable[[AsyncSession], UsersRepositoryProtocol]
):
    return users_repo_factory


UsersRepoFactory = Annotated[
    Callable[[AsyncSession], UsersRepositoryProtocol],
    Depends(get_users_repo_factory),
]


def get_uow(
    async_session_factory: AsyncSessionFactory,
    users_repo_factory: UsersRepoFactory,
) -> RepositoryManagerProtocol:
    """Create a Depends instance of uow."""
    return SQLTransactionsManagerImpl(
        async_session_factory=async_session_factory,
        users_repo_factory=users_repo_factory,
    )


RepositoryManager = Annotated[RepositoryManagerProtocol, Depends(get_uow)]


# Cache repositories --------------------------


def get_users_cache_repository(
    redis_pool: RedisPool,
    config: RedisConfigService,
) -> CacheRepositoryProtocol[SInfoUser]:
    return UsersCacheRepositoryImpl(redis=redis_pool, config=config)


RedisUsersCacheRepository = Annotated[
    CacheRepositoryProtocol[SInfoUser], Depends(get_users_cache_repository)
]
