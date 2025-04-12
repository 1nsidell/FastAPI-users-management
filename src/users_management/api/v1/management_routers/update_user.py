from typing import Any, Dict

from fastapi import APIRouter, Header, Path, status

from users_management.app.depends import APIAccessProvider, UsersUseCase
from users_management.app.schemas.responses import ErrorResponse
from users_management.app.schemas.users import SInfoUser
from users_management.settings import settings

router = APIRouter()


@router.patch(
    f"{settings.api.users}/{{user_id}}",
    response_model=SInfoUser,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Invalid request",
            "content": {
                "application/json": {
                    "example": {
                        "error_type": "DATA_NOT_TRANSMITTED",
                        "message": "No data transmitted for update.",
                    }
                }
            },
        },
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
                        "cache_error": {
                            "summary": "Cache error",
                            "value": {
                                "error_type": "REDIS_ERROR",
                                "message": "Cache operation failed.",
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
async def update_user(
    api_access_provider: APIAccessProvider,
    users_use_case: UsersUseCase,
    user_info: Dict[str, Any],
    user_id: int = Path(...),
    api_key: str = Header(..., alias="X-API-Key"),
) -> SInfoUser:
    """Update information for a specific user.

    Args:
        user_info (Dict[str, Any]): Dictionary containing fields to update
            Possible fields:
            - nickname (str): User's new nickname
            - is_active (bool): User's new active status
            - is_verified (bool): User's new verification status
            - avatar (bool): User's new avatar status
        user_id (int): Unique identifier of the user to update
        api_key (str): API key for authentication (passed in X-API-Key header)

    Returns:
        SInfoUser: Updated user information containing:
            - user_id (int): User's unique identifier
            - nickname (str): User's nickname
            - is_active (bool): User's active status
            - is_verified (bool): User's verification status
            - avatar (bool): User's avatar status

    Example Request:
        PATCH /api/users-management/v1/users/123
        Headers:
            X-API-Key: your-api-key
        Body:
            {
                "nickname": "new_nickname",
                "is_verified": true
            }

    Example Success Response:
        Status: 200 OK
        Body: {
            "user_id": 123,
            "nickname": "new_nickname",
            "is_active": true,
            "is_verified": true,
            "avatar": false
        }
    """

    api_access_provider.check_api_key(api_key)
    return await users_use_case.update_user(user_id, user_info)
