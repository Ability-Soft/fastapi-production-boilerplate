# Built by AbilitySoft | abilitysoft.net
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    """
    Test user registration.
    """
    payload = {
        "email": "test@example.com",
        "password": "securepassword123",
        "first_name": "Test",
        "last_name": "User"
    }
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]
    assert "id" in data


@pytest.mark.asyncio
async def test_login_user(client: AsyncClient):
    """
    Test user login and token generation.
    """
    # First register
    payload = {
        "email": "login@example.com",
        "password": "securepassword123",
        "first_name": "Login",
        "last_name": "User"
    }
    await client.post("/api/v1/auth/register", json=payload)

    # Then login
    login_payload = {
        "email": "login@example.com",
        "password": "securepassword123"
    }
    response = await client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_get_me(client: AsyncClient):
    """
    Test getting current user profile.
    """
    # Register and login
    payload = {
        "email": "me@example.com",
        "password": "securepassword123",
        "first_name": "Me",
        "last_name": "User"
    }
    await client.post("/api/v1/auth/register", json=payload)
    
    login_response = await client.post("/api/v1/auth/login", json={
        "email": "me@example.com",
        "password": "securepassword123"
    })
    token = login_response.json()["access_token"]

    # Get profile
    response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"
