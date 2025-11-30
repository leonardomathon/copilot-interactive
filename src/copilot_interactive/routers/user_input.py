"""User input router."""

from typing import Annotated

from fastapi import APIRouter, Body, Depends

from copilot_interactive.config.settings import Settings, get_settings
from copilot_interactive.models.requests import UserInputRequest
from copilot_interactive.models.responses import UserInputResponse
from copilot_interactive.services.assistant_service import AssistantService
from copilot_interactive.services.input_service import InputService
from copilot_interactive.services.notification_service import NotificationService

router = APIRouter(tags=["user-input"])


def get_input_service(
    settings: Annotated[Settings, Depends(get_settings)],
) -> InputService:
    """Dependency to get InputService instance."""
    notification_service = NotificationService(settings)
    assistant_service = AssistantService(settings)
    return InputService(settings, notification_service, assistant_service)


@router.post("/user-input", response_model=UserInputResponse)
async def request_user_input(
    input_service: Annotated[InputService, Depends(get_input_service)],
    body: Annotated[str, Body(media_type="text/plain")] = "",
) -> UserInputResponse:
    """
    Request user input from the terminal.

    Sends a notification and waits for user input from the terminal.
    If the user doesn't respond within the timeout and context is provided,
    falls back to the local assistant for a suggested response.

    Args:
        body: Plain text body containing context/reason for the input request.

    Returns:
        UserInputResponse with the input and its source.
    """
    context = body.strip() if body else ""
    return await input_service.get_user_input(context)


@router.post("/user-input/json", response_model=UserInputResponse)
async def request_user_input_json(
    input_service: Annotated[InputService, Depends(get_input_service)],
    request: UserInputRequest,
) -> UserInputResponse:
    """
    Request user input from the terminal (JSON body variant).

    Sends a notification and waits for user input from the terminal.
    If the user doesn't respond within the timeout and context is provided,
    falls back to the local assistant for a suggested response.

    Args:
        request: UserInputRequest containing context for the input request.

    Returns:
        UserInputResponse with the input and its source.
    """
    return await input_service.get_user_input(request.context)
