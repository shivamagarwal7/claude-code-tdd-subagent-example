"""Tests for password hashing functionality."""
import pytest

from src.password import hash_password, verify_password


class TestHashPassword:
    """Tests for the hash_password function."""

    def test_hash_password_returns_different_value_than_input(self):
        """Hash should not be the same as the original password."""
        password = "mysecretpassword"
        hashed = hash_password(password)
        assert hashed != password

    def test_hash_password_produces_unique_hashes(self):
        """Same password hashed twice should produce different hashes (due to salt)."""
        password = "mysecretpassword"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        assert hash1 != hash2

    def test_hash_password_rejects_empty_password(self):
        """Empty password should raise ValueError."""
        with pytest.raises(ValueError):
            hash_password("")


class TestVerifyPassword:
    """Tests for the verify_password function."""

    def test_verify_password_returns_true_for_correct_password(self):
        """Verification should succeed for the correct password."""
        password = "mysecretpassword"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True

    def test_verify_password_returns_false_for_incorrect_password(self):
        """Verification should fail for an incorrect password."""
        password = "mysecretpassword"
        wrong_password = "wrongpassword"
        hashed = hash_password(password)
        assert verify_password(wrong_password, hashed) is False
