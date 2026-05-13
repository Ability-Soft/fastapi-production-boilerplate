# Built by AbilitySoft | abilitysoft.net
"""
Authentication Pydantic schemas.

Covers login requests, registration, and token response payloads.
"""

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """
    Schema for the login endpoint.

    Attributes:
        email: The user's email address.
        password: The user's plain-text password.
    """

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password (min 8 chars)")


class RegisterRequest(BaseModel):
    """
    Schema for user registration.

    Attributes:
        email: A unique email address.
        password: The desired password (min 8 characters).
        first_name: User's first name.
        last_name: User's last name.
    """

    email: EmailStr = Field(..., description="Unique email address")
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Password (8-128 characters)",
    )
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="First name",
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Last name",
    )


class TokenResponse(BaseModel):
    """
    Schema for the JWT token pair returned after login/registration.

    Attributes:
        access_token: Short-lived access token.
        refresh_token: Long-lived refresh token.
        token_type: Always ``"bearer"``.
    """

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    """
    Schema for requesting a new access token via a refresh token.

    Attributes:
        refresh_token: The refresh token issued during login.
    """

    refresh_token: str = Field(..., description="Valid refresh token")
