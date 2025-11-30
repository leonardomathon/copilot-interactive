"""Pytest configuration and fixtures."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from copilot_interactive.config.settings import Settings
from copilot_interactive.main import app


@pytest.fixture
def settings() -> Settings:
    """Create a test settings instance."""
    return Settings(
        app_port=8000,
        app_host="127.0.0.1",
        input_timeout=5,  # Short timeout for tests
        assistant_host="localhost",
        assistant_port=4141,
        assistant_timeout=2,
        notification_enabled=False,  # Disable notifications in tests
    )


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Create a test client for the FastAPI app."""
    with TestClient(app) as test_client:
        yield test_client
