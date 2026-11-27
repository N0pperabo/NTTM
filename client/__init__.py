"""
GitHub-Based Offline Browser Client Module
"""

from .config import BrowserConfig
from .engine import FetchEngine, FetchResult, create_engine, list_available_engines
from .local_engine import LocalEngine
from .session_manager import SessionManager
from .transport import GitHubTransport

__all__ = [
    "BrowserConfig",
    "SessionManager",
    "GitHubTransport",
    "FetchResult",
    "FetchEngine",
    "LocalEngine",
    "create_engine",
    "list_available_engines",
]
