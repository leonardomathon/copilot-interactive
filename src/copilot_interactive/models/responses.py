"""Response models for the API."""

from pydantic import BaseModel, Field


class UserInputResponse(BaseModel):
    """Response model for user input endpoint."""

    input: str = Field(description="The user input or generated response.")
    source: str = Field(
        description="Source of the input: 'user', 'assistant', or 'default'."
    )


class HealthCheckResponse(BaseModel):
    """Response model for health check endpoint."""

    status: str = Field(default="healthy", description="Health status of the service.")
    version: str = Field(description="Version of the application.")


class AssistantChatResponse(BaseModel):
    """Response model from local assistant chat completions."""

    choices: list[dict[str, object]] = Field(description="List of completion choices.")
