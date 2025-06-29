"""Core FixtureGPT functionality for recording and replaying function outputs."""

import os
import json
import hashlib
import functools
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Tuple
from datetime import datetime


def _get_fixtures_dir() -> Path:
    """Get the fixtures directory, creating it if it doesn't exist."""
    fixtures_dir = Path("./fixtures")
    fixtures_dir.mkdir(exist_ok=True)
    return fixtures_dir


def _hash_inputs(args: Tuple, kwargs: Dict[str, Any]) -> str:
    """Create a SHA256 hash of the function inputs for deduplication."""
    # Convert args and kwargs to a stable string representation
    input_data = {
        "args": args,
        "kwargs": kwargs
    }
    
    # Sort kwargs for consistent hashing
    if kwargs:
        input_data["kwargs"] = dict(sorted(kwargs.items()))
    
    input_str = json.dumps(input_data, sort_keys=True, default=str)
    return hashlib.sha256(input_str.encode()).hexdigest()[:16]  # Use first 16 chars


def _is_json_serializable(obj: Any) -> bool:
    """Check if an object is JSON serializable."""
    try:
        json.dumps(obj, default=str)
        return True
    except (TypeError, ValueError):
        return False


def _save_fixture(name: str, args: Tuple, kwargs: Dict[str, Any], response: Any) -> str:
    """Save a fixture to disk and return the filename."""
    fixtures_dir = _get_fixtures_dir()
    hash_value = _hash_inputs(args, kwargs)
    filename = f"{name}-{hash_value}.json"
    filepath = fixtures_dir / filename
    
    fixture_data = {
        "name": name,
        "args": args,
        "kwargs": kwargs,
        "response": response,
        "timestamp": datetime.now().isoformat()
    }
    
    try:
        with open(filepath, 'w') as f:
            json.dump(fixture_data, f, indent=2, default=str)
        return filename
    except (TypeError, ValueError) as e:
        print(f"Warning: Could not serialize fixture {filename}: {e}")
        return ""


def _load_fixture(name: str, args: Tuple, kwargs: Dict[str, Any]) -> Optional[Any]:
    """Load a fixture from disk if it exists."""
    fixtures_dir = _get_fixtures_dir()
    hash_value = _hash_inputs(args, kwargs)
    filename = f"{name}-{hash_value}.json"
    filepath = fixtures_dir / filename
    
    if not filepath.exists():
        return None
    
    try:
        with open(filepath, 'r') as f:
            fixture_data = json.load(f)
        return fixture_data["response"]
    except (json.JSONDecodeError, KeyError, FileNotFoundError):
        return None


def snapshot(name: str, fn: Callable, *args, **kwargs) -> Any:
    """
    Record and replay expensive or variable function outputs.
    
    Args:
        name: User-defined label for the fixture (e.g., "user_summary")
        fn: Function to call (e.g., openai.ChatCompletion.create)
        *args: Positional arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function
    
    Returns:
        The function result (either recorded or replayed)
    
    Environment Variables:
        FIXTUREGPT_MODE: "record" to save outputs, "replay" to use saved outputs
    """
    mode = os.environ.get("FIXTUREGPT_MODE", "record").lower()
    
    if mode == "replay":
        # Try to load existing fixture
        cached_result = _load_fixture(name, args, kwargs)
        if cached_result is not None:
            print(f"📼 FixtureGPT: Replaying fixture '{name}'")
            return cached_result
        else:
            print(f"⚠️  FixtureGPT: No fixture found for '{name}', falling back to live call")
            mode = "record"  # Fall back to recording if no fixture exists
    
    if mode == "record":
        # Call the actual function
        print(f"🔴 FixtureGPT: Recording fixture '{name}'")
        try:
            result = fn(*args, **kwargs)
            
            # Save the fixture if serializable
            if _is_json_serializable(result):
                filename = _save_fixture(name, args, kwargs, result)
                if filename:
                    print(f"💾 FixtureGPT: Saved fixture as '{filename}'")
            else:
                print(f"⚠️  FixtureGPT: Result not JSON serializable, skipping save")
            
            return result
        except Exception as e:
            print(f"❌ FixtureGPT: Error calling function: {e}")
            raise
    
    else:
        raise ValueError(f"Invalid FIXTUREGPT_MODE: {mode}. Use 'record' or 'replay'")


def get_fixture_stats() -> Dict[str, Any]:
    """Get statistics about saved fixtures."""
    fixtures_dir = _get_fixtures_dir()
    
    if not fixtures_dir.exists():
        return {"count": 0, "total_size": 0, "fixtures": []}
    
    fixtures = list(fixtures_dir.glob("*.json"))
    total_size = sum(f.stat().st_size for f in fixtures)
    
    fixture_info = []
    for fixture_file in fixtures:
        try:
            with open(fixture_file, 'r') as f:
                data = json.load(f)
            fixture_info.append({
                "name": data.get("name", "unknown"),
                "filename": fixture_file.name,
                "timestamp": data.get("timestamp", "unknown"),
                "size": fixture_file.stat().st_size
            })
        except (json.JSONDecodeError, KeyError):
            continue
    
    return {
        "count": len(fixtures),
        "total_size": total_size,
        "fixtures": fixture_info
    }


def diff_fixture(name: str) -> Dict[str, Any]:
    """
    Re-run a function with stored args and compare with saved output.
    
    Args:
        name: The fixture name to diff
        
    Returns:
        Dict containing comparison results
    """
    fixtures_dir = _get_fixtures_dir()
    
    # Find all fixtures with the given name
    matching_fixtures = list(fixtures_dir.glob(f"{name}-*.json"))
    
    if not matching_fixtures:
        return {"error": f"No fixtures found with name '{name}'"}
    
    results = []
    for fixture_file in matching_fixtures:
        try:
            with open(fixture_file, 'r') as f:
                fixture_data = json.load(f)
            
            # Extract the original function call info
            original_response = fixture_data["response"]
            args = tuple(fixture_data.get("args", []))
            kwargs = fixture_data.get("kwargs", {})
            
            # Note: We can't actually re-run the function here because we don't have
            # access to the original function reference. This would need to be 
            # implemented at the application level.
            
            results.append({
                "filename": fixture_file.name,
                "timestamp": fixture_data.get("timestamp"),
                "args": args,
                "kwargs": kwargs,
                "original_response": original_response,
                "note": "Re-execution requires the original function reference"
            })
            
        except (json.JSONDecodeError, KeyError) as e:
            results.append({
                "filename": fixture_file.name,
                "error": f"Could not parse fixture: {e}"
            })
    
    return {"fixtures": results} 