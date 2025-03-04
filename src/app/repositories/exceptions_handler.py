import logging
from functools import wraps

from redis.exceptions import RedisError
from sqlalchemy.exc import SQLAlchemyError

from src.app.exceptions import RedisCacheDBException, RepositoryException


log = logging.getLogger("repositories")


def handle_repository_exceptions(
    specific_exception, custom_exception, log_message
):
    """Universal decorator for handling repository exceptions."""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except specific_exception as e:
                log.error(
                    "%s in %s with args %s, kwargs %s: %s",
                    log_message,
                    func.__name__,
                    args,
                    kwargs,
                    e,
                )
                raise custom_exception()

        return wrapper

    return decorator


handle_sql_exceptions = handle_repository_exceptions(
    SQLAlchemyError, RepositoryException, "SQL Database error"
)
handle_redis_exceptions = handle_repository_exceptions(
    RedisError, RedisCacheDBException, "Redis error"
)
