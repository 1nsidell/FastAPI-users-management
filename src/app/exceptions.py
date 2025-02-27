"""Custom infrastructure exceptions."""

from src.core.exceptions import BaseCustomException


class CustomDBException(BaseCustomException):
    """Base class for all custom exception databases."""

    error_type = "DATABASE_ERROR"
    status_code = None


class RepositoryException(CustomDBException):
    """SQL repository working error."""

    error_type = "REPOSITORY_ERROR"
    status_code = 500

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class RedisDBException(CustomDBException):
    """Redis working error."""

    error_type = "REDIS_ERROR"
    status_code = 500

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
