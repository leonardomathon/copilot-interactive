"""Utility functions for the application."""

from copilot_interactive.utils.platform import get_platform_name, is_windows
from copilot_interactive.utils.text import truncate_text

__all__ = [
    "get_platform_name",
    "is_windows",
    "truncate_text",
]
