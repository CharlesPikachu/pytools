"""Shared pytest fixtures and configuration for all tests."""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path
from typing import Generator, Dict, Any
from unittest.mock import Mock, MagicMock

import pytest

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files.
    
    Yields:
        Path: Path to the temporary directory.
    """
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    # Cleanup after test
    if temp_path.exists():
        shutil.rmtree(temp_path)


@pytest.fixture
def temp_file(temp_dir: Path) -> Generator[Path, None, None]:
    """Create a temporary file for testing.
    
    Args:
        temp_dir: Temporary directory fixture.
        
    Yields:
        Path: Path to the temporary file.
    """
    temp_file_path = temp_dir / "test_file.txt"
    temp_file_path.write_text("Test content")
    yield temp_file_path


@pytest.fixture
def mock_config() -> Dict[str, Any]:
    """Create a mock configuration dictionary.
    
    Returns:
        Dict[str, Any]: Mock configuration data.
    """
    return {
        "app_name": "pytools_test",
        "version": "0.1.0",
        "debug": True,
        "settings": {
            "timeout": 30,
            "max_retries": 3,
            "log_level": "DEBUG"
        }
    }


@pytest.fixture
def mock_json_file(temp_dir: Path, mock_config: Dict[str, Any]) -> Path:
    """Create a temporary JSON file with mock configuration.
    
    Args:
        temp_dir: Temporary directory fixture.
        mock_config: Mock configuration data.
        
    Returns:
        Path: Path to the JSON file.
    """
    json_path = temp_dir / "config.json"
    with open(json_path, 'w') as f:
        json.dump(mock_config, f, indent=2)
    return json_path


@pytest.fixture
def mock_response():
    """Create a mock HTTP response object.
    
    Returns:
        Mock: Mock response object with common attributes.
    """
    response = Mock()
    response.status_code = 200
    response.text = '{"success": true, "data": "test"}'
    response.json.return_value = {"success": True, "data": "test"}
    response.content = b'{"success": true, "data": "test"}'
    response.headers = {"Content-Type": "application/json"}
    response.raise_for_status = Mock()
    return response


@pytest.fixture
def mock_failed_response():
    """Create a mock failed HTTP response object.
    
    Returns:
        Mock: Mock response object representing a failed request.
    """
    response = Mock()
    response.status_code = 404
    response.text = '{"error": "Not found"}'
    response.json.return_value = {"error": "Not found"}
    response.content = b'{"error": "Not found"}'
    response.headers = {"Content-Type": "application/json"}
    response.raise_for_status = Mock(side_effect=Exception("404 Not Found"))
    return response


@pytest.fixture
def mock_qt_app(monkeypatch):
    """Mock PyQt5 QApplication for testing GUI components.
    
    Args:
        monkeypatch: Pytest monkeypatch fixture.
        
    Returns:
        Mock: Mocked QApplication instance.
    """
    mock_app = MagicMock()
    mock_app.exec_.return_value = 0
    
    # Mock PyQt5 imports if needed
    mock_pyqt5 = MagicMock()
    monkeypatch.setattr("PyQt5.QtWidgets.QApplication", lambda x: mock_app)
    
    return mock_app


@pytest.fixture
def sample_image_path(temp_dir: Path) -> Path:
    """Create a sample image file for testing.
    
    Args:
        temp_dir: Temporary directory fixture.
        
    Returns:
        Path: Path to the sample image.
    """
    # Create a simple 1x1 pixel PNG
    import base64
    
    # 1x1 transparent PNG
    png_data = base64.b64decode(
        b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=='
    )
    
    image_path = temp_dir / "test_image.png"
    image_path.write_bytes(png_data)
    return image_path


@pytest.fixture
def mock_email_server():
    """Create a mock email server for testing email functionality.
    
    Returns:
        Mock: Mock SMTP server object.
    """
    server = Mock()
    server.login = Mock(return_value=True)
    server.send_message = Mock()
    server.sendmail = Mock()
    server.quit = Mock()
    server.__enter__ = Mock(return_value=server)
    server.__exit__ = Mock(return_value=None)
    return server


@pytest.fixture
def env_vars(monkeypatch):
    """Set up test environment variables.
    
    Args:
        monkeypatch: Pytest monkeypatch fixture.
        
    Returns:
        Dict[str, str]: Dictionary of test environment variables.
    """
    test_env = {
        "TEST_MODE": "true",
        "LOG_LEVEL": "DEBUG",
        "API_KEY": "test_api_key_123",
        "DATABASE_URL": "sqlite:///:memory:"
    }
    
    for key, value in test_env.items():
        monkeypatch.setenv(key, value)
    
    return test_env


@pytest.fixture(autouse=True)
def reset_sys_modules():
    """Reset sys.modules to prevent import conflicts between tests.
    
    This fixture automatically runs before each test.
    """
    modules_before = set(sys.modules.keys())
    yield
    modules_after = set(sys.modules.keys())
    
    # Remove any modules that were imported during the test
    for module in modules_after - modules_before:
        if module.startswith('pytools'):
            sys.modules.pop(module, None)


# Markers for different test types
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "gui: mark test as requiring GUI components"
    )
    config.addinivalue_line(
        "markers", "network: mark test as requiring network access"
    )