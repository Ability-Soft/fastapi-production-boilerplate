# Built by AbilitySoft | abilitysoft.net
"""
FastAPI application factory.

Creates the FastAPI instance, registers routers, middleware,
exception handlers, and lifecycle events.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.core.logging_config import get_logger, setup_logging
from app.core.middleware import register_middleware
from app.routers import auth, health, users

settings = get_settings()

# Initialise logging before anything else
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan handler.

    Runs startup logic before yielding, and shutdown logic after.
    """
    logger.info(
        "🚀 Starting %s v%s [%s]",
        settings.APP_NAME,
        settings.APP_VERSION,
        settings.ENVIRONMENT,
    )
    yield
    logger.info("👋 Shutting down %s", settings.APP_NAME)


def create_app() -> FastAPI:
    """
    Build and configure the FastAPI application instance.

    Returns:
        A fully configured ``FastAPI`` application.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=settings.APP_DESCRIPTION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # ── Middleware ─────────────────────────────────────────────
    register_middleware(app)

    # ── Exception handlers ────────────────────────────────────
    register_exception_handlers(app)

    # ── Routers ───────────────────────────────────────────────
    api_prefix = "/api/v1"
    app.include_router(health.router, prefix=api_prefix)
    app.include_router(auth.router, prefix=api_prefix)
    app.include_router(users.router, prefix=api_prefix)

    logger.info("Application initialised — routes registered under %s", api_prefix)
    return app


# The application instance used by Uvicorn
app = create_app()
