# Built by AbilitySoft | abilitysoft.net
"""
Declarative base model for all SQLAlchemy ORM models.

Provides shared columns (``id``, ``created_at``, ``updated_at``) so
every table has consistent primary keys and audit timestamps.
"""

from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Abstract base class for all ORM models.

    Attributes:
        id: Auto-incrementing primary key.
        created_at: Timestamp set automatically on INSERT.
        updated_at: Timestamp updated automatically on every UPDATE.
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
