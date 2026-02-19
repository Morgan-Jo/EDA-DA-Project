from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

import pandas as pd

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover
    load_dotenv = None


PathLike = Union[str, Path]


@dataclass(frozen=True)
class DataPaths:
    raw_csv: Path
    processed_parquet: Path
    processed_csv: Path
    export_parquet: Path
    export_csv: Path
    sqlite_db: Path
    duckdb_db: Path


def load_env(env_path: Optional[PathLike] = None) -> None:
    """Load environment variables from a .env file if python-dotenv is available."""
    if load_dotenv is None:
        return
    if env_path is None:
        load_dotenv()
        return
    load_dotenv(dotenv_path=str(env_path))


def get_paths(project_root: Optional[PathLike] = None) -> DataPaths:
    """
    Build standardised project paths from environment variables.
    Falls back to sensible defaults that match your repo structure.
    """
    root = Path(project_root) if project_root else Path.cwd()

    raw_csv = Path(os.getenv("RAW_DATA_PATH", "data/raw/Google-Playstore.csv"))
    processed_parquet = Path(os.getenv("PROCESSED_PARQUET_PATH", "data/processed/playstore_clean.parquet"))
    processed_csv = Path(os.getenv("PROCESSED_CSV_PATH", "data/processed/playstore_clean.csv"))
    export_parquet = Path(os.getenv("EXPORT_PARQUET_PATH", "data/exports/playstore_final.parquet"))
    export_csv = Path(os.getenv("EXPORT_CSV_PATH", "data/exports/playstore_final.csv"))

    sqlite_db = Path(os.getenv("SQLITE_DB_PATH", "data/processed/playstore.db"))
    duckdb_db = Path(os.getenv("DUCKDB_PATH", "data/processed/playstore.duckdb"))

    # Make paths relative to root if they are relative
    def _abs(p: Path) -> Path:
        return p if p.is_absolute() else (root / p)

    return DataPaths(
        raw_csv=_abs(raw_csv),
        processed_parquet=_abs(processed_parquet),
        processed_csv=_abs(processed_csv),
        export_parquet=_abs(export_parquet),
        export_csv=_abs(export_csv),
        sqlite_db=_abs(sqlite_db),
        duckdb_db=_abs(duckdb_db),
    )


def read_raw_csv(
    csv_path: PathLike,
    usecols: Optional[list[str]] = None,
    nrows: Optional[int] = None,
    low_memory: bool = True,
) -> pd.DataFrame:
    """
    Load the raw Kaggle CSV.
    For large files, keep this lean: select columns when prototyping in notebooks.
    """
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Raw CSV not found: {csv_path}")

    # dtype inference is okay initially; we will cast properly in cleaner.py
    df = pd.read_csv(
        csv_path,
        usecols=usecols,
        nrows=nrows,
        low_memory=low_memory,
    )
    return df


def read_parquet(parquet_path: PathLike) -> pd.DataFrame:
    parquet_path = Path(parquet_path)
    if not parquet_path.exists():
        raise FileNotFoundError(f"Parquet not found: {parquet_path}")
    return pd.read_parquet(parquet_path)


def write_parquet(df: pd.DataFrame, parquet_path: PathLike) -> None:
    parquet_path = Path(parquet_path)
    parquet_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(parquet_path, index=False)


def write_csv(df: pd.DataFrame, csv_path: PathLike) -> None:
    csv_path = Path(csv_path)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(csv_path, index=False)
