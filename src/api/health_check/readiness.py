from fastapi import APIRouter
from sqlalchemy.future import select

from src.app.exceptions import (
    RedisHealthException,
    SQLRepositoryHealthException,
)
from src.core.depends import DBHelper, RedisPoolManager
from src.core.schemas import SSuccessfulRequest
from src.settings import settings


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
            pong = await RedisPoolManager.redis.ping()
            if pong is not True:
                raise RedisHealthException("Redis ping failed.")
        except Exception as e:
            raise RedisHealthException(f"Redis connection error: {e}") from e

        try:
            async with DBHelper.async_session_factory() as session:
                await session.execute(select(1))
        except Exception as e:
            raise SQLRepositoryHealthException(
                f"SQL connectivity error: {e}"
            ) from e

        return SSuccessfulRequest()


readiness = Readiness()

router = readiness.router
