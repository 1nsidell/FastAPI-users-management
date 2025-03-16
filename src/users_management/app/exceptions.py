"""Custom application exceptions."""

from typing import Optional

from users_management.core.exceptions import (
    CustomDataException,
    CustomRepositoriesException,
    CustomSecurityException,
    CustomUsersException,
)


class SQLRepositoryException(CustomRepositoriesException):
    """SQL repository working error."""

    error_type = "SQL_REPOSITORY_ERROR"
    status_code = 500

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.__doc__
        super().__init__(self.message)


class RedisCacheDBException(CustomRepositoriesException):
    """Cache operation failed."""

    error_type = "REDIS_ERROR"
    status_code = 202

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.__doc__
        super().__init__(self.message)


class RedisHealthException(CustomRepositoriesException):
    """Redis connection error."""

    error_type = "REDIS_ERROR"
    status_code = 500

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.__doc__
        super().__init__(self.message)


class TransactionException(CustomRepositoriesException):
    """Transaction error."""

    error_type = "TRANSACTION_ERROR"
    status_code = 500

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.__doc__
        super().__init__(self.message)


class AccessDeniedException(CustomSecurityException):
    """API key rejected."""

    error_type: str = "API_KEY_ERROR"
    status_code: int = 403

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.__doc__
        super().__init__(self.message)


class UserNotFoundException(CustomUsersException):
    """User not found."""

    error_type: str = "USER_NOT_FOUND"
    status_code: int = 404

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.__doc__
        super().__init__(self.message)


class UserAlreadyExistException(CustomUsersException):
    """User already exist."""

    error_type: str = "USER_EXIST"
    status_code: int = 409

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.__doc__
        super().__init__(self.message)


class UserAlreadyExist_Nickname(CustomUsersException):
    """A user with this name already exists."""

    error_type = "USERNAME_ALREADY_EXIST"
    status_code = 409

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.__doc__
        super().__init__(self.message)


class DataNotTransmitted(CustomDataException):
    """The data was not transmitted."""

    error_type: str = "MISSING_DATA"
    status_code: int = 400

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.__doc__
        super().__init__(self.message)
