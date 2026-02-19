"""
update_impact.py
Update frequency impact analysis for Google Play Store dataset.

Goal:
- Parse last_updated and compute days_since_update relative to crawl date (June 2021 snapshot)
- Bucket apps into update-frequency ranges
- Compare rating and installs across buckets (overall and by category)
- Export Tableau-ready summaries

Expected columns (minimum):
- last_updated (date-like string)
- rating (numeric)
- min_installs (numeric)
- category (optional)
- rating_count (optional)
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


@dataclass
class UpdateImpactConfig:
    last_updated_col: str = "last_updated"
    rating_col: str = "rating"
    installs_col: str = "min_installs"
    category_col: str = "category"
    rating_count_col: str = "rating_count"

    # Snapshot date: dataset is a June 2021 scrape. Choose a consistent reference date.
    snapshot_date: str = "2021-06-30"

    # Filters
    min_rating_count: int = 1000
    min_installs: int = 1

    # Buckets
    bucket_labels: Tuple[str, ...] = (
        "< 30 days",
        "30–90 days",
        "90–180 days",
        "180–365 days",
        "1–2 years",
        "2+ years",
    )

    # Export and plotting
    export_dir: str = "reports/figures"
    export_summary_path: str = "reports/update_impact_summary.csv"
    export_category_path: str = "reports/update_impact_by_category.csv"
    make_plots: bool = True
    sample_n: int = 300_000
    random_state: int = 42


def _safe_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def _clean(df: pd.DataFrame, cfg: UpdateImpactConfig) -> pd.DataFrame:
    df = df.copy()

    if cfg.rating_col in df.columns:
        df[cfg.rating_col] = _safe_numeric(df[cfg.rating_col])
    if cfg.installs_col in df.columns:
        df[cfg.installs_col] = _safe_numeric(df[cfg.installs_col])
    if cfg.rating_count_col in df.columns:
        df[cfg.rating_count_col] = _safe_numeric(df[cfg.rating_count_col])

    if cfg.category_col in df.columns:
        df[cfg.category_col] = df[cfg.category_col].astype(str).str.strip()

    # Parse dates
    if cfg.last_updated_col not in df.columns:
        raise ValueError(f"Missing required column: {cfg.last_updated_col}")

    df[cfg.last_updated_col] = pd.to_datetime(df[cfg.last_updated_col], errors="coerce", utc=False)
    snapshot_dt = pd.to_datetime(cfg.snapshot_date)

    df["days_since_update"] = (snapshot_dt - df[cfg.last_updated_col]).dt.days

    # Filters
    keep = df["days_since_update"].notna()
    keep &= df["days_since_update"] >= 0

    if cfg.rating_col in df.columns:
        keep &= df[cfg.rating_col].between(0, 5, inclusive="both")
    if cfg.installs_col in df.columns:
        keep &= df[cfg.installs_col].fillna(0) >= cfg.min_installs

    if cfg.rating_count_col in df.columns and cfg.min_rating_count is not None:
        keep &= df[cfg.rating_count_col].fillna(0) >= cfg.min_rating_count

    return df.loc[keep].copy()


def bucket_days_since_update(days: pd.Series) -> pd.Series:
    """
    Buckets:
    <30, 30-90, 90-180, 180-365, 365-730, 730+
    """
    bins = [-1, 29, 90, 180, 365, 730, np.inf]
    labels = ["< 30 days", "30–90 days", "90–180 days", "180–365 days", "1–2 years", "2+ years"]
    return pd.cut(days, bins=bins, labels=labels, include_lowest=True)


def update_impact_summary(df: pd.DataFrame, cfg: Optional[UpdateImpactConfig] = None) -> pd.DataFrame:
    cfg = cfg or UpdateImpactConfig()
    dfc = _clean(df, cfg)

    dfc["update_bucket"] = bucket_days_since_update(dfc["days_since_update"])

    agg = (
        dfc.groupby("update_bucket", dropna=False)
        .agg(
            apps=("update_bucket", "size"),
            avg_days_since_update=("days_since_update", "mean"),
            median_days_since_update=("days_since_update", "median"),
            avg_rating=(cfg.rating_col, "mean"),
            median_rating=(cfg.rating_col, "median"),
            median_installs=(cfg.installs_col, "median"),
            mean_installs=(cfg.installs_col, "mean"),
        )
        .reset_index()
    )

    # Order buckets
    agg["update_bucket"] = pd.Categorical(agg["update_bucket"], categories=list(cfg.bucket_labels), ordered=True)
    agg = agg.sort_values("update_bucket").reset_index(drop=True)
    return agg


def update_impact_by_category(
    df: pd.DataFrame,
    cfg: Optional[UpdateImpactConfig] = None,
    min_apps_per_bucket: int = 100,
) -> pd.DataFrame:
    cfg = cfg or UpdateImpactConfig()
    dfc = _clean(df, cfg)

    if cfg.category_col not in dfc.columns:
        raise ValueError(f"Missing required column: {cfg.category_col}")

    dfc["update_bucket"] = bucket_days_since_update(dfc["days_since_update"])

    out = (
        dfc.groupby([cfg.category_col, "update_bucket"], dropna=False)
        .agg(
            apps=("update_bucket", "size"),
            avg_rating=(cfg.rating_col, "mean"),
            median_rating=(cfg.rating_col, "median"),
            median_installs=(cfg.installs_col, "median"),
            mean_installs=(cfg.installs_col, "mean"),
        )
        .reset_index()
    )

    out = out[out["apps"] >= min_apps_per_bucket].copy()

    out["update_bucket"] = pd.Categorical(out["update_bucket"], categories=list(cfg.bucket_labels), ordered=True)
    out = out.sort_values([cfg.category_col, "update_bucket"]).reset_index(drop=True)
    return out


def plot_rating_by_update_bucket(summary_df: pd.DataFrame, cfg: UpdateImpactConfig) -> Optional[str]:
    if summary_df.empty:
        return None

    x = summary_df["update_bucket"].astype(str).to_list()
    y = summary_df["avg_rating"].to_numpy()

    plt.figure()
    plt.plot(x, y, marker="o")
    plt.xticks(rotation=30, ha="right")
    plt.xlabel("Update frequency bucket")
    plt.ylabel("Average rating")
    plt.title("Average rating by update frequency bucket")
    plt.grid(True, linewidth=0.3, alpha=0.4)

    os.makedirs(cfg.export_dir, exist_ok=True)
    out_path = os.path.join(cfg.export_dir, "avg_rating_by_update_bucket.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=160)
    plt.close()
    return out_path


def run(
    df: pd.DataFrame,
    cfg: Optional[UpdateImpactConfig] = None,
) -> Tuple[pd.DataFrame, pd.DataFrame, Optional[str]]:
    cfg = cfg or UpdateImpactConfig()

    summary = update_impact_summary(df, cfg)
    by_cat = update_impact_by_category(df, cfg)

    if cfg.export_summary_path and not summary.empty:
        os.makedirs(os.path.dirname(cfg.export_summary_path), exist_ok=True)
        summary.to_csv(cfg.export_summary_path, index=False)

    if cfg.export_category_path and not by_cat.empty:
        os.makedirs(os.path.dirname(cfg.export_category_path), exist_ok=True)
        by_cat.to_csv(cfg.export_category_path, index=False)

    fig_path = None
    if cfg.make_plots:
        fig_path = plot_rating_by_update_bucket(summary, cfg)

    return summary, by_cat, fig_path


if __name__ == "__main__":
    raw_path = os.getenv("RAW_DATA_PATH", "data/raw/Google-Playstore.csv")
    processed_dir = os.getenv("PROCESSED_DATA_PATH_PARQUET", "data/processed/")
    processed_path = os.path.join(processed_dir, "playstore_clean.parquet")

    if os.path.exists(processed_path):
        df_ = pd.read_parquet(processed_path)
    else:
        df_ = pd.read_csv(raw_path, low_memory=False)

    cfg_ = UpdateImpactConfig()
    summary_df, by_category_df, fig_path = run(df_, cfg_)

    print("Update impact summary:")
    print(summary_df.head(20).to_string(index=False))

    if fig_path:
        print(f"Saved plot: {fig_path}")
