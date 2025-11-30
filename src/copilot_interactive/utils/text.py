"""Text utility functions."""


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length, adding a suffix if truncated.

    Args:
        text: The text to truncate.
        max_length: Maximum length of the result (including suffix).
        suffix: Suffix to add if text is truncated.

    Returns:
        The truncated text with suffix, or original text if no truncation needed.
    """
    if len(text) <= max_length:
        return text

    # Account for suffix length
    truncate_at = max_length - len(suffix)
    if truncate_at <= 0:
        return suffix[:max_length]

    return text[:truncate_at] + suffix


def sanitize_input(text: str) -> str:
    """
    Sanitize user input by stripping whitespace.

    Args:
        text: The text to sanitize.

    Returns:
        The sanitized text.
    """
    return text.strip() if text else ""
