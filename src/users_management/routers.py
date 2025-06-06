"""
Main module for application roots.
"""

from fastapi import FastAPI

from users_management.api.http.root_router import root_router


def apply_routes(app: FastAPI) -> FastAPI:
    """
    Applying application roots.
    """
    app.include_router(root_router)
    return app
