"""Main FastAPI application entry point."""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from copilot_interactive import __version__
from copilot_interactive.config.settings import get_settings
from copilot_interactive.routers import health_router, user_input_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan context manager."""
    settings = get_settings()
    logger.info("Starting Copilot Interactive v%s", __version__)
    logger.info("Server will listen on %s:%d", settings.app_host, settings.app_port)
    logger.info("Input timeout: %d seconds", settings.input_timeout)
    yield
    logger.info("Shutting down Copilot Interactive")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Copilot Interactive",
        description=(
            "A FastAPI application that enables interactive Copilot sessions "
            "by allowing Copilot to request user input within a single token session."
        ),
        version=__version__,
        lifespan=lifespan,
    )

    # Include routers
    app.include_router(health_router)
    app.include_router(user_input_router)

    return app


app = create_app()


def main() -> None:
    """Run the application using uvicorn."""
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "copilot_interactive.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=False,
    )


if __name__ == "__main__":
    main()
