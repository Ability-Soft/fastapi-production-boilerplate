# Built by AbilitySoft | abilitysoft.net
"""
User Pydantic schemas for request validation and response serialisation.

Follows the pattern of separate schemas for creation, update, database
representation, and API response to keep concerns cleanly separated.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """
    Shared base fields for user schemas.

    Attributes:
        email: The user's email address.
        first_name: First name.
        last_name: Last name.
    """

    email: EmailStr = Field(..., description="User email address")
    first_name: str = Field(..., min_length=1, max_length=100, description="First name")
    last_name: str = Field(..., min_length=1, max_length=100, description="Last name")


class UserCreate(UserBase):
    """
    Schema for creating a new user (admin endpoint).

    Extends ``UserBase`` with password and optional role assignment.
    """

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Password (8-128 characters)",
    )
    role: str = Field(
        default="user",
        description="User role: 'user' or 'admin'",
        pattern=r"^(user|admin)$",
    )


class UserUpdate(BaseModel):
    """
    Schema for partial user updates.

    All fields are optional — only provided fields are updated.
    """

    email: Optional[EmailStr] = Field(None, description="New email address")
    first_name: Optional[str] = Field(
        None, min_length=1, max_length=100, description="New first name"
    )
    last_name: Optional[str] = Field(
        None, min_length=1, max_length=100, description="New last name"
    )
    role: Optional[str] = Field(
        None,
        description="New role ('user' or 'admin')",
        pattern=r"^(user|admin)$",
    )
    is_active: Optional[bool] = Field(None, description="Account active status")


class UserResponse(BaseModel):
    """
    Schema for returning user data in API responses.

    Excludes sensitive fields like ``hashed_password``.
    """

    id: int
    email: EmailStr
    first_name: str
    last_name: str
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class UserListParams(BaseModel):
    """
    Query parameters for listing / filtering users.

    Attributes:
        page: Page number (1-indexed).
        page_size: Number of results per page.
        search: Free-text search on email, first_name, last_name.
        role: Filter by role.
        is_active: Filter by active status.
        sort_by: Column to sort by.
        sort_order: ``asc`` or ``desc``.
    """

    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=20, ge=1, le=100, description="Items per page")
    search: Optional[str] = Field(None, description="Search term (email, name)")
    role: Optional[str] = Field(None, description="Filter by role")
    is_active: Optional[bool] = Field(None, description="Filter by active status")
    sort_by: str = Field(default="created_at", description="Sort column")
    sort_order: str = Field(
        default="desc",
        description="Sort direction",
        pattern=r"^(asc|desc)$",
    )
