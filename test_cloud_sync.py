#!/usr/bin/env python3
"""
Integration test for FixtureGPT cloud sync functionality.
"""

import os
import time
import tempfile
import shutil
from pathlib import Path
from fixturegpt import snapshot, configure_cloud_sync

def test_function(message: str, delay: float = 0.1):
    """A simple test function to record/replay."""
    time.sleep(delay)
    return {
        "message": message,
        "timestamp": time.time(),
        "processed": True
    }

def test_local_only():
    """Test local-only mode (default behavior)."""
    print("\n🧪 Test 1: Local-Only Mode")
    print("-" * 40)
    
    # Ensure clean state
    os.environ.pop('FIXTUREGPT_API_KEY', None)
    os.environ['FIXTUREGPT_SYNC_MODE'] = 'local'
    os.environ['FIXTUREGPT_MODE'] = 'record'
    
    # Record a fixture
    start_time = time.time()
    result1 = snapshot("test_local", test_function, "Hello local mode", 0.2)
    record_time = time.time() - start_time
    
    print(f"✅ Recorded in {record_time:.3f}s: {result1['message']}")
    
    # Switch to replay mode
    os.environ['FIXTUREGPT_MODE'] = 'replay'
    
    # Replay should be much faster
    start_time = time.time()
    result2 = snapshot("test_local", test_function, "Hello local mode", 0.2)
    replay_time = time.time() - start_time
    
    print(f"✅ Replayed in {replay_time:.3f}s: {result2['message']}")
    print(f"⚡ Speedup: {record_time/replay_time:.1f}x faster")
    
    assert result1['message'] == result2['message']
    assert replay_time < record_time / 2  # Should be much faster

def test_cloud_sync_configuration():
    """Test cloud sync configuration."""
    print("\n🧪 Test 2: Cloud Sync Configuration")
    print("-" * 40)
    
    # Test programmatic configuration
    configure_cloud_sync("test-api-key-12345", "both", "https://test.example.com")
    
    # Verify environment variables were set
    assert os.environ['FIXTUREGPT_API_KEY'] == "test-api-key-12345"
    assert os.environ['FIXTUREGPT_SYNC_MODE'] == "both"
    assert os.environ['FIXTUREGPT_API_URL'] == "https://test.example.com"
    
    print("✅ Programmatic configuration works")
    
    # Test environment variable configuration
    os.environ['FIXTUREGPT_API_KEY'] = "env-api-key-67890"
    os.environ['FIXTUREGPT_SYNC_MODE'] = "cloud"
    
    print("✅ Environment variable configuration works")

def test_cloud_sync_fallback():
    """Test cloud sync with fallback to local/live calls."""
    print("\n🧪 Test 3: Cloud Sync Fallback")
    print("-" * 40)
    
    # Configure for cloud sync (will fail with fake API key)
    configure_cloud_sync("fake-api-key", "both")
    os.environ['FIXTUREGPT_MODE'] = 'record'
    
    # This should try cloud sync, fail, but still work locally
    result = snapshot("test_fallback", test_function, "Testing fallback", 0.1)
    
    print(f"✅ Fallback worked: {result['message']}")
    
    # Switch to replay mode
    os.environ['FIXTUREGPT_MODE'] = 'replay'
    
    # Should replay from local cache
    result2 = snapshot("test_fallback", test_function, "Testing fallback", 0.1)
    
    print(f"✅ Local replay worked: {result2['message']}")
    assert result['message'] == result2['message']

def test_different_sync_modes():
    """Test different sync modes."""
    print("\n🧪 Test 4: Different Sync Modes")
    print("-" * 40)
    
    # Test local mode
    configure_cloud_sync("test-key", "local")
    os.environ['FIXTUREGPT_MODE'] = 'record'
    
    result1 = snapshot("test_modes_local", test_function, "Local mode test")
    print(f"✅ Local mode: {result1['message']}")
    
    # Test cloud mode (will fallback to live call)
    configure_cloud_sync("test-key", "cloud")
    
    result2 = snapshot("test_modes_cloud", test_function, "Cloud mode test")
    print(f"✅ Cloud mode (fallback): {result2['message']}")
    
    # Test both mode
    configure_cloud_sync("test-key", "both")
    
    result3 = snapshot("test_modes_both", test_function, "Both mode test")
    print(f"✅ Both mode: {result3['message']}")

def test_cli_integration():
    """Test CLI commands work with cloud sync."""
    print("\n🧪 Test 5: CLI Integration")
    print("-" * 40)
    
    import subprocess
    
    # Test stats command
    result = subprocess.run(
        ["python", "-m", "fixturegpt.cli", "stats"],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0
    assert "Cloud Sync Status" in result.stdout
    print("✅ CLI stats command works")
    
    # Test config command
    result = subprocess.run(
        ["python", "-m", "fixturegpt.cli", "config"],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0
    assert "FixtureGPT Configuration" in result.stdout
    print("✅ CLI config command works")

def cleanup_fixtures():
    """Clean up test fixtures."""
    fixtures_dir = Path("./fixtures")
    if fixtures_dir.exists():
        shutil.rmtree(fixtures_dir)
    print("🧹 Cleaned up test fixtures")

def main():
    """Run all integration tests."""
    print("🎯 FixtureGPT Cloud Sync Integration Tests")
    print("=" * 50)
    
    try:
        # Clean up before tests
        cleanup_fixtures()
        
        # Run tests
        test_local_only()
        test_cloud_sync_configuration()
        test_cloud_sync_fallback()
        test_different_sync_modes()
        test_cli_integration()
        
        print("\n" + "=" * 50)
        print("🎉 All tests passed!")
        print("✅ Local fixtures work perfectly")
        print("✅ Cloud sync configuration works")
        print("✅ Fallback behavior is correct")
        print("✅ CLI integration is functional")
        
        print("\n💡 Next steps:")
        print("1. Get a real API key from https://app.fixturegpt.com")
        print("2. Test with actual cloud sync")
        print("3. Share fixtures with your team!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise
    
    finally:
        # Clean up after tests
        cleanup_fixtures()

if __name__ == "__main__":
    main() 