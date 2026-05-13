# Built by AbilitySoft | abilitysoft.net
"""
Reusable FastAPI dependencies.

Provides the authenticated user dependency and role-checking helpers
that can be injected into any route handler.
"""

from typing import List

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.exceptions import ForbiddenException, UnauthorizedException
from app.core.security import decode_token
from app.models.user import User
from app.repositories.user import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Dependency that extracts and validates the current user from a JWT.

    Args:
        token: The Bearer token from the Authorization header.
        db: The async database session.

    Returns:
        The authenticated ``User`` ORM instance.

    Raises:
        UnauthorizedException: If the token is invalid or the user doesn't exist.
    """
    try:
        payload = decode_token(token)
        user_id: str | None = payload.get("sub")
        token_type: str | None = payload.get("type")

        if user_id is None or token_type != "access":
            raise UnauthorizedException("Invalid token payload")
    except JWTError:
        raise UnauthorizedException("Token is invalid or expired")

    repo = UserRepository(db)
    user = await repo.get_by_id(int(user_id))

    if user is None:
        raise UnauthorizedException("User not found")
    if not user.is_active:
        raise UnauthorizedException("User account is deactivated")

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependency that ensures the authenticated user's account is active.

    Args:
        current_user: The user resolved from the JWT.

    Returns:
        The active ``User`` instance.

    Raises:
        UnauthorizedException: If the user account is inactive.
    """
    if not current_user.is_active:
        raise UnauthorizedException("User account is deactivated")
    return current_user


class RoleChecker:
    """
    Callable dependency that enforces role-based access control.

    Usage::

        admin_only = RoleChecker(["admin"])

        @router.get("/admin-panel", dependencies=[Depends(admin_only)])
        async def admin_panel(): ...
    """

    def __init__(self, allowed_roles: List[str]) -> None:
        """
        Initialise the role checker.

        Args:
            allowed_roles: List of role names that are permitted access.
        """
        self.allowed_roles = allowed_roles

    async def __call__(
        self,
        current_user: User = Depends(get_current_active_user),
    ) -> User:
        """
        Verify that the current user has one of the allowed roles.

        Args:
            current_user: The authenticated user.

        Returns:
            The user if authorised.

        Raises:
            ForbiddenException: If the user's role is not in the allowed list.
        """
        if current_user.role not in self.allowed_roles:
            raise ForbiddenException(
                f"Role '{current_user.role}' is not authorised. "
                f"Required: {', '.join(self.allowed_roles)}"
            )
        return current_user
