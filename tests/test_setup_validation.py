"""Validation tests to ensure the testing infrastructure is properly set up."""

import os
import sys
from pathlib import Path

import pytest


class TestSetupValidation:
    """Test class to validate the testing infrastructure setup."""
    
    @pytest.mark.unit
    def test_pytest_import(self):
        """Test that pytest can be imported successfully."""
        import pytest
        assert pytest is not None
        assert hasattr(pytest, 'mark')
        assert hasattr(pytest, 'fixture')
    
    @pytest.mark.unit
    def test_project_structure(self):
        """Test that the project structure is correct."""
        project_root = Path(__file__).parent.parent
        
        # Check main package exists
        assert (project_root / 'pytools').exists()
        assert (project_root / 'pytools' / '__init__.py').exists()
        
        # Check test directories exist
        assert (project_root / 'tests').exists()
        assert (project_root / 'tests' / '__init__.py').exists()
        assert (project_root / 'tests' / 'unit').exists()
        assert (project_root / 'tests' / 'integration').exists()
        assert (project_root / 'tests' / 'conftest.py').exists()
    
    @pytest.mark.unit
    def test_pytools_import(self):
        """Test that the main pytools package can be imported."""
        import pytools
        
        assert pytools is not None
        assert hasattr(pytools, '__version__')
        assert hasattr(pytools, '__title__')
        assert pytools.__title__ == 'pikachupytools'
    
    @pytest.mark.unit
    def test_fixtures_available(self, temp_dir, mock_config):
        """Test that custom fixtures are available and working."""
        # Test temp_dir fixture
        assert temp_dir.exists()
        assert temp_dir.is_dir()
        
        # Test mock_config fixture
        assert isinstance(mock_config, dict)
        assert 'app_name' in mock_config
        assert mock_config['app_name'] == 'pytools_test'
    
    @pytest.mark.unit
    def test_coverage_import(self):
        """Test that coverage tools can be imported."""
        try:
            import coverage
            assert coverage is not None
        except ImportError:
            pytest.skip("Coverage not yet installed")
    
    @pytest.mark.unit
    def test_mock_import(self):
        """Test that mock utilities can be imported."""
        from unittest.mock import Mock, patch
        
        assert Mock is not None
        assert patch is not None
        
        # Test basic mock functionality
        mock_obj = Mock()
        mock_obj.test_method.return_value = "test"
        assert mock_obj.test_method() == "test"
    
    @pytest.mark.unit
    def test_markers_defined(self, request):
        """Test that custom markers are properly defined."""
        # Check that this test has the unit marker
        assert 'unit' in [marker.name for marker in request.node.iter_markers()]
    
    @pytest.mark.integration
    def test_integration_marker(self, request):
        """Test that integration marker works."""
        assert 'integration' in [marker.name for marker in request.node.iter_markers()]
    
    @pytest.mark.slow
    def test_slow_marker(self, request):
        """Test that slow marker works."""
        assert 'slow' in [marker.name for marker in request.node.iter_markers()]
    
    @pytest.mark.unit
    @pytest.mark.parametrize("module_name", [
        "pytools.modules.calculator",
        "pytools.modules.clock",
        "pytools.modules.timer",
    ])
    def test_module_imports(self, module_name):
        """Test that various pytools modules can be imported."""
        try:
            parts = module_name.split('.')
            __import__(module_name)
            module = sys.modules[module_name]
            assert module is not None
        except ImportError as e:
            # Some modules might have dependencies not installed yet
            pytest.skip(f"Module {module_name} has unmet dependencies: {e}")
    
    @pytest.mark.unit
    def test_temp_file_fixture(self, temp_file):
        """Test the temp_file fixture."""
        assert temp_file.exists()
        assert temp_file.is_file()
        assert temp_file.read_text() == "Test content"
    
    @pytest.mark.unit
    def test_mock_response_fixture(self, mock_response):
        """Test the mock_response fixture."""
        assert mock_response.status_code == 200
        assert mock_response.json() == {"success": True, "data": "test"}
        
        # Test that raise_for_status doesn't raise
        mock_response.raise_for_status()
    
    @pytest.mark.unit
    def test_mock_failed_response_fixture(self, mock_failed_response):
        """Test the mock_failed_response fixture."""
        assert mock_failed_response.status_code == 404
        assert mock_failed_response.json() == {"error": "Not found"}
        
        # Test that raise_for_status raises exception
        with pytest.raises(Exception, match="404 Not Found"):
            mock_failed_response.raise_for_status()


class TestPytestConfiguration:
    """Test pytest configuration settings."""
    
    @pytest.mark.unit
    def test_pytest_ini_options(self):
        """Test that pytest.ini options are properly configured."""
        # This test validates that pytest configuration exists and can be loaded
        # The configuration is in pyproject.toml [tool.pytest.ini_options]
        project_root = Path(__file__).parent.parent
        pyproject_path = project_root / 'pyproject.toml'
        
        assert pyproject_path.exists()
        
        content = pyproject_path.read_text()
        assert '[tool.pytest.ini_options]' in content
        assert 'testpaths = ["tests"]' in content
        assert 'python_files = ["test_*.py", "*_test.py"]' in content
    
    @pytest.mark.unit
    def test_coverage_configuration(self):
        """Test that coverage is properly configured."""
        # This test validates that coverage configuration exists in pyproject.toml
        project_root = Path(__file__).parent.parent
        pyproject_path = project_root / 'pyproject.toml'
        
        assert pyproject_path.exists()
        
        content = pyproject_path.read_text()
        assert '[tool.coverage.run]' in content
        assert '[tool.coverage.report]' in content
        assert 'source = ["pytools"]' in content