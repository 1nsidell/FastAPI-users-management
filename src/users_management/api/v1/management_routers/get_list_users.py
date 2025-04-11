from typing import List

from fastapi import APIRouter, Header, Query, status

from users_management.app.depends import APIAccessProvider, UsersUseCase
from users_management.app.schemas.users import SInfoUser
from users_management.core.schemas import SErrorResponse
from users_management.settings import settings

router = APIRouter()


@router.get(
    settings.api.users,
    response_model=List[SInfoUser],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "model": SErrorResponse,
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
            "model": SErrorResponse,
            "description": "Users not found",
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
            "model": SErrorResponse,
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
async def get_list_user(
    api_access_provider: APIAccessProvider,
    users_use_case: UsersUseCase,
    users_id: List[int] = Query(...),
    api_key: str = Header(..., alias="X-API-Key"),
) -> List[SInfoUser]:
    """Get information about multiple users by their IDs.

    Args:
        users_id (List[int]): List of user IDs to retrieve information for
        api_key (str): API key for authentication (passed in X-API-Key header)

    Returns:
        List[SInfoUser]: List of user information objects containing:
            - user_id (int): User's unique identifier
            - nickname (str): User's nickname
            - is_active (bool): User's active status
            - is_verified (bool): User's verification status
            - avatar (bool): User's avatar status

    Example Request:
        GET /api/users-management/v1/users?users_id=1&users_id=2&users_id=3
        Headers:
            X-API-Key: your-api-key

    Example Success Response:
        Status: 200 OK
        Body: [
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
    """
    api_access_provider.check_api_key(api_key)
    return await users_use_case.get_list_users_by_id(users_id)
