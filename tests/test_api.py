"""Tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient

from copilot_interactive import __version__
from copilot_interactive.main import app


class TestHealthEndpoint:
    """Tests for health check endpoint."""

    @pytest.fixture
    def client(self) -> TestClient:
        """Create a test client."""
        return TestClient(app)

    def test_health_check_returns_200(self, client: TestClient) -> None:
        """Test health check returns 200 status."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_response_format(self, client: TestClient) -> None:
        """Test health check response format."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert "version" in data
        assert data["status"] == "healthy"
        assert data["version"] == __version__


class TestOpenAPISchema:
    """Tests for OpenAPI schema."""

    @pytest.fixture
    def client(self) -> TestClient:
        """Create a test client."""
        return TestClient(app)

    def test_openapi_schema_available(self, client: TestClient) -> None:
        """Test OpenAPI schema is available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200

    def test_openapi_schema_has_endpoints(self, client: TestClient) -> None:
        """Test OpenAPI schema includes expected endpoints."""
        response = client.get("/openapi.json")
        data = response.json()
        paths = data.get("paths", {})
        assert "/health" in paths
        assert "/user-input" in paths
        assert "/user-input/json" in paths
