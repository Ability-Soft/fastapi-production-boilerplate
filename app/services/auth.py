# Built by AbilitySoft | abilitysoft.net
"""
Authentication service — business logic for login, registration, and token refresh.

Orchestrates calls to the user repository and security utilities.
"""

from app.core.exceptions import BadRequestException, ConflictException, UnauthorizedException
from app.core.logging_config import get_logger
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse

logger = get_logger(__name__)


class AuthService:
    """
    Service layer for authentication operations.

    Each instance is scoped to a single request via the repository's session.
    """

    def __init__(self, user_repo: UserRepository) -> None:
        """
        Initialise the auth service.

        Args:
            user_repo: The user repository instance.
        """
        self.user_repo = user_repo

    async def register(self, payload: RegisterRequest) -> TokenResponse:
        """
        Register a new user and return a JWT token pair.

        Args:
            payload: The registration data (email, password, name).

        Returns:
            A ``TokenResponse`` with access and refresh tokens.

        Raises:
            ConflictException: If the email is already registered.
        """
        existing = await self.user_repo.get_by_email(payload.email)
        if existing:
            raise ConflictException(f"Email '{payload.email}' is already registered")

        user = User(
            email=payload.email,
            hashed_password=hash_password(payload.password),
            first_name=payload.first_name,
            last_name=payload.last_name,
            role="user",
            is_active=True,
        )
        user = await self.user_repo.create(user)
        logger.info("New user registered: %s (id=%d)", user.email, user.id)

        return self._generate_tokens(user)

    async def login(self, payload: LoginRequest) -> TokenResponse:
        """
        Authenticate a user and return a JWT token pair.

        Args:
            payload: The login credentials (email, password).

        Returns:
            A ``TokenResponse`` with access and refresh tokens.

        Raises:
            UnauthorizedException: If the email or password is incorrect.
        """
        user = await self.user_repo.get_by_email(payload.email)

        if not user or not verify_password(payload.password, user.hashed_password):
            raise UnauthorizedException("Incorrect email or password")

        if not user.is_active:
            raise UnauthorizedException("Account is deactivated")

        logger.info("User logged in: %s (id=%d)", user.email, user.id)
        return self._generate_tokens(user)

    async def refresh(self, refresh_token: str) -> TokenResponse:
        """
        Issue a new access token using a valid refresh token.

        Args:
            refresh_token: The refresh token from the client.

        Returns:
            A new ``TokenResponse`` with fresh tokens.

        Raises:
            UnauthorizedException: If the refresh token is invalid or expired.
        """
        try:
            payload = decode_token(refresh_token)
            if payload.get("type") != "refresh":
                raise UnauthorizedException("Invalid token type")

            user_id = payload.get("sub")
            if not user_id:
                raise UnauthorizedException("Invalid token payload")
        except Exception:
            raise UnauthorizedException("Refresh token is invalid or expired")

        user = await self.user_repo.get_by_id(int(user_id))
        if not user or not user.is_active:
            raise UnauthorizedException("User not found or deactivated")

        logger.info("Token refreshed for user: %s (id=%d)", user.email, user.id)
        return self._generate_tokens(user)

    # ── Private helpers ───────────────────────────────────────────

    @staticmethod
    def _generate_tokens(user: User) -> TokenResponse:
        """
        Generate an access + refresh token pair for a user.

        Args:
            user: The authenticated user.

        Returns:
            A ``TokenResponse`` containing both tokens.
        """
        token_data = {"sub": str(user.id), "email": user.email, "role": user.role}
        return TokenResponse(
            access_token=create_access_token(token_data),
            refresh_token=create_refresh_token(token_data),
        )
