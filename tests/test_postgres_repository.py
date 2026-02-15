"""Integration tests for PostgreSQL-backed UserRepository."""
import pytest
from testcontainers.postgres import PostgresContainer

from src.postgres_repository import PostgresUserRepository
from src.password import verify_password


class TestPostgresUserRepository:
    """Integration tests for PostgresUserRepository using testcontainers."""

    def test_connection_to_postgres_docker(self, postgres_connection_url):
        """Repository should successfully connect to PostgreSQL container."""
        repo = PostgresUserRepository(postgres_connection_url)

        # Should be able to connect and initialize schema
        assert repo.is_connected() is True

    def test_create_user_persists_to_postgres(self, postgres_connection_url):
        """Created user should be persisted to PostgreSQL database."""
        repo = PostgresUserRepository(postgres_connection_url)

        user = repo.create_user("persist@example.com", "securepassword")

        # User should have an ID assigned by the database
        assert user.id is not None
        assert user.email == "persist@example.com"
        # Password should be hashed
        assert user.password != "securepassword"
        assert verify_password("securepassword", user.password) is True

    def test_find_user_returns_persisted_user(self, postgres_connection_url):
        """Finding a user should return the user persisted in PostgreSQL."""
        repo = PostgresUserRepository(postgres_connection_url)

        # Create a user first
        created_user = repo.create_user("findme@example.com", "mypassword")

        # Find the user by email
        found_user = repo.find_by_email("findme@example.com")

        assert found_user is not None
        assert found_user.id == created_user.id
        assert found_user.email == "findme@example.com"
        assert verify_password("mypassword", found_user.password) is True

    def test_duplicate_username_raises_error(self, postgres_connection_url):
        """Creating a user with duplicate email should raise ValueError."""
        repo = PostgresUserRepository(postgres_connection_url)

        # Create initial user
        repo.create_user("duplicate@example.com", "password1")

        # Attempting to create another user with same email should fail
        with pytest.raises(ValueError, match="email already exists"):
            repo.create_user("duplicate@example.com", "password2")
