"""PostgreSQL-backed user repository."""
import psycopg2
from psycopg2 import errors
from typing import Optional
from src.user_repository import User
from src.password import hash_password


class PostgresUserRepository:
    """Repository for managing users in PostgreSQL."""

    def __init__(self, connection_url: str):
        """Initialize repository with PostgreSQL connection.

        Args:
            connection_url: PostgreSQL connection URL
        """
        # Handle SQLAlchemy-style URLs (postgresql+psycopg2://)
        normalized_url = connection_url.replace("postgresql+psycopg2://", "postgresql://")
        self._connection = psycopg2.connect(normalized_url)
        self._create_schema()

    def _create_schema(self):
        """Create users table if it doesn't exist."""
        with self._connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL
                )
            """)
            self._connection.commit()

    def is_connected(self) -> bool:
        """Check if connected to database.

        Returns:
            True if connected
        """
        return self._connection is not None and not self._connection.closed

    def create_user(self, email: str, password: str) -> User:
        """Create a new user with hashed password.

        Args:
            email: User's email address
            password: User's plain text password

        Returns:
            Created User object with database-assigned ID

        Raises:
            ValueError: If email already exists
        """
        hashed_password = hash_password(password)

        try:
            with self._connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (email, password) VALUES (%s, %s) RETURNING id",
                    (email, hashed_password)
                )
                user_id = cursor.fetchone()[0]
                self._connection.commit()
                return User(id=user_id, email=email, password=hashed_password)
        except errors.UniqueViolation:
            self._connection.rollback()
            raise ValueError("email already exists")

    def find_by_email(self, email: str) -> Optional[User]:
        """Find a user by email address.

        Args:
            email: Email address to search for

        Returns:
            User if found, None otherwise
        """
        with self._connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, email, password FROM users WHERE email = %s",
                (email,)
            )
            row = cursor.fetchone()
            if row:
                return User(id=row[0], email=row[1], password=row[2])
            return None
