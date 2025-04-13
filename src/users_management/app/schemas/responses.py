from users_management.core.schemas.base import BaseSchema


class SuccessResponse(BaseSchema):
    """Scheme for a successful response."""

    message: str = "success"


class ErrorResponse(BaseSchema):
    """Error response scheme."""

    error_type: str
    message: str


# Common response patterns
SQL_ERROR = {
    "summary": "Database error",
    "value": {
        "error_type": "SQL_REPOSITORY_ERROR",
        "message": "SQL repository working error.",
    },
}

REDIS_ERROR = {
    "summary": "Cache error",
    "value": {
        "error_type": "REDIS_ERROR",
        "message": "Cache operation failed.",
    },
}

REDIS_CONNECTION_ERROR = {
    "summary": "Redis connection error",
    "value": {
        "error_type": "REDIS_ERROR",
        "message": "Redis connection error.",
    },
}

REDIS_PING_ERROR = {
    "summary": "Redis ping failed",
    "value": {
        "error_type": "REDIS_ERROR",
        "message": "Redis ping failed.",
    },
}

# Complete response definitions
API_KEY_ERROR = {
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
}

USER_NOT_FOUND = {
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
}

USERNAME_CONFLICT = {
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
}

DATA_NOT_TRANSMITTED = {
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
}

INTERNAL_SERVER_ERROR = {
    "model": ErrorResponse,
    "description": "Internal server error",
    "content": {
        "application/json": {
            "examples": {
                "sql_error": SQL_ERROR,
                "cache_error": REDIS_ERROR,
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
}

SERVICE_UNAVAILABLE = {
    "model": ErrorResponse,
    "description": "Service dependencies are not ready",
    "content": {
        "application/json": {
            "examples": {
                "redis_error": REDIS_CONNECTION_ERROR,
                "redis_ping_error": REDIS_PING_ERROR,
                "sql_error": SQL_ERROR,
            }
        }
    },
}
