from fastapi import APIRouter
from sqlalchemy.future import select

from users_management.app.exceptions import (
    RedisHealthException,
    SQLRepositoryException,
)
from users_management.core.depends import RedisManager, SQLDBHelper
from users_management.core.schemas import SSuccessfulRequest
from users_management.settings import settings


class Readiness:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route(
            settings.api.readiness,
            self.get_readiness,
            methods=["GET"],
            response_model=SSuccessfulRequest,
            status_code=200,
        )

    async def get_readiness(
        self,
    ) -> SSuccessfulRequest:
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


readiness = Readiness()

router = readiness.router
