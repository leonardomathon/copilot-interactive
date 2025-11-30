"""Request models for the API."""

from pydantic import BaseModel, Field


class UserInputRequest(BaseModel):
    """Request model for user input endpoint."""

    context: str = Field(
        default="",
        description="The context or reason for requesting user input. "
        "If provided and user doesn't respond, the local assistant will be used.",
    )


class AssistantChatRequest(BaseModel):
    """Request model for local assistant chat completions."""

    model: str = Field(description="The model to use for completion.")
    messages: list[dict[str, str]] = Field(
        description="List of messages in the conversation."
    )
    max_tokens: int = Field(default=256, description="Maximum tokens in the response.")
