"""Tests for settings configuration."""

from copilot_interactive.config.settings import Settings, get_settings


class TestSettings:
    """Tests for Settings configuration."""

    def test_default_values(self) -> None:
        """Test default setting values."""
        settings = Settings()
        assert settings.app_port == 4000
        assert settings.app_host == "0.0.0.0"
        assert settings.input_timeout == 540
        assert settings.assistant_host == "localhost"
        assert settings.assistant_port == 4141
        assert settings.assistant_timeout == 10
        assert settings.assistant_model == "gpt-5-mini"
        assert settings.notification_enabled is True
        assert settings.notification_max_content_length == 200

    def test_custom_port(self) -> None:
        """Test setting custom port."""
        settings = Settings(app_port=8080)
        assert settings.app_port == 8080

    def test_all_settings_customizable(self) -> None:
        """Test all settings can be customized."""
        settings = Settings(
            app_port=9000,
            app_host="127.0.0.1",
            input_timeout=60,
            assistant_host="remote.server",
            assistant_port=5000,
            assistant_timeout=30,
            assistant_model="custom-model",
            notification_enabled=False,
            notification_max_content_length=100,
        )
        assert settings.app_port == 9000
        assert settings.app_host == "127.0.0.1"
        assert settings.input_timeout == 60
        assert settings.assistant_host == "remote.server"
        assert settings.assistant_port == 5000
        assert settings.assistant_timeout == 30
        assert settings.assistant_model == "custom-model"
        assert settings.notification_enabled is False
        assert settings.notification_max_content_length == 100


class TestGetSettings:
    """Tests for get_settings function."""

    def test_returns_settings_instance(self) -> None:
        """Test that get_settings returns a Settings instance."""
        # Clear cache to ensure fresh instance
        get_settings.cache_clear()
        settings = get_settings()
        assert isinstance(settings, Settings)

    def test_caching(self) -> None:
        """Test that get_settings returns cached instance."""
        get_settings.cache_clear()
        settings1 = get_settings()
        settings2 = get_settings()
        assert settings1 is settings2
