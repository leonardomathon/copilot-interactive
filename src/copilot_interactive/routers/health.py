"""Health check router."""

from fastapi import APIRouter

from copilot_interactive import __version__
from copilot_interactive.models.responses import HealthCheckResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthCheckResponse)
async def health_check() -> HealthCheckResponse:
    """Health check endpoint."""
    return HealthCheckResponse(status="healthy", version=__version__)
