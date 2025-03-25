"""
Main module for middleware application.
"""

from fastapi import FastAPI

middlewares = []


def apply_middlewares(app: FastAPI) -> FastAPI:
    """
    Applying middleware.
    """
    for middleware in middlewares:
        app.add_middleware(middleware)
    return app
