import time
from typing import Callable

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import get_logger, log_request

logger = get_logger("middleware.logging")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.perf_counter()

        request_id = request.headers.get("X-Request-ID", "")

        response = await call_next(request)

        duration_ms = (time.perf_counter() - start_time) * 1000

        log_request(
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=duration_ms,
            extra={
                "request_id": request_id,
                "query_params": str(request.query_params) if request.query_params else None,
                "client_ip": request.client.host if request.client else None,
            },
        )

        return response


def setup_logging_middleware(app: FastAPI) -> None:
    app.add_middleware(RequestLoggingMiddleware)
