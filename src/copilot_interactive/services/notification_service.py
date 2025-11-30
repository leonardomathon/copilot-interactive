"""Service for sending notifications."""

import asyncio
import logging
import shutil

from copilot_interactive.config.settings import Settings
from copilot_interactive.utils.platform import is_windows
from copilot_interactive.utils.text import truncate_text

logger = logging.getLogger(__name__)


class NotificationService:
    """Service for sending system notifications."""

    def __init__(self, settings: Settings) -> None:
        """Initialize the notification service."""
        self._settings = settings

    async def send_input_request_notification(self, context: str | None = None) -> bool:
        """
        Send a notification that input is requested.

        Args:
            context: Optional context/reason for the input request.

        Returns:
            True if notification was sent successfully, False otherwise.
        """
        if not self._settings.notification_enabled:
            logger.debug("Notifications are disabled")
            return False

        if is_windows():
            return await self._send_windows_notification(context)
        else:
            return await self._send_termux_notification(context)

    async def _send_windows_notification(self, context: str | None = None) -> bool:
        """Send a Windows toast notification using PowerShell."""
        try:
            title = "Input Requested"
            content = self._format_notification_content(context)

            # Use PowerShell to show a toast notification
            script = f"""
            [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
            [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null

            $template = @"
            <toast>
                <visual>
                    <binding template="ToastText02">
                        <text id="1">{title}</text>
                        <text id="2">{content}</text>
                    </binding>
                </visual>
            </toast>
"@

            $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
            $xml.LoadXml($template)
            $toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
            [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Copilot Interactive").Show($toast)
            """

            process = await asyncio.create_subprocess_exec(
                "powershell",
                "-NoProfile",
                "-NonInteractive",
                "-Command",
                script,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.PIPE,
            )

            _, stderr = await process.communicate()

            if process.returncode != 0:
                logger.warning(
                    "Windows notification failed: %s",
                    stderr.decode() if stderr else "unknown error",
                )
                return False

            return True

        except Exception as e:
            logger.warning("Failed to send Windows notification: %s", e)
            return False

    async def _send_termux_notification(self, context: str | None = None) -> bool:
        """Send a Termux notification (Linux/Android)."""
        if not shutil.which("termux-notification"):
            logger.debug("termux-notification not available")
            return False

        try:
            content = self._format_notification_content(context)
            title = "Input requested"

            # Try with inline reply first
            success = await self._try_termux_notification_with_reply(title, content)
            if success:
                return True

            # Fallback to plain notification
            return await self._try_termux_notification_plain(title, content)

        except Exception as e:
            logger.warning("Failed to send Termux notification: %s", e)
            return False

    async def _try_termux_notification_with_reply(
        self, title: str, content: str
    ) -> bool:
        """Try to send a Termux notification with inline reply support."""
        try:
            process = await asyncio.create_subprocess_exec(
                "termux-notification",
                "--title",
                title,
                "--content",
                content,
                "--input",
                "--input-label",
                "Reply",
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.PIPE,
            )

            _, _stderr = await process.communicate()
            return process.returncode == 0

        except Exception:
            return False

    async def _try_termux_notification_plain(self, title: str, content: str) -> bool:
        """Send a plain Termux notification without inline reply."""
        try:
            process = await asyncio.create_subprocess_exec(
                "termux-notification",
                "--title",
                title,
                "--content",
                content,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.PIPE,
            )

            _, _stderr = await process.communicate()
            return process.returncode == 0

        except Exception:
            return False

    def _format_notification_content(self, context: str | None) -> str:
        """Format the notification content."""
        if context:
            truncated = truncate_text(
                context, self._settings.notification_max_content_length, suffix=""
            )
            return f"Input requested: {truncated}"
        return "Input requested"
