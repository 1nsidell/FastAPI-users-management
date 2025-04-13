"""
Application initialization.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from users_management.core import setup_logging
from users_management.core.settings import settings
from users_management.exceptions import apply_exceptions_handlers
from users_management.gateways.depends import RedisManager, SQLDBHelper
from users_management.routers import apply_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Pre-initialization of the application.
    """
    # startup
    setup_logging(settings)
    SQLDBHelper.startup()
    RedisManager.startup()
    yield
    # shutdown
    await SQLDBHelper.shutdown()
    await RedisManager.shutdown()


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        docs_url="/docs",
        openapi_url="/docs.json",
    )
    return apply_exceptions_handlers(apply_routes(app))
