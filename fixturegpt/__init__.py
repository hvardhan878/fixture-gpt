"""FixtureGPT - Record and replay expensive or variable outputs for AI/LLM development."""

from .main import snapshot, configure_cloud_sync

__version__ = "0.1.1"
__all__ = ["snapshot", "configure_cloud_sync"] 