from __future__ import annotations

import os
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

from src.data.loader import get_paths, load_env, read_raw_csv, write_csv, write_parquet


@dataclass(frozen=True)
class CleaningReport:
    input_rows: int
    output_rows: int
    dropped_duplicates: int
    invalid_app_id: int
    invalid_rating: int
    invalid_price: int
    invalid_installs: int


def _to_bool(series: pd.Series) -> pd.Series:
    """Convert common boolean encodings to pandas boolean dtype."""
    if series.dtype == "bool":
        return series
    s = series.astype("string").str.strip().str.lower()
    mapping = {
        "true": True,
        "false": False,
        "1": True,
        "0": False,
        "yes": True,
        "no": False,
        "y": True,
        "n": False,
    }
    out = s.map(mapping)
    return out.astype("boolean")


def _parse_size_to_mb(size: pd.Series) -> pd.Series:
    """
    Convert size strings to MB.
    Examples: '12M', '850k', 'Varies with device'
    """
    s = size.astype("string").str.strip()

    # Normalize
    s = s.replace({"Varies with device": pd.NA, "": pd.NA, "nan": pd.NA})

    def _convert(val: str) -> Optional[float]:
        if val is None or val == "<NA>":
            return None
        v = str(val).strip().lower()
        if not v:
            return None
        # Handle plain numbers as MB assumption
        try:
            return float(v)
        except Exception:
            pass

        m = re.match(r"^([0-9]*\.?[0-9]+)\s*([kmgb])$", v)
        if not m:
            return None
        num = float(m.group(1))
        unit = m.group(2)

        if unit == "k":
            return num / 1024.0
        if unit == "m":
            return num
        if unit == "g":
            return num * 1024.0
        if unit == "b":
            # bytes to MB
            return num / (1024.0 * 1024.0)
        return None

    return s.map(_convert).astype("Float64")


def _parse_currency_price(price: pd.Series) -> pd.Series:
    """
    Ensure price is numeric (float) in its existing currency column.
    The Kaggle dataset usually provides `price` already numeric, but we harden it anyway.
    """
    s = price.astype("string").str.strip()

    # Remove currency symbols if present
    s = s.str.replace(r"[^0-9\.\-]", "", regex=True)
    out = pd.to_numeric(s, errors="coerce")
    return out.astype("Float64")


def _parse_installs(installs: pd.Series) -> pd.Series:
    """
    Parse installs like '1,000,000+' into int.
    Some datasets already provide min_installs/max_installs, but installs is still useful.
    """
    s = installs.astype("string").str.strip()
    s = s.replace({"": pd.NA, "nan": pd.NA})
    s = s.str.replace("+", "", regex=False)
    s = s.str.replace(",", "", regex=False)
    out = pd.to_numeric(s, errors="coerce")
    return out.astype("Int64")


def _parse_android_version(min_android: pd.Series) -> pd.Series:
    """
    Keep a simplified minimum android requirement as float, where possible.
    Examples: '5.0 and up', 'Varies with device'
    """
    s = min_android.astype("string").str.strip().str.lower()
    s = s.replace({"varies with device": pd.NA, "": pd.NA, "nan": pd.NA})
    s = s.str.extract(r"([0-9]+(?:\.[0-9]+)?)", expand=False)
    out = pd.to_numeric(s, errors="coerce")
    return out.astype("Float64")


def _parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Parse date columns safely."""
    for col in ["released", "last_updated"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce", utc=True).dt.tz_convert(None)
    return df


def clean_playstore(df: pd.DataFrame) -> tuple[pd.DataFrame, CleaningReport]:
    """
    Core cleaning pipeline.
    Keeps raw columns, standardises types, and removes obvious invalids.
    """
    input_rows = len(df)

    # Basic column hygiene
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]

    # Fix common typo in column list: developer_email developer_website missing comma
    if "developer_email developer_website" in df.columns and "developer_email" not in df.columns:
        # If the source column exists as a merged name, rename it to something workable.
        df = df.rename(columns={"developer_email developer_website": "developer_email_website"})

    # Dedupe (app_id should be unique, but scraped data often has duplicates)
    before_dupes = len(df)
    if "app_id" in df.columns:
        df["app_id"] = df["app_id"].astype("string").str.strip()
        df = df.drop_duplicates(subset=["app_id"], keep="first")
    else:
        df = df.drop_duplicates(keep="first")
    dropped_duplicates = before_dupes - len(df)

    # app_id validity
    invalid_app_id = 0
    if "app_id" in df.columns:
        invalid_mask = df["app_id"].isna() | (df["app_id"].str.len() == 0)
        invalid_app_id = int(invalid_mask.sum())
        df = df.loc[~invalid_mask].copy()

    # Types and parsing
    if "rating" in df.columns:
        df["rating"] = pd.to_numeric(df["rating"], errors="coerce").astype("Float64")

    if "rating_count" in df.columns:
        df["rating_count"] = pd.to_numeric(df["rating_count"], errors="coerce").astype("Int64")

    if "installs" in df.columns:
        df["installs"] = _parse_installs(df["installs"])

    if "min_installs" in df.columns:
        df["min_installs"] = pd.to_numeric(df["min_installs"], errors="coerce").astype("Int64")

    if "max_installs" in df.columns:
        df["max_installs"] = pd.to_numeric(df["max_installs"], errors="coerce").astype("Int64")

    if "free" in df.columns:
        df["free"] = _to_bool(df["free"])

    if "ad_supported" in df.columns:
        df["ad_supported"] = _to_bool(df["ad_supported"])

    if "in_app_purchases" in df.columns:
        df["in_app_purchases"] = _to_bool(df["in_app_purchases"])

    if "editors_choice" in df.columns:
        df["editors_choice"] = _to_bool(df["editors_choice"])

    if "price" in df.columns:
        df["price"] = _parse_currency_price(df["price"])

    if "size" in df.columns:
        df["size_mb"] = _parse_size_to_mb(df["size"])

    if "min_android" in df.columns:
        df["min_android_version"] = _parse_android_version(df["min_android"])

    df = _parse_dates(df)

    # Standardise strings
    for col in ["app_name", "category", "developer", "content_rating", "currency", "market_territory"]:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip()

    # Validity checks and caps
    invalid_rating = 0
    if "rating" in df.columns:
        invalid_rating_mask = (df["rating"] < 0) | (df["rating"] > 5)
        invalid_rating = int(invalid_rating_mask.sum())
        df.loc[invalid_rating_mask, "rating"] = pd.NA

    invalid_price = 0
    if "price" in df.columns:
        invalid_price_mask = (df["price"] < 0) | (df["price"] > 1000)
        invalid_price = int(invalid_price_mask.sum())
        df.loc[invalid_price_mask, "price"] = pd.NA

    invalid_installs = 0
    for col in ["installs", "min_installs", "max_installs"]:
        if col in df.columns:
            bad = df[col].notna() & (df[col] < 0)
            invalid_installs += int(bad.sum())
            df.loc[bad, col] = pd.NA

    # Basic derived sanity: ensure min_installs <= max_installs when both exist
    if "min_installs" in df.columns and "max_installs" in df.columns:
        bad_range = df["min_installs"].notna() & df["max_installs"].notna() & (df["min_installs"] > df["max_installs"])
        if bad_range.any():
            # swap where clearly inverted
            min_vals = df.loc[bad_range, "min_installs"].copy()
            df.loc[bad_range, "min_installs"] = df.loc[bad_range, "max_installs"]
            df.loc[bad_range, "max_installs"] = min_vals

    report = CleaningReport(
        input_rows=input_rows,
        output_rows=len(df),
        dropped_duplicates=dropped_duplicates,
        invalid_app_id=invalid_app_id,
        invalid_rating=invalid_rating,
        invalid_price=invalid_price,
        invalid_installs=invalid_installs,
    )
    return df, report


def run_cleaning_pipeline(
    env_path: Optional[str] = None,
    sample_rows: Optional[int] = None,
) -> CleaningReport:
    """
    Entry point used by:
      python src/data/cleaner.py
    """
    load_env(env_path)
    paths = get_paths()

    df_raw = read_raw_csv(paths.raw_csv, nrows=sample_rows)
    df_clean, report = clean_playstore(df_raw)

    # Write processed outputs
    write_parquet(df_clean, paths.processed_parquet)
    write_csv(df_clean, paths.processed_csv)

    return report


if __name__ == "__main__":
    # Optional: allow sampling for quick local tests
    sample = os.getenv("SAMPLE_ROWS")
    sample_rows = int(sample) if sample and sample.isdigit() else None

    rep = run_cleaning_pipeline(sample_rows=sample_rows)
    print(
        "Cleaning complete\n"
        f"Input rows: {rep.input_rows}\n"
        f"Output rows: {rep.output_rows}\n"
        f"Dropped duplicates: {rep.dropped_duplicates}\n"
        f"Invalid app_id removed: {rep.invalid_app_id}\n"
        f"Invalid ratings set to null: {rep.invalid_rating}\n"
        f"Invalid prices set to null: {rep.invalid_price}\n"
        f"Invalid installs set to null: {rep.invalid_installs}\n"
    )
