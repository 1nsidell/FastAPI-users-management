from fastapi import APIRouter, Header, status

from users_management.app.depends import APIAccessProvider, UsersUseCase
from users_management.app.schemas.requests import CreateUserRequest
from users_management.app.schemas.responses import ErrorResponse
from users_management.app.schemas.users import SInfoUser
from users_management.settings import settings

router = APIRouter()


@router.post(
    settings.api.users,
    response_model=SInfoUser,
    status_code=status.HTTP_201_CREATED,
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
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse,
            "description": "Username conflict",
            "content": {
                "application/json": {
                    "example": {
                        "error_type": "USERNAME_ALREADY_EXIST",
                        "message": "A user with this name already exists.",
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
async def create_user(
    api_access_provider: APIAccessProvider,
    users_use_case: UsersUseCase,
    user_info: CreateUserRequest,
    api_key: str = Header(..., alias="X-API-Key"),
) -> SInfoUser:
    """Create a new user in the system.

    Args:
        user_info (CreateUserRequest): User information with required fields:
            - user_id (PositiveInt): Unique user identifier
            - nickname (str): Unique user nickname
        api_key (str): API key for authentication (passed in X-API-Key header)

    Returns:
        SInfoUser: Created user information containing:
            - user_id (int): User's unique identifier
            - nickname (str): User's nickname
            - is_active (bool): User's active status (default: True)
            - is_verified (bool): User's verification status (default: False)
            - avatar (bool): User's avatar status (default: False)

    Example Request:
        POST /api/users-management/v1/users
        Headers:
            X-API-Key: your-api-key
        Body:
            {
                "user_id": 123,
                "nickname": "john_doe"
            }

    Example Success Response:
        Status: 201 Created
        Body:
            {
                "user_id": 123,
                "nickname": "john_doe",
                "is_active": true,
                "is_verified": false,
                "avatar": false
            }
    """

    api_access_provider.check_api_key(api_key)
    return await users_use_case.create_user(user_info)
