"""
NTTM_PLUS - Engine Abstraction Layer (Phase 0)

این ماژول لایه‌ی موتور مرور را از مکانیزم انتقال (Transport) جدا می‌کند.
هر موتور (GitHub Actions، محلی، CDP و ...) باید اینترفیس FetchEngine را پیاده کند
تا UI بدون دانستن جزئیات، بتواند از هر موتوری استفاده کند.

Phase 0 contract:
- fetch(): اجباری؛ امضا و معناشی دقیقاً مشابه GitHubTransport.fetch
- daemon methods: اختیاری؛ کلاس پایه مقادیر «پشتیبانی‌نشده» برمی‌گرداند تا UI
  بتواند بدون چک کردن قابلیت، آن‌ها را صدا بزند.
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

logger = logging.getLogger("FetchEngine")


@dataclass
class FetchResult:
    """Represents the outcome of a fetch operation, regardless of engine."""

    success: bool
    response_type: str = "page"  # "page" or "file"
    index_html_path: Optional[str] = None
    downloaded_file_path: Optional[str] = None
    meta: Dict[str, Any] = field(default_factory=dict)
    error_message: str = ""


class FetchEngine(ABC):
    """
    Unified interface for every browsing engine.

    Any engine (GitHub Actions transport, local Playwright, CDP attach, ...)
    implements fetch() with the exact same signature as GitHubTransport.fetch
    so that the UI layer stays engine-agnostic.
    """

    name: str = "base"

    @abstractmethod
    def fetch(
        self,
        target_url: str,
        mode: str = "navigate",
        method: str = "GET",
        content_type: str = "",
        body_bytes: bytes = b"",
        actions: Optional[List[Dict[str, Any]]] = None,
        intercepted_ajax: Optional[Dict[str, Any]] = None,
        custom_headers: Optional[Dict[str, str]] = None,
        custom_delay_seconds: int = 0,
        custom_scroll_steps: int = 0,
        status_callback: Optional[Callable[[str], None]] = None,
    ) -> FetchResult:
        """Executes an end-to-end fetch and returns a FetchResult."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Optional daemon capability (engines with a persistent worker override)
    # ------------------------------------------------------------------
    def is_daemon_alive(self) -> bool:
        """Returns True if this engine keeps a persistent worker running."""
        return False

    def start_daemon(self, idle_timeout_min: int = 30) -> Tuple[bool, str]:
        return False, f"موتور '{self.name}' از رانر دائمی پشتیبانی نمی‌کند."

    def stop_daemon(self) -> Tuple[bool, str]:
        return False, f"موتور '{self.name}' از رانر دائمی پشتیبانی نمی‌کند."


class LocalEngineStub(FetchEngine):
    """
    Placeholder wired into the factory ahead of Phase 1.

    In Phase 1 this class will be replaced by a real local Playwright engine
    (client/local_engine.py) running on the user's own machine, plus a CDP
    attach mode targeting the user's existing browser.
    """

    name = "local"

    def fetch(
        self,
        target_url: str,
        mode: str = "navigate",
        method: str = "GET",
        content_type: str = "",
        body_bytes: bytes = b"",
        actions: Optional[List[Dict[str, Any]]] = None,
        intercepted_ajax: Optional[Dict[str, Any]] = None,
        custom_headers: Optional[Dict[str, str]] = None,
        custom_delay_seconds: int = 0,
        custom_scroll_steps: int = 0,
        status_callback: Optional[Callable[[str], None]] = None,
    ) -> FetchResult:
        return FetchResult(
            success=False,
            error_message=(
                "موتور محلی هنوز پیاده‌سازی نشده است (فاز ۱). "
                "لطفاً فعلاً از موتور GitHub استفاده کنید."
            ),
        )


# ----------------------------------------------------------------------
# Engine registry & factory
# ----------------------------------------------------------------------
# Deferred imports inside loaders keep module import order cycle-free:
#   engine.py -> (lazy) -> transport.py / local_engine.py -> engine.py
ENGINE_REGISTRY: Dict[str, str] = {
    "github": "GitHub Actions transport (موجود)",
    "local": "Playwright محلی روی سیستم کاربر (فاز ۱)",
}


def create_engine(
    engine_type: str, config, session_manager
) -> FetchEngine:
    """
    Builds the requested engine.

    engine_type: "github" | "local"
    """
    if engine_type == "github":
        # Lazy import: transport.py will later import FetchResult from here.
        from .transport import GitHubTransport

        return GitHubTransport(config=config, session_manager=session_manager)

    if engine_type == "local":
        from .local_engine import LocalEngine

        return LocalEngine(config=config, session_manager=session_manager)

    raise ValueError(
        f"موتور ناشناخته: '{engine_type}'. موتورهای موجود: {sorted(ENGINE_REGISTRY)}"
    )


def list_available_engines() -> Dict[str, str]:
    """Exposes the registry for UI dropdowns / settings screens."""
    return dict(ENGINE_REGISTRY)
