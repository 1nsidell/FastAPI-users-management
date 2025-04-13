from fastapi import APIRouter, Header, status

from users_management.app.depends import APIAccessProvider, UsersUseCase
from users_management.app.schemas.requests import CreateUserRequest
from users_management.app.schemas.responses import (
    API_KEY_ERROR,
    INTERNAL_SERVER_ERROR,
    USERNAME_CONFLICT,
)
from users_management.app.schemas.users import SInfoUser
from users_management.core.settings import settings

router = APIRouter()


@router.post(
    settings.api.users,
    response_model=SInfoUser,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_403_FORBIDDEN: API_KEY_ERROR,
        status.HTTP_409_CONFLICT: USERNAME_CONFLICT,
        status.HTTP_500_INTERNAL_SERVER_ERROR: INTERNAL_SERVER_ERROR,
    },
)
async def create_user(
    api_access_provider: APIAccessProvider,
    users_use_case: UsersUseCase,
    user_info: CreateUserRequest,
    api_key: str = Header(..., alias="X-API-Key"),
) -> SInfoUser:
    """Create a new user in the system.

    Creates a new user with the provided user ID and nickname. The API key is required
    for authentication.

    Parameters
    ----------
    user_info : CreateUserRequest
        The user information containing:
        * user_id: Unique positive integer identifier for the user
        * nickname: Unique string username for the user
    api_key : str
        API key for authentication (provide in X-API-Key header)

    Returns
    -------
    SInfoUser
        The created user information object containing:
        * user_id: The user's unique identifier
        * nickname: The user's nickname
        * is_active: User's active status (default: True)
        * is_verified: User's verification status (default: False)
        * avatar: User's avatar status (default: False)

    Raises
    ------
    HTTPException
        * 403: If API key validation fails
        * 409: If username already exists
        * 500: If database error occurs or other internal error

    Example
    -------
    Request:
    ```http
        POST /api/users-management/v1/users
        Headers:
            X-API-Key: your-api-key
        Body:
            {
                "user_id": 123,
                "nickname": "john_doe"
            }
    ```

    Response:
    ```json
    {
        "user_id": 123,
        "nickname": "john_doe",
        "is_active": true,
        "is_verified": false,
        "avatar": false
    }
    ```
    """
    api_access_provider.check_api_key(api_key)
    return await users_use_case.create_user(user_info)
