"""Basic tests for FixtureGPT functionality."""

import os
import tempfile
import shutil
from pathlib import Path
import pytest

from fixturegpt import snapshot


def test_snapshot_import():
    """Test that snapshot function can be imported."""
    assert callable(snapshot)


def test_snapshot_record_mode():
    """Test snapshot function in record mode."""
    # Create a temporary directory for fixtures
    with tempfile.TemporaryDirectory() as temp_dir:
        # Change to temp directory
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        
        try:
            # Set record mode
            os.environ["FIXTUREGPT_MODE"] = "record"
            
            def dummy_function(x, y=10):
                return {"result": x + y}
            
            # Call snapshot
            result = snapshot("test_func", dummy_function, 5, y=15)
            
            # Check result
            assert result == {"result": 20}
            
            # Check fixture was created
            fixtures_dir = Path("./fixtures")
            assert fixtures_dir.exists()
            
            fixture_files = list(fixtures_dir.glob("test_func-*.json"))
            assert len(fixture_files) == 1
            
        finally:
            # Cleanup
            os.chdir(original_cwd)
            if "FIXTUREGPT_MODE" in os.environ:
                del os.environ["FIXTUREGPT_MODE"]


def test_snapshot_normal_mode():
    """Test snapshot function without mode set (normal execution)."""
    # Ensure no mode is set
    if "FIXTUREGPT_MODE" in os.environ:
        del os.environ["FIXTUREGPT_MODE"]
    
    def dummy_function(x):
        return x * 2
    
    # Should execute normally
    result = snapshot("test_normal", dummy_function, 10)
    assert result == 20


def test_snapshot_with_args_kwargs():
    """Test snapshot with both args and kwargs."""
    if "FIXTUREGPT_MODE" in os.environ:
        del os.environ["FIXTUREGPT_MODE"]
    
    def complex_function(a, b, c=None, d=42):
        return {"a": a, "b": b, "c": c, "d": d}
    
    result = snapshot("complex_test", complex_function, 1, 2, c="hello", d=100)
    expected = {"a": 1, "b": 2, "c": "hello", "d": 100}
    assert result == expected


if __name__ == "__main__":
    pytest.main([__file__]) 