"""Platform-specific utility functions."""

import platform
import sys


def is_windows() -> bool:
    """Check if the current platform is Windows."""
    return sys.platform == "win32" or platform.system() == "Windows"


def is_linux() -> bool:
    """Check if the current platform is Linux."""
    return sys.platform == "linux" or platform.system() == "Linux"


def get_platform_name() -> str:
    """Get the name of the current platform."""
    return platform.system()
