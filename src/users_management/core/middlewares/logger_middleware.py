"""Middleware for response/request logging."""

import logging

from fastapi import Request
from starlette.background import BackgroundTask
from starlette.middleware.base import BaseHTTPMiddleware

log = logging.getLogger("requests")


def log_info(
    request_id: str,
    method: str,
    endpoint: str,
    status_code: int,
    client_ip: str,
):
    log.info(
        "Request ID: %s. Method: %s. Endpoint: %s. Status: %s. Client IP: %s",
        request_id,
        method,
        endpoint,
        status_code,
        client_ip,
    )


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        method = request.method
        endpoint = request.url.path
        client_ip = request.client.host

        response = await call_next(request)

        task = BackgroundTask(
            log_info,
            request.headers.get("X-Request-ID"),
            method,
            endpoint,
            response.status_code,
            client_ip,
        )

        response.background = task
        return response
