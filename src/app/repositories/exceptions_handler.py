import logging
from functools import wraps

from redis.exceptions import RedisError
from sqlalchemy.exc import SQLAlchemyError

from src.app.exceptions import RedisDBException, RepositoryException

log = logging.getLogger("repositories")


def handle_repository_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except (TypeError, ValueError) as e:
            log.warning("Error when working with database: %s.", e)
            raise RepositoryException(e)
        except SQLAlchemyError as e:
            log.exception("Error when working with database: %s.", e)
            raise RepositoryException(e)
        except Exception as e:
            log.exception("!Critical error when working with database: %s.", e)
            raise RepositoryException(e)

    return wrapper


def handle_redis_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except RedisError as e:
            log.exception("Error when working with Redis: %s.", e)
            raise RedisDBException(e)
        except Exception as e:
            log.exception("!Critical error when working with Redis: %s.", e)
            raise RedisDBException(e)

    return wrapper
