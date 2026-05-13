# Built by AbilitySoft | abilitysoft.net
"""
Health check router.

Provides a lightweight endpoint for load balancers, orchestrators,
and monitoring systems to verify the service is running.
"""

from datetime import datetime, timezone

from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.common import HealthResponse

settings = get_settings()

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Returns the current health status, version, and environment of the API.",
)
async def health_check() -> HealthResponse:
    """
    Perform a basic health check.

    Returns:
        A ``HealthResponse`` with the service status, version, and timestamp.
    """
    return HealthResponse(
        status="ok",
        version=settings.APP_VERSION,
        timestamp=datetime.now(timezone.utc),
        environment=settings.ENVIRONMENT,
    )
