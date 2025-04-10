from fastapi import APIRouter, status

from users_management.core.schemas import SSuccessfulRequest
from users_management.settings import settings

router = APIRouter()


@router.get(
    settings.api.liveness,
    response_model=SSuccessfulRequest,
    status_code=status.HTTP_200_OK,
)
async def get_liveness() -> SSuccessfulRequest:
    """Check if the service is alive.

    This endpoint performs a basic health check to verify that the service
    is up and running. If the service is down, the client will receive
    a connection error instead of an HTTP response.

    Returns:
        SSuccessfulRequest: A success response indicating the service is alive
            Response body: {"message": "success"}

    Example Request:
        GET /api/users-management/healthcheck/liveness

    Example Success Response:
        Status: 200 OK
        Body: {"message": "success"}

    Note:
        If the service is completely down, no HTTP response will be returned
        and the client will receive a connection error or timeout.
    """
    return SSuccessfulRequest()
