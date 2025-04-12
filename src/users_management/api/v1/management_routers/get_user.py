from fastapi import APIRouter, Header, Path, status

from users_management.app.depends import APIAccessProvider, UsersUseCase
from users_management.app.schemas.responses import ErrorResponse
from users_management.app.schemas.users import SInfoUser
from users_management.settings import settings

router = APIRouter()


@router.get(
    f"{settings.api.users}/{{user_id}}",
    response_model=SInfoUser,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorResponse,
            "description": "API key rejected",
            "content": {
                "application/json": {
                    "example": {
                        "error_type": "API_KEY_ERROR",
                        "message": "API key rejected.",
                    }
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {
                        "error_type": "USER_NOT_FOUND",
                        "message": "User not found.",
                    }
                }
            },
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorResponse,
            "description": "Database operation failed",
            "content": {
                "application/json": {
                    "example": {
                        "error_type": "SQL_REPOSITORY_ERROR",
                        "message": "SQL repository working error.",
                    }
                }
            },
        },
    },
)
async def get_user(
    api_access_provider: APIAccessProvider,
    users_use_case: UsersUseCase,
    user_id: int = Path(...),
    api_key: str = Header(..., alias="X-API-Key"),
) -> SInfoUser:
    """Get information about a specific user by their ID.

    Args:
        user_id (int): Unique identifier of the user to retrieve
        api_key (str): API key for authentication (passed in X-API-Key header)

    Returns:
        SInfoUser: User information object containing:
            - user_id (int): User's unique identifier
            - nickname (str): User's nickname
            - is_active (bool): User's active status
            - is_verified (bool): User's verification status
            - avatar (bool): User's avatar status

    Example Request:
        GET /api/users-management/v1/users/123
        Headers:
            X-API-Key: your-api-key

    Example Success Response:
        Status: 200 OK
        Body: {
            "user_id": 123,
            "nickname": "john_doe",
            "is_active": true,
            "is_verified": false,
            "avatar": false
        }
    """

    api_access_provider.check_api_key(api_key)
    return await users_use_case.get_user_by_id(user_id)
