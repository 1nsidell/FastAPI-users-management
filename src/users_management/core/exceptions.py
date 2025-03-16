"""
Custom base exceptions.
"""


class BaseCustomException(Exception):
    """Base class for all custom exceptions."""

    error_type: str
    status_code: int
    message: str


class CustomRepositoriesException(BaseCustomException):
    """Base class for all custom exceptions databases."""

    pass


class CustomSecurityException(BaseCustomException):
    """Base class for all API security related exceptions."""

    pass


class CustomUsersException(BaseCustomException):
    """Base class for all user-related exceptions."""

    pass


class CustomDataException(BaseCustomException):
    """Base class for exceptions with data."""

    pass
