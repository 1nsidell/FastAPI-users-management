from fastapi import APIRouter, status

from users_management.app.schemas.responses import SuccessResponse
from users_management.core.settings import settings


router = APIRouter()


@router.get(
    settings.api.liveness,
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
)
async def get_liveness() -> SuccessResponse:
    """Check if the service is alive.

    Performs basic health check to verify service availability.

    Returns
    -------
    SuccessResponse
        Success response with message
        * message: "success"

    Example
    -------
    Request:
    ```http
        GET /api/users-management/healthcheck/liveness
    ```

    Response:
    ```json
        {
            "message": "success"
        }
    ```

    Notes
    -----
    If service is down, connection error will occur instead of HTTP response
    """
    return SuccessResponse()
