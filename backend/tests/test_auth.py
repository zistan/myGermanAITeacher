"""
Tests for authentication endpoints and utilities.
"""
import pytest
from fastapi import status

from app.utils.auth import verify_password, get_password_hash, create_access_token, decode_access_token


class TestPasswordHashing:
    """Test password hashing utilities."""

    def test_password_hashing(self):
        """Test that password hashing and verification works."""
        password = "mysecretpassword"
        hashed = get_password_hash(password)

        # Hash should not equal plain password
        assert hashed != password

        # Verification should work
        assert verify_password(password, hashed) is True

        # Wrong password should not verify
        assert verify_password("wrongpassword", hashed) is False

    def test_different_hashes_for_same_password(self):
        """Test that same password generates different hashes (salt)."""
        password = "testpassword"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)

        # Hashes should be different due to salt
        assert hash1 != hash2

        # Both should verify correctly
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True


class TestJWTTokens:
    """Test JWT token creation and decoding."""

    def test_create_and_decode_token(self):
        """Test creating and decoding a JWT token."""
        data = {"sub": 123, "username": "testuser"}
        token = create_access_token(data)

        # Token should be a string
        assert isinstance(token, str)

        # Decode should return original data
        decoded = decode_access_token(token)
        assert decoded is not None
        assert decoded["sub"] == 123
        assert decoded["username"] == "testuser"
        assert "exp" in decoded  # Expiration should be added

    def test_decode_invalid_token(self):
        """Test that invalid token returns None."""
        invalid_token = "invalid.token.string"
        decoded = decode_access_token(invalid_token)
        assert decoded is None


class TestAuthEndpoints:
    """Test authentication API endpoints."""

    def test_register_user_success(self, client):
        """Test successful user registration."""
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepassword123",
            "native_language": "it",
            "target_language": "de",
            "proficiency_level": "B2"
        }

        response = client.post("/api/v1/auth/register", json=user_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "newuser@example.com"
        assert "password" not in data  # Password should not be in response
        assert "id" in data

    def test_register_duplicate_username(self, client, test_user):
        """Test that registering duplicate username fails."""
        user_data = {
            "username": "testuser",  # Same as test_user
            "email": "different@example.com",
            "password": "password123"
        }

        response = client.post("/api/v1/auth/register", json=user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Username already registered" in response.json()["detail"]

    def test_register_duplicate_email(self, client, test_user):
        """Test that registering duplicate email fails."""
        user_data = {
            "username": "differentuser",
            "email": "test@example.com",  # Same as test_user
            "password": "password123"
        }

        response = client.post("/api/v1/auth/register", json=user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email already registered" in response.json()["detail"]

    def test_login_success(self, client, test_user):
        """Test successful login."""
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "testuser", "password": "testpassword123"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client, test_user):
        """Test login with wrong password."""
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "testuser", "password": "wrongpassword"}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect username or password" in response.json()["detail"]

    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user."""
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "nonexistent", "password": "password123"}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_current_user(self, client, test_user, auth_headers):
        """Test getting current user information."""
        response = client.get("/api/v1/auth/me", headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert "password" not in data

    def test_get_current_user_without_token(self, client):
        """Test that accessing /me without token fails."""
        response = client.get("/api/v1/auth/me")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_current_user_invalid_token(self, client):
        """Test that invalid token is rejected."""
        headers = {"Authorization": "Bearer invalid.token.here"}
        response = client.get("/api/v1/auth/me", headers=headers)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
