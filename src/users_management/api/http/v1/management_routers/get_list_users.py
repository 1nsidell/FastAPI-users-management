from typing import List

from fastapi import APIRouter, Header, Query, status

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
    settings.api.users,
    response_model=List[SInfoUser],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_403_FORBIDDEN: API_KEY_ERROR,
        status.HTTP_404_NOT_FOUND: USER_NOT_FOUND,
        status.HTTP_500_INTERNAL_SERVER_ERROR: INTERNAL_SERVER_ERROR,
    },
)
async def get_list_user(
    api_access_provider: APIAccessProvider,
    users_use_case: UsersUseCase,
    users_id: List[int] = Query(...),
    api_key: str = Header(..., alias="X-API-Key"),
) -> List[SInfoUser]:
    """Get information about multiple users.

    Parameters
    ----------
    users_id : List[int]
        List of user IDs to retrieve
    api_key : str
        API key for authentication (X-API-Key header)

    Returns
    -------
    List[SInfoUser]
        List of user information objects containing:
        * user_id: Unique identifier
        * nickname: User's nickname
        * is_active: Active status
        * is_verified: Verification status
        * avatar: Avatar status

    Raises
    ------
    HTTPException
        * 403: API key validation failed
        * 404: Users not found
        * 500: Database or cache error

    Example
    -------
    Request:
    ```http
        GET /api/users-management/v1/users?users_id=1&users_id=2
        Headers:
            X-API-Key: your-api-key
    ```

    Response:
    ```json
        [
            {
                "user_id": 1,
                "nickname": "user1",
                "is_active": true,
                "is_verified": false,
                "avatar": false
            },
            {
                "user_id": 2,
                "nickname": "user2",
                "is_active": true,
                "is_verified": true,
                "avatar": true
            }
        ]
    ```
    """
    api_access_provider.check_api_key(api_key)
    return await users_use_case.get_list_users_by_id(users_id)
