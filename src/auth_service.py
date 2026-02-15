"""Authentication service for user registration and login."""
from src.user_repository import UserRepository
from src.password import verify_password


class AuthService:
    """Service for handling user authentication."""

    def __init__(self, user_repository: UserRepository):
        """Initialize authentication service with repository.

        Args:
            user_repository: Repository for managing users
        """
        self._repository = user_repository

    def register(self, email: str, password: str) -> bool:
        """Register a new user.

        Args:
            email: User's email address
            password: User's password

        Returns:
            True on successful registration

        Raises:
            ValueError: If email already exists
        """
        self._repository.create_user(email, password)
        return True

    def login(self, email: str, password: str) -> bool:
        """Authenticate a user.

        Args:
            email: User's email address
            password: User's password

        Returns:
            True if authentication succeeds, False otherwise
        """
        user = self._repository.find_by_email(email)
        if user is None:
            return False
        return verify_password(password, user.password)
