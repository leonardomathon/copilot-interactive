"""Service for interacting with the local assistant."""

import json
import logging

import httpx

from copilot_interactive.config.settings import Settings

logger = logging.getLogger(__name__)


class AssistantService:
    """Service for calling the local OpenAI-compatible assistant."""

    SYSTEM_PROMPT = (
        "You are an assistant that must suggest a single-line terminal input "
        "that best matches the user intent given the context. "
        "Respond only with the suggested input, no explanation."
    )

    USER_PROMPT_TEMPLATE = (
        "Context: {context}\n\n"
        "Please provide a single-line input string (as the user would type) "
        "that should be returned automatically because the user did not respond. "
        "Do not wrap the suggestion in quotes."
    )

    def __init__(self, settings: Settings) -> None:
        """Initialize the assistant service."""
        self._settings = settings
        self._base_url = f"http://{settings.assistant_host}:{settings.assistant_port}"

    async def get_suggested_input(self, context: str) -> str | None:
        """
        Get a suggested input from the local assistant based on context.

        Args:
            context: The context/reason for the input request.

        Returns:
            The suggested input string, or None if unavailable.
        """
        if not context:
            return None

        try:
            payload = {
                "model": self._settings.assistant_model,
                "messages": [
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": self.USER_PROMPT_TEMPLATE.format(context=context),
                    },
                ],
                "max_tokens": 256,
            }

            async with httpx.AsyncClient(
                timeout=self._settings.assistant_timeout
            ) as client:
                response = await client.post(
                    f"{self._base_url}/chat/completions",
                    json=payload,
                    headers={"Content-Type": "application/json"},
                )

                if response.status_code != 200:
                    logger.warning(
                        "Assistant returned status %d: %s",
                        response.status_code,
                        response.text,
                    )
                    return None

                return self._parse_response(response.text)

        except httpx.TimeoutException:
            logger.warning("Assistant request timed out")
            return None
        except httpx.RequestError as e:
            logger.warning("Assistant request failed: %s", e)
            return None
        except Exception as e:
            logger.error("Unexpected error calling assistant: %s", e)
            return None

    def _parse_response(self, response_text: str) -> str | None:
        """
        Parse the assistant response to extract the suggested input.

        Args:
            response_text: Raw response text from the assistant.

        Returns:
            The extracted suggestion, or None if parsing failed.
        """
        try:
            data: object = json.loads(response_text)

            # Try OpenAI Chat Completions format
            if isinstance(data, dict) and "choices" in data:
                choices = data["choices"]
                if isinstance(choices, list) and len(choices) > 0:
                    first_choice = choices[0]
                    if isinstance(first_choice, dict):
                        message = first_choice.get("message")
                        if isinstance(message, dict):
                            content = message.get("content")
                            if isinstance(content, str):
                                return content.strip()

            # Fallback: if response is a plain string
            if isinstance(data, str):
                return data.strip()

            return None

        except json.JSONDecodeError:
            # If not JSON, return raw text if non-empty
            text = response_text.strip()
            return text if text else None
