from fastapi import APIRouter, Header, Path, status

from users_management.app.depends import APIAccessProvider, UsersUseCase
from users_management.app.schemas.responses import ErrorResponse
from users_management.settings import settings

router = APIRouter()


@router.delete(
    f"{settings.api.users}/{{user_id}}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorResponse,
            "description": "API key validation failed",
            "content": {
                "application/json": {
                    "example": {
                        "error_type": "API_KEY_ERROR",
                        "message": "API key rejected.",
                    }
                }
            },
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorResponse,
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "examples": {
                        "sql_error": {
                            "summary": "Database error",
                            "value": {
                                "error_type": "SQL_REPOSITORY_ERROR",
                                "message": "SQL repository working error.",
                            },
                        },
                        "unknown_error": {
                            "summary": "Unexpected error",
                            "value": {
                                "error_type": "INTERNAL_SERVER_ERROR",
                                "message": "Internal server error",
                            },
                        },
                    }
                }
            },
        },
    },
)
async def delete_user(
    api_access_provider: APIAccessProvider,
    users_use_case: UsersUseCase,
    user_id: int = Path(...),
    api_key: str = Header(..., alias="X-API-Key"),
) -> None:
    """Delete a user from the system.

    Args:
        user_id (int): Unique identifier of the user to delete
        api_key (str): API key for authentication (passed in X-API-Key header)

    Returns:
        None: Returns nothing, status code 204 indicates successful deletion

    Example Request:
        DELETE /api/users-management/v1/users/123
        Headers:
            X-API-Key: your-api-key

    Example Success Response:
        Status: 204 No Content
    """

    api_access_provider.check_api_key(api_key)
    await users_use_case.delete_user(user_id)
