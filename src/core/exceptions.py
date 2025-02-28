"""Custom domain exceptions."""


class BaseCustomDomainException(Exception):
    """Base class for all custom exceptions."""

    error_type: str
    status_code: int
    message: str


class CustomSecurityException(BaseCustomDomainException):
    """Base class for all API security related exceptions."""

    error_type: str
    status_code: int
    message: str


class CustomUserException(BaseCustomDomainException):
    """Base class for all user-related errors."""

    error_type: str
    status_code: int
    message: str


class CustomAccessDeniedException(CustomSecurityException):
    """API key rejected."""

    error_type: str = "API_KEY_ERROR"
    status_code: int = 403

    def __init__(self, message: str = None):
        self.message = message or self.__doc__


class UserNotFoundException(CustomUserException):
    """User not found."""

    error_type: str = "USER_NOT_FOUND"
    status_code: int = 404

    def __init__(self, message: str = None):
        self.message = message or self.__doc__
