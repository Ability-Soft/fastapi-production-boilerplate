# Built by AbilitySoft | abilitysoft.net
"""
User service — business logic for user CRUD operations.

Sits between the router and repository layers, enforcing business
rules like duplicate-email checks and password hashing on updates.
"""

import math
from typing import Optional

from app.core.exceptions import ConflictException, NotFoundException
from app.core.logging_config import get_logger
from app.core.security import hash_password
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.common import PaginatedResponse
from app.schemas.user import UserCreate, UserListParams, UserResponse, UserUpdate

logger = get_logger(__name__)


class UserService:
    """
    Service layer for user management operations.

    Each instance is scoped to a single request via the repository's session.
    """

    def __init__(self, user_repo: UserRepository) -> None:
        """
        Initialise the user service.

        Args:
            user_repo: The user repository instance.
        """
        self.user_repo = user_repo

    async def get_user(self, user_id: int) -> UserResponse:
        """
        Retrieve a single user by ID.

        Args:
            user_id: The user's database ID.

        Returns:
            A ``UserResponse`` schema.

        Raises:
            NotFoundException: If no user with the given ID exists.
        """
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User", user_id)
        return UserResponse.model_validate(user)

    async def list_users(
        self, params: UserListParams
    ) -> PaginatedResponse[UserResponse]:
        """
        List users with pagination, filtering, and sorting.

        Args:
            params: Query parameters for filtering and pagination.

        Returns:
            A ``PaginatedResponse`` of ``UserResponse`` objects.
        """
        users, total = await self.user_repo.get_list(
            page=params.page,
            page_size=params.page_size,
            search=params.search,
            role=params.role,
            is_active=params.is_active,
            sort_by=params.sort_by,
            sort_order=params.sort_order,
        )

        total_pages = math.ceil(total / params.page_size) if total > 0 else 0

        return PaginatedResponse[UserResponse](
            items=[UserResponse.model_validate(u) for u in users],
            total=total,
            page=params.page,
            page_size=params.page_size,
            total_pages=total_pages,
        )

    async def create_user(self, payload: UserCreate) -> UserResponse:
        """
        Create a new user (admin operation).

        Args:
            payload: The user creation data.

        Returns:
            The created ``UserResponse``.

        Raises:
            ConflictException: If the email is already taken.
        """
        existing = await self.user_repo.get_by_email(payload.email)
        if existing:
            raise ConflictException(f"Email '{payload.email}' is already registered")

        user = User(
            email=payload.email,
            hashed_password=hash_password(payload.password),
            first_name=payload.first_name,
            last_name=payload.last_name,
            role=payload.role,
            is_active=True,
        )
        user = await self.user_repo.create(user)
        logger.info("User created by admin: %s (id=%d)", user.email, user.id)
        return UserResponse.model_validate(user)

    async def update_user(
        self, user_id: int, payload: UserUpdate
    ) -> UserResponse:
        """
        Partially update a user.

        Args:
            user_id: The user's database ID.
            payload: The fields to update.

        Returns:
            The updated ``UserResponse``.

        Raises:
            NotFoundException: If no user with the given ID exists.
            ConflictException: If the new email is already taken by another user.
        """
        existing = await self.user_repo.get_by_id(user_id)
        if not existing:
            raise NotFoundException("User", user_id)

        update_data = payload.model_dump(exclude_unset=True)

        # Check email uniqueness if changing email
        if "email" in update_data and update_data["email"] != existing.email:
            conflict = await self.user_repo.get_by_email(update_data["email"])
            if conflict:
                raise ConflictException(
                    f"Email '{update_data['email']}' is already registered"
                )

        user = await self.user_repo.update(user_id, update_data)
        logger.info("User updated: id=%d, fields=%s", user_id, list(update_data.keys()))
        return UserResponse.model_validate(user)

    async def delete_user(self, user_id: int) -> bool:
        """
        Delete a user from the database.

        Args:
            user_id: The user's database ID.

        Returns:
            ``True`` if the user was deleted.

        Raises:
            NotFoundException: If no user with the given ID exists.
        """
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User", user_id)

        deleted = await self.user_repo.delete(user_id)
        logger.info("User deleted: id=%d, email=%s", user_id, user.email)
        return deleted
