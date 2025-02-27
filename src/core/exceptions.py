"""Custom domain exceptions."""


class BaseCustomException(Exception):
    """Base class for all custom exceptions."""

    error_type: str = "APPLICATION_ERROR"
    status_code: int = 500

    def __init__(self, message: str = None):
        self.message = message or self.__doc__
        super().__init__(self.message)


class SecurityException(BaseCustomException):
    """Base class for all API security related exceptions."""

    error_type: str = "SECURITY_ERROR"
    status_code: int = None

    def __init__(self, message: str = None):
        self.message = message or self.__doc__
        super().__init__(self.message)


class CustomUserException(BaseCustomException):
    """Base class for all user-related errors."""

    error_type = "USER_ERROR"
    status_code = None


class CustomAccessDeniedException(SecurityException):
    """API key rejected."""

    error_type: str = "API_KEY_ERROR"
    status_code: int = 403

    def __init__(self, message: str = None):
        self.message = message or self.__doc__
        super().__init__(self.message)


class UserNotFoundException(CustomUserException):
    """User not found."""

    error_type: str = "USER_NOT_FOUND"
    status_code: int = 404

    def __init__(self, message: str = None):
        self.message = message or self.__doc__
        super().__init__(self.message)
