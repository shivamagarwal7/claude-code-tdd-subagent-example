"""Pytest configuration and shared fixtures."""
import pytest
from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope="module")
def postgres_container():
    """Spin up a PostgreSQL container for integration tests."""
    with PostgresContainer("postgres:15-alpine") as postgres:
        yield postgres


@pytest.fixture(scope="module")
def postgres_connection_url(postgres_container):
    """Get the connection URL for the PostgreSQL container."""
    return postgres_container.get_connection_url()
