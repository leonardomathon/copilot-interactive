"""Tests for AssistantService."""

import json

import pytest

from copilot_interactive.config.settings import Settings
from copilot_interactive.services.assistant_service import AssistantService


class TestAssistantServiceParseResponse:
    """Tests for AssistantService._parse_response method."""

    @pytest.fixture
    def service(self) -> AssistantService:
        """Create an AssistantService instance for testing."""
        settings = Settings()
        return AssistantService(settings)

    def test_parse_openai_format(self, service: AssistantService) -> None:
        """Test parsing OpenAI Chat Completions format."""
        response = json.dumps(
            {
                "choices": [
                    {"message": {"role": "assistant", "content": "suggested input"}}
                ]
            }
        )
        result = service._parse_response(response)
        assert result == "suggested input"

    def test_parse_openai_format_with_whitespace(
        self, service: AssistantService
    ) -> None:
        """Test parsing strips whitespace."""
        response = json.dumps(
            {"choices": [{"message": {"content": "  suggested input  \n"}}]}
        )
        result = service._parse_response(response)
        assert result == "suggested input"

    def test_parse_empty_choices(self, service: AssistantService) -> None:
        """Test parsing with empty choices list."""
        response = json.dumps({"choices": []})
        result = service._parse_response(response)
        assert result is None

    def test_parse_missing_content(self, service: AssistantService) -> None:
        """Test parsing when content is missing."""
        response = json.dumps({"choices": [{"message": {}}]})
        result = service._parse_response(response)
        assert result is None

    def test_parse_plain_string_json(self, service: AssistantService) -> None:
        """Test parsing plain string in JSON format."""
        response = json.dumps("suggested input")
        result = service._parse_response(response)
        assert result == "suggested input"

    def test_parse_non_json_text(self, service: AssistantService) -> None:
        """Test parsing non-JSON plain text."""
        response = "suggested input as plain text"
        result = service._parse_response(response)
        assert result == "suggested input as plain text"

    def test_parse_empty_response(self, service: AssistantService) -> None:
        """Test parsing empty response."""
        result = service._parse_response("")
        assert result is None

    def test_parse_whitespace_only(self, service: AssistantService) -> None:
        """Test parsing whitespace-only response."""
        result = service._parse_response("   \n\t  ")
        assert result is None
