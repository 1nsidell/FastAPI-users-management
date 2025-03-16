import logging
from functools import wraps
from typing import Tuple, Type, Union

from redis.exceptions import RedisError
from sqlalchemy.exc import SQLAlchemyError

from users_management.app.exceptions import (
    RedisCacheDBException,
    SQLRepositoryException,
)

log = logging.getLogger("exception_handler")


def handle_repository_exceptions(
    specific_exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]],
    custom_exception: Type[Exception],
    log_message: str,
):
    """
    Universal decorator for handling repository exceptions.

    Args:
        specific_exceptions: One or more exception types to catch (e.g., SQLAlchemyError, RedisError).
        custom_exception: Custom exception to raise (e.g., SQLRepositoryException).
        log_message: Message to log when an exception occurs.
    """

    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except specific_exceptions as e:
                log.error(
                    "%s in %s with args %s, kwargs %s: %s",
                    log_message,
                    func.__name__,
                    args,
                    kwargs,
                    str(e),
                    exc_info=True,
                )
                raise custom_exception(str(e))

        return async_wrapper

    return decorator


handle_sql_exceptions = handle_repository_exceptions(
    SQLAlchemyError, SQLRepositoryException, "SQL Database error."
)
handle_redis_exceptions = handle_repository_exceptions(
    RedisError, RedisCacheDBException, "Redis error."
)
