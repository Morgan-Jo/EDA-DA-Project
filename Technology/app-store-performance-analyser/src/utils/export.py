"""
export.py
File export utilities for CSV, Parquet, and Excel.

Use cases:
- Save processed datasets to data/processed or data/exports
- Save small summary tables for Tableau or README reporting
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Union

import pandas as pd


@dataclass
class ExportConfig:
    processed_dir: str = "data/processed"
    exports_dir: str = "data/exports"


def _ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def export_csv(
    df: pd.DataFrame,
    filename: str,
    out_dir: str | Path,
    index: bool = False,
    encoding: str = "utf-8",
) -> str:
    out_dir = _ensure_dir(out_dir)
    out_path = out_dir / filename
    df.to_csv(out_path, index=index, encoding=encoding)
    return str(out_path)


def export_parquet(
    df: pd.DataFrame,
    filename: str,
    out_dir: str | Path,
    index: bool = False,
) -> str:
    out_dir = _ensure_dir(out_dir)
    out_path = out_dir / filename
    df.to_parquet(out_path, index=index)
    return str(out_path)


def export_excel(
    sheets: Dict[str, pd.DataFrame],
    filename: str,
    out_dir: str | Path,
    index: bool = False,
) -> str:
    """
    Export multiple DataFrames to one Excel file with named sheets.
    """
    out_dir = _ensure_dir(out_dir)
    out_path = out_dir / filename

    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        for sheet_name, df in sheets.items():
            safe_name = str(sheet_name)[:31]  # Excel sheet name limit
            df.to_excel(writer, sheet_name=safe_name, index=index)

    return str(out_path)


def export_tableau_ready(
    df: pd.DataFrame,
    base_name: str,
    cfg: Optional[ExportConfig] = None,
    to_csv: bool = True,
    to_parquet: bool = True,
) -> Dict[str, str]:
    """
    Convenience exporter for Tableau-ready outputs.

    Returns dict with keys: csv, parquet if created.
    """
    cfg = cfg or ExportConfig()
    outputs: Dict[str, str] = {}

    if to_csv:
        outputs["csv"] = export_csv(df, f"{base_name}.csv", cfg.exports_dir, index=False)

    if to_parquet:
        outputs["parquet"] = export_parquet(df, f"{base_name}.parquet", cfg.exports_dir, index=False)

    return outputs


def export_processed_dataset(
    df: pd.DataFrame,
    base_name: str = "playstore_clean",
    cfg: Optional[ExportConfig] = None,
    to_csv: bool = True,
    to_parquet: bool = True,
) -> Dict[str, str]:
    """
    Save processed data to data/processed for downstream analysis scripts.
    """
    cfg = cfg or ExportConfig()
    outputs: Dict[str, str] = {}

    if to_csv:
        outputs["csv"] = export_csv(df, f"{base_name}.csv", cfg.processed_dir, index=False)

    if to_parquet:
        outputs["parquet"] = export_parquet(df, f"{base_name}.parquet", cfg.processed_dir, index=False)

    return outputs
