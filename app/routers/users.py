# Built by AbilitySoft | abilitysoft.net
"""
Users router — CRUD endpoints for user management.

All endpoints require authentication. Some endpoints (create, update,
delete) are restricted to admin users via role-based access control.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import RoleChecker, get_current_active_user
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.common import MessageResponse, PaginatedResponse
from app.schemas.user import (
    UserCreate,
    UserListParams,
    UserResponse,
    UserUpdate,
)
from app.services.user import UserService
from typing import Optional

router = APIRouter(prefix="/users", tags=["Users"])

# ── Role checkers ─────────────────────────────────────────────────
admin_only = RoleChecker(["admin"])
admin_or_user = RoleChecker(["admin", "user"])


def _get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    """
    Factory dependency that creates a UserService for the current request.

    Args:
        db: The async database session.

    Returns:
        A ``UserService`` instance.
    """
    return UserService(UserRepository(db))


# ── Endpoints ─────────────────────────────────────────────────────


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
    description="Returns the profile of the currently authenticated user.",
)
async def get_me(
    current_user: User = Depends(get_current_active_user),
) -> UserResponse:
    """
    Return the profile of the currently authenticated user.

    Args:
        current_user: The authenticated user (injected).

    Returns:
        The user's profile as a ``UserResponse``.
    """
    return UserResponse.model_validate(current_user)


@router.get(
    "",
    response_model=PaginatedResponse[UserResponse],
    summary="List all users",
    description="Paginated list of users with optional filtering and sorting. Admin only.",
    dependencies=[Depends(admin_only)],
)
async def list_users(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by email or name"),
    role: Optional[str] = Query(None, description="Filter by role"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    sort_by: str = Query("created_at", description="Sort column"),
    sort_order: str = Query("desc", regex=r"^(asc|desc)$", description="Sort direction"),
    user_service: UserService = Depends(_get_user_service),
) -> PaginatedResponse[UserResponse]:
    """
    List users with pagination, filtering, and sorting.

    Args:
        page: Page number (1-indexed).
        page_size: Number of results per page.
        search: Free-text search on email, first_name, last_name.
        role: Filter by exact role.
        is_active: Filter by active status.
        sort_by: Column to sort by.
        sort_order: ``"asc"`` or ``"desc"``.
        user_service: Injected user service.

    Returns:
        A paginated response of ``UserResponse`` objects.
    """
    params = UserListParams(
        page=page,
        page_size=page_size,
        search=search,
        role=role,
        is_active=is_active,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return await user_service.list_users(params)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="Retrieve a single user by their database ID. Admin only.",
    dependencies=[Depends(admin_only)],
)
async def get_user(
    user_id: int,
    user_service: UserService = Depends(_get_user_service),
) -> UserResponse:
    """
    Get a single user by ID.

    Args:
        user_id: The user's database ID.
        user_service: Injected user service.

    Returns:
        The user's profile as a ``UserResponse``.
    """
    return await user_service.get_user(user_id)


@router.post(
    "",
    response_model=UserResponse,
    status_code=201,
    summary="Create a new user",
    description="Admin endpoint to create a new user with a specified role.",
    dependencies=[Depends(admin_only)],
)
async def create_user(
    payload: UserCreate,
    user_service: UserService = Depends(_get_user_service),
) -> UserResponse:
    """
    Create a new user (admin only).

    Args:
        payload: The user creation data.
        user_service: Injected user service.

    Returns:
        The newly created user as a ``UserResponse``.
    """
    return await user_service.create_user(payload)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update a user",
    description="Partially update a user's profile. Admin only.",
    dependencies=[Depends(admin_only)],
)
async def update_user(
    user_id: int,
    payload: UserUpdate,
    user_service: UserService = Depends(_get_user_service),
) -> UserResponse:
    """
    Partially update a user by ID (admin only).

    Args:
        user_id: The user's database ID.
        payload: The fields to update.
        user_service: Injected user service.

    Returns:
        The updated user as a ``UserResponse``.
    """
    return await user_service.update_user(user_id, payload)


@router.delete(
    "/{user_id}",
    response_model=MessageResponse,
    summary="Delete a user",
    description="Permanently delete a user from the database. Admin only.",
    dependencies=[Depends(admin_only)],
)
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(_get_user_service),
) -> MessageResponse:
    """
    Delete a user by ID (admin only).

    Args:
        user_id: The user's database ID.
        user_service: Injected user service.

    Returns:
        A confirmation message.
    """
    await user_service.delete_user(user_id)
    return MessageResponse(message=f"User {user_id} deleted successfully")
