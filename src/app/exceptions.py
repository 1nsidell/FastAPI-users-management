"""Custom infrastructure exceptions."""


class BaseCustomInfrastructureException(Exception):
    """Base class for all custom exceptions."""

    error_type: str
    status_code: int
    message: str


class CustomDBException(BaseCustomInfrastructureException):
    """Base class for all custom exception databases."""

    error_type: str
    status_code: int
    message: str


class RepositoryException(CustomDBException):
    """SQL repository working error."""

    error_type = "SQL_REPOSITORY_ERROR"
    status_code = 500

    def __init__(self, message: str):
        self.message = message or self.__doc__


class RedisDBException(CustomDBException):
    """Redis working error."""

    error_type = "REDIS_ERROR"
    status_code = 500

    def __init__(self, message: str):
        self.message = message or self.__doc__


class TransactionException(CustomDBException):
    """Transaction error."""

    error_type = "TRANSACTION_ERROR"
    status_code = 500

    def __init__(self, message: str):
        self.message = message or self.__doc__
