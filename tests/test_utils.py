"""Tests for utility functions."""

from copilot_interactive.utils.platform import get_platform_name, is_linux, is_windows
from copilot_interactive.utils.text import sanitize_input, truncate_text


class TestTruncateText:
    """Tests for truncate_text function."""

    def test_no_truncation_needed(self) -> None:
        """Test that text shorter than max_length is returned unchanged."""
        text = "Hello World"
        result = truncate_text(text, max_length=20)
        assert result == "Hello World"

    def test_exact_length(self) -> None:
        """Test that text exactly at max_length is returned unchanged."""
        text = "Hello"
        result = truncate_text(text, max_length=5)
        assert result == "Hello"

    def test_truncation_with_default_suffix(self) -> None:
        """Test truncation with default '...' suffix."""
        text = "Hello World"
        result = truncate_text(text, max_length=8)
        assert result == "Hello..."
        assert len(result) == 8

    def test_truncation_with_custom_suffix(self) -> None:
        """Test truncation with custom suffix."""
        text = "Hello World"
        result = truncate_text(text, max_length=8, suffix="~")
        assert result == "Hello W~"
        assert len(result) == 8

    def test_empty_string(self) -> None:
        """Test empty string input."""
        result = truncate_text("", max_length=10)
        assert result == ""

    def test_very_short_max_length(self) -> None:
        """Test with max_length smaller than suffix."""
        text = "Hello"
        result = truncate_text(text, max_length=2, suffix="...")
        assert result == ".."

    def test_zero_max_length(self) -> None:
        """Test with zero max_length."""
        text = "Hello"
        result = truncate_text(text, max_length=0, suffix="...")
        assert result == ""


class TestSanitizeInput:
    """Tests for sanitize_input function."""

    def test_strips_whitespace(self) -> None:
        """Test that leading/trailing whitespace is stripped."""
        result = sanitize_input("  hello world  ")
        assert result == "hello world"

    def test_strips_newlines(self) -> None:
        """Test that newlines are stripped."""
        result = sanitize_input("\n\thello\n")
        assert result == "hello"

    def test_empty_string(self) -> None:
        """Test empty string input."""
        result = sanitize_input("")
        assert result == ""

    def test_none_like_empty(self) -> None:
        """Test that falsy empty string is handled."""
        result = sanitize_input("   ")
        assert result == ""


class TestPlatformUtils:
    """Tests for platform utility functions."""

    def test_is_windows_returns_bool(self) -> None:
        """Test that is_windows returns a boolean."""
        result = is_windows()
        assert isinstance(result, bool)

    def test_is_linux_returns_bool(self) -> None:
        """Test that is_linux returns a boolean."""
        result = is_linux()
        assert isinstance(result, bool)

    def test_get_platform_name_returns_string(self) -> None:
        """Test that get_platform_name returns a non-empty string."""
        result = get_platform_name()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_platform_mutual_exclusivity(self) -> None:
        """Test that Windows and Linux are mutually exclusive."""
        # Can't both be true at the same time
        if is_windows():
            assert not is_linux()
        if is_linux():
            assert not is_windows()
