from fastapi import APIRouter, Header, Path, status

from users_management.app.depends import APIAccessProvider, UsersUseCase
from users_management.app.schemas.responses import (
    ErrorResponse,
    SuccessResponse,
)
from users_management.settings import settings

router = APIRouter()


@router.get(
    f"{settings.api.nicknames}/{{nickname}}",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
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
            "description": "Username exists",
            "content": {
                "application/json": {
                    "example": {
                        "error_type": "USER_EXIST",
                        "message": "User already exist.",
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
async def exist_nickname(
    api_access_provider: APIAccessProvider,
    users_use_case: UsersUseCase,
    nickname: str = Path(...),
    api_key: str = Header(..., alias="X-API-Key"),
) -> SuccessResponse:
    """Check if a nickname is available in the system.

    Args:
        nickname (str): Nickname to check for availability
        api_key (str): API key for authentication (passed in X-API-Key header)

    Returns:
        SuccessResponse: Empty success response if nickname is available
            Response body: {"message": "success"}

    Example Request:
        GET /api/users-management/v1/nicknames/john_doe
        Headers:
            X-API-Key: your-api-key

    Example Success Response:
        Status: 200 OK
        Body: {"message": "success"}

    Note:
        - Returns 200 OK if the nickname is available
        - Returns 409 Conflict if the nickname is already taken
    """

    api_access_provider.check_api_key(api_key)
    await users_use_case.find_user_by_nickname(nickname)
    return SuccessResponse()
