# Built by AbilitySoft | abilitysoft.net
"""
User repository — data access layer.

All direct database queries for the ``users`` table live here.
The service layer calls repository methods and never touches
SQLAlchemy queries directly.
"""

import math
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import func, or_, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    """
    Repository for ``User`` CRUD operations.

    Each instance is scoped to a single database session.
    """

    def __init__(self, db: AsyncSession) -> None:
        """
        Initialise the repository with an async session.

        Args:
            db: The SQLAlchemy async session.
        """
        self.db = db

    # ── Read ──────────────────────────────────────────────────────

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Fetch a single user by primary key.

        Args:
            user_id: The user's database ID.

        Returns:
            The ``User`` instance or ``None`` if not found.
        """
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Fetch a single user by email address.

        Args:
            email: The email to look up (case-insensitive).

        Returns:
            The ``User`` instance or ``None`` if not found.
        """
        result = await self.db.execute(
            select(User).where(func.lower(User.email) == email.lower())
        )
        return result.scalar_one_or_none()

    async def get_list(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        role: Optional[str] = None,
        is_active: Optional[bool] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> Tuple[List[User], int]:
        """
        Fetch a paginated, filtered, sorted list of users.

        Args:
            page: 1-indexed page number.
            page_size: Results per page.
            search: Free-text search across email, first_name, last_name.
            role: Exact role filter.
            is_active: Active-status filter.
            sort_by: Column name to sort by.
            sort_order: ``"asc"`` or ``"desc"``.

        Returns:
            A tuple of ``(users, total_count)``.
        """
        query = select(User)
        count_query = select(func.count(User.id))

        # ── Filters ──────────────────────────────────────────────
        if search:
            search_filter = or_(
                User.email.ilike(f"%{search}%"),
                User.first_name.ilike(f"%{search}%"),
                User.last_name.ilike(f"%{search}%"),
            )
            query = query.where(search_filter)
            count_query = count_query.where(search_filter)

        if role is not None:
            query = query.where(User.role == role)
            count_query = count_query.where(User.role == role)

        if is_active is not None:
            query = query.where(User.is_active == is_active)
            count_query = count_query.where(User.is_active == is_active)

        # ── Total count ──────────────────────────────────────────
        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0

        # ── Sorting ──────────────────────────────────────────────
        sort_column = getattr(User, sort_by, User.created_at)
        order = sort_column.asc() if sort_order == "asc" else sort_column.desc()
        query = query.order_by(order)

        # ── Pagination ───────────────────────────────────────────
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        result = await self.db.execute(query)
        users = list(result.scalars().all())

        return users, total

    # ── Create ────────────────────────────────────────────────────

    async def create(self, user: User) -> User:
        """
        Persist a new user to the database.

        Args:
            user: The ``User`` ORM instance to insert.

        Returns:
            The persisted user with ``id`` and timestamps populated.
        """
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    # ── Update ────────────────────────────────────────────────────

    async def update(self, user_id: int, data: Dict[str, Any]) -> Optional[User]:
        """
        Partially update a user's fields.

        Args:
            user_id: The user's database ID.
            data: Dictionary of column names → new values.

        Returns:
            The updated ``User`` instance or ``None`` if not found.
        """
        if not data:
            return await self.get_by_id(user_id)

        await self.db.execute(
            update(User).where(User.id == user_id).values(**data)
        )
        await self.db.commit()
        return await self.get_by_id(user_id)

    # ── Delete ────────────────────────────────────────────────────

    async def delete(self, user_id: int) -> bool:
        """
        Hard-delete a user from the database.

        Args:
            user_id: The user's database ID.

        Returns:
            ``True`` if a row was deleted, ``False`` if the user didn't exist.
        """
        result = await self.db.execute(
            delete(User).where(User.id == user_id)
        )
        await self.db.commit()
        return result.rowcount > 0
