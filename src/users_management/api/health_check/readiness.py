from fastapi import APIRouter
from sqlalchemy.future import select

from users_management.app.exceptions import (
    RedisHealthException,
    SQLRepositoryException,
)
from users_management.core.depends import RedisManager, SQLDBHelper
from users_management.core.schemas import SSuccessfulRequest
from users_management.settings import settings

router = APIRouter()


@router.get(
    settings.api.readiness,
    response_model=SSuccessfulRequest,
    status_code=200,
)
async def get_readiness() -> SSuccessfulRequest:
    try:
        pong = await RedisManager.redis.ping()
        if pong is not True:
            raise RedisHealthException("Redis ping failed.")
    except Exception:
        raise RedisHealthException("Redis connection error.")

    try:
        async with SQLDBHelper.async_session_factory() as session:
            await session.execute(select(1))
    except Exception:
        raise SQLRepositoryException("SQL connectivity error.")

    return SSuccessfulRequest()
