"""Tests for Pydantic models."""

import pytest
from pydantic import ValidationError

from copilot_interactive.models.requests import AssistantChatRequest, UserInputRequest
from copilot_interactive.models.responses import (
    AssistantChatResponse,
    HealthCheckResponse,
    UserInputResponse,
)


class TestUserInputRequest:
    """Tests for UserInputRequest model."""

    def test_default_context_is_empty(self) -> None:
        """Test that default context is empty string."""
        request = UserInputRequest()
        assert request.context == ""

    def test_context_with_value(self) -> None:
        """Test setting context value."""
        request = UserInputRequest(context="Please confirm deployment")
        assert request.context == "Please confirm deployment"

    def test_from_dict(self) -> None:
        """Test creating from dictionary."""
        data = {"context": "test context"}
        request = UserInputRequest.model_validate(data)
        assert request.context == "test context"


class TestAssistantChatRequest:
    """Tests for AssistantChatRequest model."""

    def test_required_fields(self) -> None:
        """Test that model and messages are required."""
        with pytest.raises(ValidationError):
            AssistantChatRequest()  # type: ignore[call-arg]

    def test_valid_request(self) -> None:
        """Test valid request creation."""
        request = AssistantChatRequest(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": "You are helpful."},
                {"role": "user", "content": "Hello"},
            ],
        )
        assert request.model == "gpt-5-mini"
        assert len(request.messages) == 2

    def test_default_max_tokens(self) -> None:
        """Test default max_tokens value."""
        request = AssistantChatRequest(
            model="gpt-5-mini",
            messages=[{"role": "user", "content": "Hello"}],
        )
        assert request.max_tokens == 256


class TestUserInputResponse:
    """Tests for UserInputResponse model."""

    def test_required_fields(self) -> None:
        """Test that input and source are required."""
        with pytest.raises(ValidationError):
            UserInputResponse()  # type: ignore[call-arg]

    def test_valid_response(self) -> None:
        """Test valid response creation."""
        response = UserInputResponse(input="user typed this", source="user")
        assert response.input == "user typed this"
        assert response.source == "user"

    def test_source_values(self) -> None:
        """Test different source values."""
        for source in ["user", "assistant", "default"]:
            response = UserInputResponse(input="test", source=source)
            assert response.source == source


class TestHealthCheckResponse:
    """Tests for HealthCheckResponse model."""

    def test_default_status(self) -> None:
        """Test default status is healthy."""
        response = HealthCheckResponse(version="0.1.0")
        assert response.status == "healthy"

    def test_with_custom_status(self) -> None:
        """Test with custom status."""
        response = HealthCheckResponse(status="degraded", version="0.1.0")
        assert response.status == "degraded"


class TestAssistantChatResponse:
    """Tests for AssistantChatResponse model."""

    def test_required_choices(self) -> None:
        """Test that choices is required."""
        with pytest.raises(ValidationError):
            AssistantChatResponse()  # type: ignore[call-arg]

    def test_valid_response(self) -> None:
        """Test valid response creation."""
        response = AssistantChatResponse(
            choices=[{"message": {"content": "suggested input"}}]
        )
        assert len(response.choices) == 1
