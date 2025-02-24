from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.core.loggers import setup_logging
from src.middlewares import apply_middlewares


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Предварительная инициализация приложения.
    """
    # startup
    setup_logging()
    yield
    # shutdown


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        docs_url="/docs",
        openapi_url="/docs.json",
    )
    return apply_middlewares(app)
