"""Tests for user repository functionality."""
import pytest

from src.user_repository import UserRepository
from src.password import hash_password, verify_password


class TestUserRepository:
    """Tests for the UserRepository class."""

    def test_create_user_stores_hashed_password(self):
        """Created user password should be hashed, not plain text."""
        repo = UserRepository()
        user = repo.create_user("test@example.com", "mypassword")

        # Password should not be stored as plain text
        assert user.password != "mypassword"
        # But should verify correctly
        assert verify_password("mypassword", user.password) is True

    def test_create_user_with_duplicate_email_raises_error(self):
        """Creating user with existing email should raise ValueError."""
        repo = UserRepository()
        repo.create_user("test@example.com", "password1")

        with pytest.raises(ValueError, match="email already exists"):
            repo.create_user("test@example.com", "password2")

    def test_find_user_by_email_returns_user_if_exists(self):
        """Finding existing user should return the user."""
        repo = UserRepository()
        created = repo.create_user("test@example.com", "mypassword")

        found = repo.find_by_email("test@example.com")

        assert found is not None
        assert found.email == "test@example.com"
        assert found.id == created.id

    def test_find_user_by_email_returns_none_if_not_exists(self):
        """Finding non-existent user should return None."""
        repo = UserRepository()

        found = repo.find_by_email("nonexistent@example.com")

        assert found is None

    def test_created_user_has_unique_id(self):
        """Each created user should have a unique ID."""
        repo = UserRepository()
        user1 = repo.create_user("user1@example.com", "password1")
        user2 = repo.create_user("user2@example.com", "password2")

        assert user1.id is not None
        assert user2.id is not None
        assert user1.id != user2.id
