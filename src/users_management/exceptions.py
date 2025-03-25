"""
Custom Exception Handlers for FastAPI Application
"""

import json
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from users_management.core.exceptions import BaseCustomException
from users_management.settings import settings

log = logging.getLogger("ExceptionsLogger")


async def read_request_body(request: Request) -> str:
    """Read and parse request data into log-friendly format"""
    try:
        log_parts = []
        query_params = dict(request.query_params)

        # Add query params
        if query_params:
            log_parts.append(f"QUERY={json.dumps(query_params)}")

        # Process body only for methods that support it
        if request.method not in {"GET", "HEAD", "OPTIONS", "DELETE"}:
            content_type = (
                request.headers.get("Content-Type", "").split(";")[0].strip()
            )

            try:
                if content_type == "application/json":
                    body = await request.json()
                    log_parts.append(f"JSON={json.dumps(body)}")

                elif content_type == "multipart/form-data":
                    form_data = await request.form()
                    files = {
                        k: {"name": v.filename, "size": v.size}
                        for k, v in form_data.items()
                        if v.filename
                    }
                    fields = {
                        k: str(v)
                        for k, v in form_data.items()
                        if not v.filename
                    }
                    if files:
                        log_parts.append(f"FILES={json.dumps(files)}")
                    if fields:
                        log_parts.append(f"FIELDS={json.dumps(fields)}")

                elif content_type == "application/x-www-form-urlencoded":
                    form_data = await request.form()
                    log_parts.append(f"FORM={json.dumps(dict(form_data))}")

                elif content_type.startswith("text/"):
                    text = (await request.body()).decode(errors="replace")[
                        :5000
                    ]
                    log_parts.append(f"TEXT={json.dumps(text)}")

                else:
                    body = await request.body()
                    if body:
                        log_parts.append(f"BINARY_SIZE={len(body)}")
            except Exception as e:
                log_parts.append(f"BODY_PARSE_ERROR={e!s}")

        return " | ".join(log_parts) if log_parts else "EMPTY_REQUEST"

    except Exception as e:
        log.error("Request data read failed: %s", str(e))
        return f"ERROR={e!s}"


async def handle_exception(
    request: Request,
    exc: Exception,
    error_type: str,
    status_code: int,
    message: str,
) -> JSONResponse:
    """Base exception handling logic."""
    # Read request body
    body_data = await read_request_body(request)

    # Prepare error response
    error_data = {"error_type": error_type, "message": message}

    # Log error details
    log.error(
        "Request ID: %s | Method: %s | Endpoint: %s | Status: %s | Client IP: %s | "
        "Request Body: %s | Response Body: %s.",
        request.headers.get("X-Request-ID", "N/A"),
        request.method,
        request.url.path,
        status_code,
        request.client.host if request.client else "unknown",
        body_data,
        error_data,
        exc_info=True,
    )

    return JSONResponse(content=error_data, status_code=status_code)


async def custom_exception_handler(request: Request, exc: BaseCustomException):
    """Handle custom business exceptions."""
    return await handle_exception(
        request=request,
        exc=exc,
        error_type=getattr(exc, "error_type", "UNKNOWN_ERROR"),
        status_code=getattr(exc, "status_code", 500),
        message=str(exc) if settings.mode != "PROD" else exc.__doc__,
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """Handle all unexpected exceptions."""
    return await handle_exception(
        request=request,
        exc=exc,
        error_type="INTERNAL_SERVER_ERROR",
        status_code=500,
        message=(
            str(exc) if settings.mode != "PROD" else "Internal server error"
        ),
    )


def apply_exceptions_handlers(app: FastAPI) -> FastAPI:
    """Register exception handlers with the FastAPI application."""
    app.add_exception_handler(BaseCustomException, custom_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
    return app
