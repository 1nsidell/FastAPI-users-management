from fastapi import APIRouter, Header, Path, status

from users_management.app.depends import APIAccessProvider, UsersUseCase
from users_management.app.schemas.responses import (
    API_KEY_ERROR,
    INTERNAL_SERVER_ERROR,
    USER_NOT_FOUND,
)
from users_management.app.schemas.users import SInfoUser
from users_management.core.settings import settings


router = APIRouter()


@router.get(
    f"{settings.api.users}/{{user_id}}",
    response_model=SInfoUser,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_403_FORBIDDEN: API_KEY_ERROR,
        status.HTTP_404_NOT_FOUND: USER_NOT_FOUND,
        status.HTTP_500_INTERNAL_SERVER_ERROR: INTERNAL_SERVER_ERROR,
    },
)
async def get_user(
    api_access_provider: APIAccessProvider,
    users_use_case: UsersUseCase,
    user_id: int = Path(...),
    api_key: str = Header(..., alias="X-API-Key"),
) -> SInfoUser:
    """Get information about a specific user.

    Parameters
    ----------
    user_id : int
        Unique identifier of the user
    api_key : str
        API key for authentication (X-API-Key header)

    Returns
    -------
    SInfoUser
        User information containing:
        * user_id: Unique identifier
        * nickname: User's nickname
        * is_active: Active status
        * is_verified: Verification status
        * avatar: Avatar status

    Raises
    ------
    HTTPException
        * 403: If API key validation fails
        * 404: If user not found
        * 500: If database error occurs

    Example
    -------
    Request:
    ```http
        GET /api/users-management/v1/users/123
        Headers:
            X-API-Key: your-api-key
    ```

    Response:
    ```json
    {
        "user_id": 123,
        "nickname": "john_doe",
        "avatar": false
    }
    ```
    """

    api_access_provider.check_api_key(api_key)
    return await users_use_case.get_user_by_id(user_id)
