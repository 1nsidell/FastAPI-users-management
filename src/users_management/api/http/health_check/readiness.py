from fastapi import APIRouter, status
from sqlalchemy.future import select

from users_management.app.depends.connections import (
    AsyncSessionFactory,
    RedisPool,
)
from users_management.app.exceptions import (
    RedisHealthException,
    SQLRepositoryException,
)
from users_management.app.schemas.responses import (
    INTERNAL_SERVER_ERROR,
    SERVICE_UNAVAILABLE,
    SuccessResponse,
)
from users_management.core.settings import settings


router = APIRouter()


@router.get(
    settings.api.readiness,
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: SERVICE_UNAVAILABLE,
        status.HTTP_500_INTERNAL_SERVER_ERROR: INTERNAL_SERVER_ERROR,
    },
)
async def get_readiness(
    Redis: RedisPool,
    SQLDatabase: AsyncSessionFactory,
) -> SuccessResponse:
    """Check if service and dependencies are ready.

    Performs deep health check of all critical dependencies.

    Returns
    -------
    SuccessResponse
        Success response with message
        * message: "success"

    Raises
    ------
    RedisHealthException
        If Redis connection fails
    SQLRepositoryException
        If SQL database connection fails

    Example
    -------
    Request:
    ```http
        GET /api/users-management/healthcheck/readiness
    ```

    Response:
    ```json
        {
            "message": "success"
        }
    ```
    Notes
    -----
    Checks:
    * Redis cache database connection
    * SQL database connection
    """
    try:
        pong = await Redis.ping()
        if pong is not True:
            raise RedisHealthException("Redis ping failed.")
    except Exception:
        raise RedisHealthException("Redis connection error.")

    try:
        async with SQLDatabase() as session:
            await session.execute(select(1))
    except Exception:
        raise SQLRepositoryException("SQL connectivity error.")

    return SuccessResponse()
