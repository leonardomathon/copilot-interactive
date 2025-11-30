"""Service for handling user input collection."""

import asyncio
import logging
import sys
from concurrent.futures import ThreadPoolExecutor

from copilot_interactive.config.settings import Settings
from copilot_interactive.models.responses import UserInputResponse
from copilot_interactive.services.assistant_service import AssistantService
from copilot_interactive.services.notification_service import NotificationService

logger = logging.getLogger(__name__)

# Thread pool for blocking input operations
_input_executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="input")


class InputService:
    """Service for collecting user input from the terminal."""

    def __init__(
        self,
        settings: Settings,
        notification_service: NotificationService,
        assistant_service: AssistantService,
    ) -> None:
        """Initialize the input service."""
        self._settings = settings
        self._notification_service = notification_service
        self._assistant_service = assistant_service

    async def get_user_input(self, context: str = "") -> UserInputResponse:
        """
        Get user input, with fallback to assistant if timeout.

        Args:
            context: The context/reason for requesting input.

        Returns:
            UserInputResponse with the input and its source.
        """
        # Send notification
        await self._notification_service.send_input_request_notification(context)

        # Try to get user input from terminal
        user_input, success = await self._read_terminal_input()

        if success and user_input:
            return UserInputResponse(input=user_input, source="user")

        # User didn't respond - try assistant if we have context
        if context:
            suggestion = await self._assistant_service.get_suggested_input(context)
            if suggestion:
                return UserInputResponse(input=suggestion, source="assistant")

        # No response available
        return UserInputResponse(input="no response provided", source="default")

    async def _read_terminal_input(self) -> tuple[str, bool]:
        """
        Read input from the terminal with timeout.

        Returns:
            Tuple of (input_text, success).
        """
        try:
            return await self._read_terminal_input_blocking()
        except Exception as e:
            logger.error("Failed to read terminal input: %s", e)
            return ("", False)

    async def _read_terminal_input_blocking(self) -> tuple[str, bool]:
        """
        Read terminal input using blocking I/O in a thread pool.

        This reads directly from the terminal where the server is running,
        allowing the user to type their response.
        """
        loop = asyncio.get_event_loop()
        timeout = self._settings.input_timeout

        def blocking_input() -> str:
            """Blocking function to read input from stdin."""
            try:
                # Print prompt to stderr so it shows even if stdout is captured
                print(
                    "\n>>> Please enter your input and press Enter: ",
                    end="",
                    flush=True,
                )
                # Read from stdin
                line = sys.stdin.readline()
                return line.strip() if line else ""
            except EOFError:
                return ""
            except Exception as e:
                logger.error("Error reading input: %s", e)
                return ""

        try:
            # Run the blocking input in a thread pool with timeout
            result = await asyncio.wait_for(
                loop.run_in_executor(_input_executor, blocking_input),
                timeout=timeout,
            )
            if result:
                return (result, True)
            return ("", False)
        except TimeoutError:
            logger.info("Input timed out after %d seconds", timeout)
            print("\n[Input timed out]", flush=True)
            return ("", False)
        except Exception as e:
            logger.error("Failed to read terminal input: %s", e)
            return ("", False)
