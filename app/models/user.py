# Built by AbilitySoft | abilitysoft.net
"""
User ORM model.

Represents the ``users`` table in the database with columns for
authentication, profile data, and role-based access control.
"""

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class User(Base):
    """
    SQLAlchemy model for the ``users`` table.

    Attributes:
        email: Unique email address used for login.
        hashed_password: Bcrypt-hashed password (never store plain text!).
        first_name: User's first name.
        last_name: User's last name.
        role: Access role — ``"user"`` or ``"admin"``.
        is_active: Soft-delete / deactivation flag.
    """

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="user",
        server_default="user",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )

    def __repr__(self) -> str:
        """Return a developer-friendly representation of the User."""
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"
