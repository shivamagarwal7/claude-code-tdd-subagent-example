"""Password hashing utilities."""
import bcrypt


def hash_password(password: str) -> str:
    """Hash a password with salt using bcrypt.

    Args:
        password: The password to hash

    Returns:
        The hashed password as a string

    Raises:
        ValueError: If password is empty
    """
    if not password:
        raise ValueError("Password cannot be empty")

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against a hash.

    Args:
        password: The password to verify
        password_hash: The hash to verify against

    Returns:
        True if password matches the hash, False otherwise
    """
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
