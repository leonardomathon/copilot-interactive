"""API routers for the application."""

from copilot_interactive.routers.health import router as health_router
from copilot_interactive.routers.user_input import router as user_input_router

__all__ = [
    "health_router",
    "user_input_router",
]
