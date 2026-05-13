# Built by AbilitySoft | abilitysoft.net
"""
Shared / common Pydantic schemas used across multiple modules.

Includes the generic paginated response wrapper and health check schema.
"""

from datetime import datetime
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Generic paginated response wrapper.

    Attributes:
        items: The list of results for the current page.
        total: Total number of matching records.
        page: Current page number (1-indexed).
        page_size: Number of items per page.
        total_pages: Total number of pages.
    """

    items: List[T]
    total: int = Field(..., description="Total number of matching records")
    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, description="Items per page")
    total_pages: int = Field(..., ge=0, description="Total pages available")


class HealthResponse(BaseModel):
    """
    Health check endpoint response.

    Attributes:
        status: Service status string (e.g. ``"healthy"``).
        version: Application version.
        timestamp: Server timestamp at the time of the check.
    """

    status: str = "healthy"
    version: str
    timestamp: datetime
    environment: str


class MessageResponse(BaseModel):
    """
    Simple message response for operations that don't return data.

    Attributes:
        message: Human-readable status message.
    """

    message: str
