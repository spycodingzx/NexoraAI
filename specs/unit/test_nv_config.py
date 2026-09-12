"""
Unit Tests for Configuration System
"""

import os
import pytest

from core.config.nv_settings import Settings, get_api_key


class TestSettings:
    """Test suite for Settings"""

    def test_default_settings(self):
        """Test default nv_settings values."""
        nv_settings = Settings()

        assert nv_settings.server.backend_port == 8601
        assert nv_settings.server.frontend_port == 8501
        assert nv_settings.server.environment == "development"

    def test_environment_override(self, test_env):
        """Test environment variable override."""
        os.environ["BACKEND_PORT"] = "9000"
        nv_settings = Settings()

        assert nv_settings.server.backend_port == 9000

    def test_get_api_key(self, test_env):
        """Test API key retrieval."""
        os.environ["REPLICATE_API_TOKEN"] = "test_token_123"
        nv_settings = Settings()

        key = nv_settings.get_api_key("REPLICATE_API_TOKEN")
        assert key == "test_token_123"

    def test_is_production(self, test_env):
        """Test production environment detection."""
        os.environ["ENVIRONMENT"] = "production"
        nv_settings = Settings()

        assert nv_settings.is_production() is True
        assert nv_settings.is_development() is False


class TestAPIKeyManagement:
    """Test API key management functions"""

    def test_get_api_key_function(self, test_env):
        """Test get_api_key helper function."""
        os.environ["TEST_API_KEY"] = "abc123"

        key = get_api_key("TEST_API_KEY")
        assert key == "abc123"

    def test_get_api_key_missing(self):
        """Test get_api_key with missing key."""
        key = get_api_key("NONEXISTENT_KEY")
        assert key is None
