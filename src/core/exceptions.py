"""Custom base exceptions."""

from typing import Optional


class BaseCustomException(Exception):
    """Base class for all custom exceptions."""

    error_type: str
    status_code: int
    message: str


class CustomRepositoriesException(BaseCustomException):
    """Base class for all custom exception databases."""

    error_type: str
    status_code: int
    message: str


class CustomSecurityException(BaseCustomException):
    """Base class for all API security related exceptions."""

    error_type: str
    status_code: int
    message: str


class CustomUsersException(BaseCustomException):
    """Base class for all user-related errors."""

    error_type: str
    status_code: int
    message: str
