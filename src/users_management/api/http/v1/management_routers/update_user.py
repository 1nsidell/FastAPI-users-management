from typing import Any, Dict

from fastapi import APIRouter, Header, Path, status

from users_management.app.depends import APIAccessProvider, UsersUseCase
from users_management.app.schemas.responses import (
    API_KEY_ERROR,
    DATA_NOT_TRANSMITTED,
    INTERNAL_SERVER_ERROR,
    USER_NOT_FOUND,
)
from users_management.app.schemas.users import SInfoUser
from users_management.core.settings import settings


router = APIRouter()


@router.patch(
    f"{settings.api.users}/{{user_id}}",
    response_model=SInfoUser,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: DATA_NOT_TRANSMITTED,
        status.HTTP_403_FORBIDDEN: API_KEY_ERROR,
        status.HTTP_404_NOT_FOUND: USER_NOT_FOUND,
        status.HTTP_500_INTERNAL_SERVER_ERROR: INTERNAL_SERVER_ERROR,
    },
)
async def update_user(
    api_access_provider: APIAccessProvider,
    users_use_case: UsersUseCase,
    user_info: Dict[str, Any],
    user_id: int = Path(...),
    api_key: str = Header(..., alias="X-API-Key"),
) -> SInfoUser:
    """Update user information.

    Parameters
    ----------
    user_info : Dict[str, Any]
        Fields to update:
        * nickname: New nickname (optional)
        * is_active: New active status (optional)
        * is_verified: New verification status (optional)
        * avatar: New avatar status (optional)
    user_id : int
        Unique identifier of user to update
    api_key : str
        API key for authentication (X-API-Key header)

    Returns
    -------
    SInfoUser
        Updated user information containing:
        * user_id: Unique identifier
        * nickname: Updated nickname
        * is_active: Updated active status
        * is_verified: Updated verification status
        * avatar: Updated avatar status

    Raises
    ------
    HTTPException
        * 400: If no update data provided
        * 403: If API key validation fails
        * 404: If user not found
        * 500: If database or cache error occurs

    Example
    -------
    Request:
    ```http
        PATCH /api/users-management/v1/users/123
        Headers:
            X-API-Key: your-api-key
        Body:
            {
                "nickname": "new_nickname",
                "is_verified": true
            }
    ```

    Response:
    ```json
    {
        "user_id": 123,
        "nickname": "new_nickname",
        "is_active": true,
        "is_verified": true,
        "avatar": false
    }
    ```
    """
    api_access_provider.check_api_key(api_key)
    return await users_use_case.update_user(user_id, user_info)
