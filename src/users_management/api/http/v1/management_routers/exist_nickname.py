from fastapi import APIRouter, Header, Path, status

from users_management.app.depends import APIAccessProvider, UsersUseCase
from users_management.app.schemas.responses import (
    API_KEY_ERROR,
    INTERNAL_SERVER_ERROR,
    USERNAME_CONFLICT,
    SuccessResponse,
)
from users_management.core.settings import settings


router = APIRouter()


@router.get(
    f"{settings.api.nicknames}/{{nickname}}",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_403_FORBIDDEN: API_KEY_ERROR,
        status.HTTP_409_CONFLICT: USERNAME_CONFLICT,
        status.HTTP_500_INTERNAL_SERVER_ERROR: INTERNAL_SERVER_ERROR,
    },
)
async def exist_nickname(
    api_access_provider: APIAccessProvider,
    users_use_case: UsersUseCase,
    nickname: str = Path(...),
    api_key: str = Header(..., alias="X-API-Key"),
) -> SuccessResponse:
    """Check if a nickname is available in the system.

    Parameters
    ----------
    nickname : str
        Nickname to check for availability
    api_key : str
        API key for authentication (X-API-Key header)

    Returns
    -------
    SuccessResponse
        Success response if nickname is available
        * message: "success"

    Raises
    ------
    HTTPException
        * 403: If API key validation fails
        * 409: If nickname is already taken
        * 500: If database error occurs

    Example
    -------
    Request:
    ```http
        GET /api/users-management/v1/nicknames/john_doe
        Headers:
            X-API-Key: your-api-key
    ```

    Response:
    ```json
        {
            "message": "success"
        }
    ```
    """

    api_access_provider.check_api_key(api_key)
    await users_use_case.find_user_by_nickname(nickname)
    return SuccessResponse()
