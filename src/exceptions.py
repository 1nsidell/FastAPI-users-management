"""Error Handler Module."""

import logging
from typing import Union
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.app.exceptions import BaseCustomInfrastructureException
from src.core.exceptions import BaseCustomDomainException
from src.settings import settings

log = logging.getLogger("exception_handler")


def structured_exception_handler(
    request: Request,
    exc: Union[BaseCustomInfrastructureException, BaseCustomDomainException],
) -> JSONResponse:
    """Custom exception handler."""
    error_data = {
        "error_type": getattr(exc, "error_type", "UNKNOWN_ERROR"),
        "message": (str(exc) if settings.mode != "PROD" else exc.__doc__),
        "error_code": getattr(exc, "status_code", 500),
    }
    log.error(
        "Request ID: %s. Error context: %s",
        request.headers.get("X-Request-ID"),
        error_data,
    )
    return JSONResponse(
        content=error_data, status_code=error_data["error_code"]
    )


def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Unexpected exception handler."""
    error_data = {
        "error_type": "INTERNAL_SERVER_ERROR",
        "message": (
            str(exc) if settings.mode != "PROD" else "Internal server error"
        ),
        "error_code": 500,
    }

    log.error(
        "Request ID: %s. Error context: %s",
        request.headers.get("X-Request-ID"),
        error_data,
    )

    return JSONResponse(content=error_data, status_code=500)


def apply_exceptions_handlers(app: FastAPI) -> FastAPI:
    """Registration of error handlers."""

    app.add_exception_handler(
        BaseCustomInfrastructureException, structured_exception_handler
    )
    app.add_exception_handler(
        BaseCustomDomainException, structured_exception_handler
    )
    app.add_exception_handler(Exception, general_exception_handler)

    return app
