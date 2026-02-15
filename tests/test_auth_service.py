"""Tests for authentication service functionality."""
import pytest

from src.auth_service import AuthService
from src.user_repository import UserRepository


class TestAuthService:
    """Tests for the AuthService class."""

    def test_register_creates_user_in_repository(self):
        """Registering a user should store them in the repository."""
        repo = UserRepository()
        auth = AuthService(repo)

        result = auth.register("test@example.com", "mypassword")

        assert result is True
        user = repo.find_by_email("test@example.com")
        assert user is not None
        assert user.email == "test@example.com"

    def test_register_with_existing_email_raises_error(self):
        """Registering with existing email should raise ValueError."""
        repo = UserRepository()
        auth = AuthService(repo)
        auth.register("test@example.com", "password1")

        with pytest.raises(ValueError, match="email already exists"):
            auth.register("test@example.com", "password2")

    def test_login_with_valid_credentials_returns_true(self):
        """Login with correct email and password should return True."""
        repo = UserRepository()
        auth = AuthService(repo)
        auth.register("test@example.com", "mypassword")

        result = auth.login("test@example.com", "mypassword")

        assert result is True

    def test_login_with_invalid_password_returns_false(self):
        """Login with wrong password should return False."""
        repo = UserRepository()
        auth = AuthService(repo)
        auth.register("test@example.com", "mypassword")

        result = auth.login("test@example.com", "wrongpassword")

        assert result is False

    def test_login_with_nonexistent_email_returns_false(self):
        """Login with non-existent email should return False."""
        repo = UserRepository()
        auth = AuthService(repo)

        result = auth.login("nonexistent@example.com", "anypassword")

        assert result is False
