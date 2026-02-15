# Navigator Handoff

## Mode: RED

### Test Files Created
- `/Users/shivam/Documents/workspace/claude-code-tdd-subagent-example/tests/conftest.py` - Shared fixtures for PostgreSQL container
- `/Users/shivam/Documents/workspace/claude-code-tdd-subagent-example/tests/test_postgres_repository.py` - Integration tests for PostgresUserRepository

### Tests Written
1. `test_connection_to_postgres_docker` - Verifies repository connects to PostgreSQL and initializes schema
2. `test_create_user_persists_to_postgres` - Verifies user creation persists to database with hashed password
3. `test_find_user_returns_persisted_user` - Verifies finding user retrieves persisted data from database
4. `test_duplicate_username_raises_error` - Verifies duplicate email raises ValueError

### Failure Output
```
ModuleNotFoundError: No module named 'src.postgres_repository'
```

### Dependencies Installed
- testcontainers[postgres]
- psycopg2-binary

### Implementation Requirements for Driver
Create `/Users/shivam/Documents/workspace/claude-code-tdd-subagent-example/src/postgres_repository.py` with:

1. **PostgresUserRepository class:**
   - `__init__(connection_url: str)` - Accepts PostgreSQL connection URL, establishes connection, creates users table if not exists
   - `is_connected() -> bool` - Returns True if connected to database
   - `create_user(email: str, password: str) -> User` - Inserts user with hashed password, returns User object with database-assigned ID
   - `find_by_email(email: str) -> Optional[User]` - Queries user by email, returns User or None

2. **Schema:**
   - users table with: id (SERIAL PRIMARY KEY), email (UNIQUE), password (VARCHAR)

3. **Error Handling:**
   - Catch unique constraint violation on email and raise `ValueError("email already exists")`

4. **Reuse:**
   - Import `User` dataclass from `src.user_repository`
   - Import `hash_password` from `src.password`

### Next
Invoke driver MODE: GREEN
