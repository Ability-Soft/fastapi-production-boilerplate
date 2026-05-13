# Built by AbilitySoft | abilitysoft.net
"""
Authentication router — login, registration, and token refresh.

All endpoints are public (no Bearer token required).
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.user import UserRepository
from app.schemas.auth import (
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
)
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


def _get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    """
    Factory dependency that creates an AuthService for the current request.

    Args:
        db: The async database session.

    Returns:
        An ``AuthService`` instance.
    """
    return AuthService(UserRepository(db))


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=201,
    summary="Register a new user",
    description="Create a new user account and return JWT tokens.",
)
async def register(
    payload: RegisterRequest,
    auth_service: AuthService = Depends(_get_auth_service),
) -> TokenResponse:
    """
    Register a new user account.

    Args:
        payload: Registration data (email, password, name).
        auth_service: Injected auth service.

    Returns:
        A ``TokenResponse`` with access and refresh tokens.
    """
    return await auth_service.register(payload)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login",
    description="Authenticate with email and password to receive JWT tokens.",
)
async def login(
    payload: LoginRequest,
    auth_service: AuthService = Depends(_get_auth_service),
) -> TokenResponse:
    """
    Authenticate a user and issue JWT tokens.

    Args:
        payload: Login credentials (email, password).
        auth_service: Injected auth service.

    Returns:
        A ``TokenResponse`` with access and refresh tokens.
    """
    return await auth_service.login(payload)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token",
    description="Exchange a valid refresh token for a new token pair.",
)
async def refresh_token(
    payload: RefreshTokenRequest,
    auth_service: AuthService = Depends(_get_auth_service),
) -> TokenResponse:
    """
    Refresh the access token using a valid refresh token.

    Args:
        payload: The refresh token.
        auth_service: Injected auth service.

    Returns:
        A new ``TokenResponse`` with fresh tokens.
    """
    return await auth_service.refresh(payload.refresh_token)
