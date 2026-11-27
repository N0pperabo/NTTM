"""
NTTM_PLUS - Local Browsing Engine (Phase 1 preview)

هدف فاز ۱: اجرای کامل مرور روی سیستم خود کاربر با Playwright محلی
و سپس حالت اتصال به مرورگر فعلی کاربر از طریق CDP.

این فایل فعلاً یک اسکلت با امضای نهایی است؛ منطق واقعی Playwright
در فاز ۱ جایگزین می‌شود.
"""

import logging
from typing import Any, Callable, Dict, List, Optional, Tuple

from .config import BrowserConfig
from .engine import FetchEngine, FetchResult
from .session_manager import SessionManager

logger = logging.getLogger("LocalEngine")


class LocalEngine(FetchEngine):
    """
    Browsing engine that runs headless Chromium locally via Playwright.

    Phase 1 milestones:
    1. navigate + render + save page (parity with remote_runner.mjs)
    2. session transfer (cookies / storage) through SessionManager
    3. SPA actions, custom delay, auto scroll
    4. file downloads with the same FetchResult contract
    5. CDP attach mode to the user's running browser
    """

    name = "local"

    def __init__(self, config: BrowserConfig, session_manager: SessionManager):
        self.config = config
        self.session_manager = session_manager

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
        # TODO(Phase 1): real Playwright implementation.
        return FetchResult(
            success=False,
            error_message=(
                "موتور محلی هنوز پیاده‌سازی نشده است (فاز ۱). "
                "لطفاً فعلاً از موتور GitHub استفاده کنید."
            ),
        )
