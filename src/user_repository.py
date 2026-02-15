"""User repository for managing users."""
from dataclasses import dataclass
from typing import Optional
from src.password import hash_password


@dataclass
class User:
    """User entity."""
    id: int
    email: str
    password: str


class UserRepository:
    """Repository for managing users."""

    def __init__(self):
        """Initialize repository with in-memory storage."""
        self._users = {}
        self._next_id = 1

    def create_user(self, email: str, password: str) -> User:
        """Create a new user with hashed password.

        Args:
            email: User's email address
            password: User's plain text password

        Returns:
            Created User object

        Raises:
            ValueError: If email already exists
        """
        if email in self._users:
            raise ValueError("email already exists")

        hashed_password = hash_password(password)
        user = User(id=self._next_id, email=email, password=hashed_password)
        self._users[email] = user
        self._next_id += 1
        return user

    def find_by_email(self, email: str) -> Optional[User]:
        """Find a user by email address.

        Args:
            email: Email address to search for

        Returns:
            User if found, None otherwise
        """
        return self._users.get(email)
