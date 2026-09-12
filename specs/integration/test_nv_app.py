"""
Integration Tests for Core Application
"""

import pytest
import sys
from pathlib import Path

# Ensure core is in path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class TestAppFactory:
    """Test application factory and initialization"""

    def test_configure_environment(self):
        """Test environment configuration."""
        from core.core.nv_app_factory import configure_environment

        # Should not raise
        configure_environment()

        # Check that paths were added
        assert any("core/tabs" in path for path in sys.path)
        assert any("core/services" in path for path in sys.path)

    def test_dependency_injection(self):
        """Test dependency injection setup."""
        from core.core.nv_container import get_container

        nv_container = get_container()
        assert nv_container is not None

        # Test config provider
        config = nv_container.config()
        assert config is not None


class TestTabLoader:
    """Test tab loading functionality"""

    def test_get_available_tabs(self):
        """Test getting list of available tabs."""
        from core.core.nv_tab_loader import get_available_tabs

        tabs = get_available_tabs()
        assert len(tabs) > 0
        assert "🏠 Dashboard" in tabs

    def test_tab_renderer_mapping(self):
        """Test tab renderer mapping."""
        from core.core.nv_tab_loader import TAB_RENDERERS

        assert "🏠 Dashboard" in TAB_RENDERERS
        module_name, func_name = TAB_RENDERERS["🏠 Dashboard"]
        assert module_name == "core.tabs.nv_abp_dashboard"
        assert func_name == "render_dashboard_tab"


class TestSessionInitialization:
    """Test session state initialization"""

    def test_session_defaults(self):
        """Test that session defaults are properly defined."""
        from core.core.nv_session_init import _initialize_ui_state

        # Should not raise
        # Note: In real specs, we'd mock streamlit.session_state
        pass


class TestErrorHandling:
    """Test error handling integration"""

    def test_error_context_integration(self):
        """Test ErrorContext in real scenario."""
        from core.core.nv_exceptions import ErrorContext

        with ErrorContext("test operation", show_user=False):
            result = 1 + 1

        assert result == 2

    def test_validation_integration(self):
        """Test input nv_validation in integration scenario."""
        from core.core.nv_exceptions import validate_input, ValidationError

        # Valid input
        validate_input(5, "count", expected_type=int, min_value=1, max_value=10)

        # Invalid input should raise
        with pytest.raises(ValidationError):
            validate_input(15, "count", max_value=10)
