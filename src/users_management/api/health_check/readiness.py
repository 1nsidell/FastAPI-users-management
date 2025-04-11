from fastapi import APIRouter, status
from sqlalchemy.future import select

from users_management.app.exceptions import (
    RedisHealthException,
    SQLRepositoryException,
)
from users_management.core.depends import RedisManager, SQLDBHelper
from users_management.core.schemas import SErrorResponse, SSuccessfulRequest
from users_management.settings import settings

router = APIRouter()


@router.get(
    settings.api.readiness,
    response_model=SSuccessfulRequest,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "model": SErrorResponse,
            "description": "Service dependencies are not ready",
            "content": {
                "application/json": {
                    "examples": {
                        "redis_error": {
                            "summary": "Redis connection error",
                            "value": {
                                "error_type": "REDIS_ERROR",
                                "message": "Redis connection error.",
                            },
                        },
                        "redis_ping_error": {
                            "summary": "Redis ping failed",
                            "value": {
                                "error_type": "REDIS_ERROR",
                                "message": "Redis ping failed.",
                            },
                        },
                        "sql_error": {
                            "summary": "SQL Database error",
                            "value": {
                                "error_type": "SQL_REPOSITORY_ERROR",
                                "message": "SQL connectivity error.",
                            },
                        },
                    }
                }
            },
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": SErrorResponse,
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "error_type": "INTERNAL_SERVER_ERROR",
                        "message": "Internal server error",
                    }
                }
            },
        },
    },
)
async def get_readiness() -> SSuccessfulRequest:
    """Check if the service and its dependencies are ready to handle requests.

    This endpoint performs a deep health check by verifying connectivity to:
    - Redis cache database
    - SQL database

    Returns:
        SSuccessfulRequest: A success response if all dependencies are available
            Response body: {"message": "success"}

    Example Request:
        GET /api/users-management/healthcheck/readiness

    Example Success Response:
        Status: 200 OK
        Body: {"message": "success"}

    Note:
        Unlike the /liveness endpoint, this check verifies that all critical
        dependencies are available and the service is ready to handle requests.
    """
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
