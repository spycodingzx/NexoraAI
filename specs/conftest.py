"""
Test Configuration and Fixtures

Provides common test fixtures and configuration for pytest.
"""

import os
import sys
from pathlib import Path

import pytest

# Add core directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def test_env():
    """Set up test environment variables."""
    original_env = os.environ.copy()

    # Set test environment variables
    os.environ["ENVIRONMENT"] = "test"
    os.environ["DEBUG"] = "true"

    # Clear lru_cache so nv_settings are freshly loaded with test env vars
    from core.config.nv_settings import get_settings

    get_settings.cache_clear()

    yield

    # Restore original environment and clear cache again
    os.environ.clear()
    os.environ.update(original_env)
    from core.config.nv_settings import get_settings

    get_settings.cache_clear()


@pytest.fixture
def mock_settings():
    """Provide mock nv_settings for testing."""
    from core.config.nv_settings import AppSettings, ServerSettings, Settings

    return Settings(
        server=ServerSettings(backend_port=8601, frontend_port=8501),
        core=AppSettings(enable_analytics=False),
    )


@pytest.fixture
def mock_session_manager():
    """Provide mock session manager for testing."""
    import tempfile

    from core.services.nv_unified_session_manager import UnifiedSessionManager

    # Create temporary session directory
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = UnifiedSessionManager(session_dir=Path(tmpdir))
        yield manager


@pytest.fixture
def sample_session_data():
    """Provide sample session data for testing."""
    return {
        "timestamp": "2026-01-28T12:00:00",
        "session_name": "test_session",
        "version": "2.0",
        "state": {
            "campaigns": [{"name": "Test Campaign", "status": "active"}],
            "products": [],
            "current_tab": 0,
        },
    }
