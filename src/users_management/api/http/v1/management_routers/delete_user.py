from fastapi import APIRouter, Header, Path, status

from users_management.app.depends import APIAccessProvider, UsersUseCase
from users_management.app.schemas.responses import (
    API_KEY_ERROR,
    INTERNAL_SERVER_ERROR,
)
from users_management.core.settings import settings

router = APIRouter()


@router.delete(
    f"{settings.api.users}/{{user_id}}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_403_FORBIDDEN: API_KEY_ERROR,
        status.HTTP_500_INTERNAL_SERVER_ERROR: INTERNAL_SERVER_ERROR,
    },
)
async def delete_user(
    api_access_provider: APIAccessProvider,
    users_use_case: UsersUseCase,
    user_id: int = Path(...),
    api_key: str = Header(..., alias="X-API-Key"),
) -> None:
    """Delete a user from the system.

    Parameters
    ----------
    user_id : int
        Unique identifier of user to delete
    api_key : str
        API key for authentication (X-API-Key header)

    Returns
    -------
    None
        204 status code on successful deletion

    Raises
    ------
    HTTPException
        * 403: If API key validation fails
        * 500: If database error occurs

    Example
    -------
    Request:
    ```http
        DELETE /api/users-management/v1/users/123
        Headers:
            X-API-Key: your-api-key
    ```

    Response:
    ```http
        Status: 204 No Content
    ```
    """

    api_access_provider.check_api_key(api_key)
    await users_use_case.delete_user(user_id)
