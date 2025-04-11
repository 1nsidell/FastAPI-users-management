"""Dependency injection container module for FastAPI application.

This module provides dependency injection containers for:
- Database connections (SQL, Redis)
- Application settings
"""

from typing import Annotated, Callable, Final

from fastapi import Depends
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession

from users_management.core.gateways import (
    RedisConnectionManager,
    SQLDatabaseHelper,
)
from users_management.core.services.transactions import SQLRepositoryUOW
from users_management.settings import Settings, get_settings, settings


# ================== Global Instances (for lifespan) ==================
def get_sql_db_helper(settings: Settings) -> SQLDatabaseHelper:
    return SQLDatabaseHelper(settings)


SQLDBHelper: Final[SQLDatabaseHelper] = get_sql_db_helper(settings)


def get_redis_manager(settings: Settings) -> RedisConnectionManager:
    return RedisConnectionManager(settings)


RedisManager: Final[RedisConnectionManager] = get_redis_manager(settings)


# ================== Settings Dependencies ==================
SettingsService = Annotated[Settings, Depends(get_settings)]


# ================== SQL Database Dependencies ==================
def get_async_session_factory() -> Callable[[], AsyncSession]:
    """Getting async session factory for Depends object."""
    return SQLDBHelper.async_session_factory


AsyncSessionFactory = Annotated[
    Callable[[], AsyncSession], Depends(get_async_session_factory)
]


def get_uow(async_session_factory: AsyncSessionFactory) -> SQLRepositoryUOW:
    """Create a Depends instance of uow."""
    return SQLRepositoryUOW(async_session_factory)


UoW = Annotated[SQLRepositoryUOW, Depends(get_uow)]


# ================== Redis Dependencies ==================
def get_redis_pool() -> redis.Redis:
    """Create a Depends instance of Redis connection."""
    return RedisManager.redis


RedisPool = Annotated[redis.Redis, Depends(get_redis_pool)]
