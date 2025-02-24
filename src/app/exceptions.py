from src.core.exceptions import BaseCustomException, SecurityException


class CustomUserException(BaseCustomException):
    """Base class for all user-related errors."""

    error_type = "USER_ERROR"
    status_code = None


class CustomDBException(BaseCustomException):
    """Base class for all custom exception databases."""

    error_type = "DATABASE_ERROR"
    status_code = None


class CustomAccessDeniedException(SecurityException):
    """API key rejected."""

    error_type: str = "API_KEY_ERROR"
    status_code: int = 403

    def __init__(self, message: str = None):
        self.message = message or self.__doc__
        super().__init__(self.message)


class RepositoryException(CustomDBException):
    """Repository working error."""

    error_type = "REPOSITORY_ERROR"
    status_code = 500

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class RedisDBException(CustomDBException):
    """Redis operation error."""

    error_type = "REDIS_ERROR"
    status_code = 500

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class UserNotFoundException(CustomUserException):
    """User not found."""

    error_type: str = "USER_NOT_FOUND"
    status_code: int = 404

    def __init__(self, message: str = None):
        self.message = message or self.__doc__
        super().__init__(self.message)
