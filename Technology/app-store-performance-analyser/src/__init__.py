"""
App Store Performance Analyser

A portfolio EDA project using Python, SQL (DuckDB/SQLite), and Tableau.
This package contains reusable code for data loading, cleaning, feature
engineering, analysis, and exports.
"""

from __future__ import annotations

__all__ = [
    "__version__",
    "get_version",
]

__version__ = "0.1.0"


def get_version() -> str:
    """Return the current package version."""
    return __version__
