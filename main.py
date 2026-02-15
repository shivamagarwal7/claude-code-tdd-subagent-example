"""Demo script showing usage of the auth service."""
from src.user_repository import UserRepository
from src.auth_service import AuthService


def main():
    # Create repository and auth service
    repository = UserRepository()
    auth = AuthService(repository)

    # Register a new user
    email = "alice@example.com"
    password = "secret123"

    print(f"Registering user: {email}")
    auth.register(email, password)
    print("Registration successful!")

    # Login with correct credentials
    print(f"\nLogging in with correct password...")
    if auth.login(email, password):
        print("Login successful!")
    else:
        print("Login failed!")

    # Login with wrong credentials
    print(f"\nLogging in with wrong password...")
    if auth.login(email, "wrongpassword"):
        print("Login successful!")
    else:
        print("Login failed!")

    # Try to register duplicate user
    print(f"\nTrying to register same email again...")
    try:
        auth.register(email, "anotherpassword")
    except ValueError as e:
        print(f"Registration failed: {e}")


if __name__ == "__main__":
    main()
