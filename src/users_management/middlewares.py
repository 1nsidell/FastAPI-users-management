"""
Main module for middleware application.
"""

from fastapi import FastAPI

from users_management.core.middlewares.logger_middleware import (
    RequestLoggingMiddleware,
)

middlewares = [RequestLoggingMiddleware]


def apply_middlewares(app: FastAPI) -> FastAPI:
    """
    Applying middleware.
    """
    for middleware in middlewares:
        app.add_middleware(middleware)
    return app
