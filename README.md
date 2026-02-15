# Auth Service Example

A simple authentication service demonstrating user registration and login with password hashing.

## Features

- User registration with email/password
- Secure password hashing using bcrypt
- Login authentication
- In-memory and PostgreSQL storage options

## Setup

```bash
pip install bcrypt psycopg2-binary pytest
```

## Usage

```python
from src.user_repository import UserRepository
from src.auth_service import AuthService

repository = UserRepository()
auth = AuthService(repository)

# Register a user
auth.register("user@example.com", "password123")

# Login
if auth.login("user@example.com", "password123"):
    print("Authenticated!")
```

Run the demo:
```bash
python3 main.py
```

## Testing

```bash
pytest -v
```

Note: PostgreSQL tests require a running Docker container.
