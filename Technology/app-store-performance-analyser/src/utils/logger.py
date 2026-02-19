"""
logger.py
Centralised logging using Loguru.

Usage:
from src.utils.logger import get_logger
logger = get_logger()
logger.info("Hello")
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional

from loguru import logger as _logger


DEFAULT_LOG_DIR = Path("reports/logs")
DEFAULT_LOG_FILE = "app_store_analyser.log"


def _env(name: str, default: str) -> str:
    v = os.getenv(name)
    return v if v is not None and str(v).strip() != "" else default


def get_logger(
    name: str = "app-store-performance-analyser",
    log_dir: str | Path = DEFAULT_LOG_DIR,
    log_file: str = DEFAULT_LOG_FILE,
    level: Optional[str] = None,
    rotation: str = "10 MB",
    retention: str = "10 days",
    backtrace: bool = False,
    diagnose: bool = False,
):
    """
    Returns a configured Loguru logger.

    Env vars:
    - LOG_LEVEL: DEBUG | INFO | WARNING | ERROR
    """
    # Remove default handlers to avoid duplicate logs in notebooks
    _logger.remove()

    log_level = (level or _env("LOG_LEVEL", "INFO")).upper()

    # Console sink
    _logger.add(
        sys.stdout,
        level=log_level,
        enqueue=True,
        backtrace=backtrace,
        diagnose=diagnose,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>",
    )

    # File sink
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    file_path = log_dir / log_file

    _logger.add(
        str(file_path),
        level=log_level,
        rotation=rotation,
        retention=retention,
        enqueue=True,
        backtrace=backtrace,
        diagnose=diagnose,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    )

    # Bind name for clarity (optional)
    return _logger.bind(app=name)
