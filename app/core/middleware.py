# Built by AbilitySoft | abilitysoft.net
"""
Application middleware stack.

Includes request timing, request-ID propagation, and CORS setup.
All middleware is registered once via ``register_middleware()``.
"""

import time
import uuid
from typing import Callable

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import get_settings
from app.core.logging_config import get_logger

logger = get_logger(__name__)
settings = get_settings()


class RequestTimingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that logs the duration of every HTTP request.

    Adds an ``X-Process-Time`` response header and logs the request
    method, path, status code, and duration.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process a request and record its execution time.

        Args:
            request: The incoming HTTP request.
            call_next: The next middleware or route handler.

        Returns:
            The HTTP response with an ``X-Process-Time`` header.
        """
        start_time = time.perf_counter()
        response: Response = await call_next(request)
        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

        response.headers["X-Process-Time"] = f"{duration_ms}ms"

        logger.info(
            "%s %s → %s (%.2fms)",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware that assigns a unique request ID to every request.

    The ID is returned in the ``X-Request-ID`` response header and can
    be used for distributed tracing.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Inject a unique request ID.

        Args:
            request: The incoming HTTP request.
            call_next: The next middleware or route handler.

        Returns:
            The HTTP response with an ``X-Request-ID`` header.
        """
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id

        response: Response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


def register_middleware(app: FastAPI) -> None:
    """
    Register all middleware on the FastAPI application.

    Order matters — middleware added last is executed first.

    Args:
        app: The FastAPI application instance.
    """
    # CORS — must be added via FastAPI helper for correct preflight handling
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )

    # Custom middleware
    app.add_middleware(RequestTimingMiddleware)
    app.add_middleware(RequestIDMiddleware)
