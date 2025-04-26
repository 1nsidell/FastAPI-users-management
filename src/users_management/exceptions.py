import json
import logging
from typing import Any, Awaitable, Callable, Dict, List

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from users_management.core.exceptions import BaseCustomException
from users_management.core.settings import settings


log: logging.Logger = logging.getLogger("ExceptionsLogger")

# Type alias for handler returning a string
BodyHandler = Callable[[Request, List[str]], Awaitable[str]]


async def _handle_json(request: Request, parts: List[str]) -> str:
    body = await request.json()
    parts.append(f"JSON={json.dumps(body)}")
    return _join(parts)


async def _handle_multipart(request: Request, parts: List[str]) -> str:
    data = await request.form()
    files: Dict[str, Dict[str, Any]] = {}
    fields: Dict[str, str] = {}
    for k, v in data.items():
        filename = getattr(v, "filename", None)
        if filename:
            files[k] = {"name": filename, "size": getattr(v, "size", 0)}
        else:
            fields[k] = str(v)
    if files:
        parts.append(f"FILES={json.dumps(files)}")
    if fields:
        parts.append(f"FIELDS={json.dumps(fields)}")
    return _join(parts)


async def _handle_urlencoded(request: Request, parts: List[str]) -> str:
    data = await request.form()
    parts.append(f"FORM={json.dumps(dict(data))}")
    return _join(parts)


async def _handle_text(request: Request, parts: List[str]) -> str:
    raw = await request.body()
    text = raw.decode(errors="replace")[:5000]
    parts.append(f"TEXT={json.dumps(text)}")
    return _join(parts)


async def _handle_default(request: Request, parts: List[str]) -> str:
    raw = await request.body()
    if raw:
        parts.append(f"BINARY_SIZE={len(raw)}")
    return _join(parts)


async def read_request_body(request: Request) -> str:
    """Read and parse request data into log-friendly format"""
    if request.method in {"GET", "HEAD", "OPTIONS", "DELETE"}:
        return "EMPTY_REQUEST"

    parts: List[str] = []
    # Query params
    qp: Dict[str, Any] = dict(request.query_params)
    if qp:
        parts.append(f"QUERY={json.dumps(qp)}")

    # Content-type based dispatch
    ctype = request.headers.get("Content-Type", "").split(";")[0].strip()
    handlers: Dict[str, BodyHandler] = {
        "application/json": _handle_json,
        "multipart/form-data": _handle_multipart,
        "application/x-www-form-urlencoded": _handle_urlencoded,
    }
    try:
        if handler := handlers.get(ctype):
            return await handler(request, parts)
        if ctype.startswith("text/"):
            return await _handle_text(request, parts)
        return await _handle_default(request, parts)
    except Exception as e:
        parts.append(f"BODY_PARSE_ERROR={e!s}")
        return _join(parts)


def _join(parts: List[str]) -> str:
    return " | ".join(parts) if parts else "EMPTY_REQUEST"


async def handle_exception(
    request: Request,
    exc: Exception,
    error_type: str,
    status_code: int,
    message: str,
) -> JSONResponse:
    body_data = await read_request_body(request)
    error_data = {"error_type": error_type, "message": message}

    log.error(
        "Request ID: %s | Method: %s | Path: %s | Status: %s | Client: %s | "
        "ReqBody: %s | RespBody: %s",  # log format simplified
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


async def custom_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Handle custom business exceptions."""
    if not isinstance(exc, BaseCustomException):
        return await generic_exception_handler(request, exc)
    return await handle_exception(
        request,
        exc,
        getattr(exc, "error_type", "UNKNOWN_ERROR"),
        getattr(exc, "status_code", 500),
        str(exc) if settings.mode != "PROD" else exc.__doc__ or "",
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Handle unexpected exceptions."""
    return await handle_exception(
        request,
        exc,
        "INTERNAL_SERVER_ERROR",
        500,
        str(exc) if settings.mode != "PROD" else "Internal server error",
    )


def apply_exceptions_handlers(app: FastAPI) -> FastAPI:
    """Register exception handlers."""
    app.add_exception_handler(BaseCustomException, custom_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
    return app
