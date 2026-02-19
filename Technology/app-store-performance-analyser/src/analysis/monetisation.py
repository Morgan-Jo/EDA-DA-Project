"""
monetisation.py
Freemium vs paid model comparison.

Goal:
- Create monetisation archetypes using:
  free, ad_supported, in_app_purchases
- Compare installs and ratings across archetypes (overall and by category)
- Export Tableau-ready summaries

Expected columns (minimum):
- free (bool-like)
- ad_supported (bool-like)
- in_app_purchases (bool-like)
- rating (numeric)
- min_installs (numeric)
- category (optional)
- price (optional for paid segmentation)
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


@dataclass
class MonetisationConfig:
    free_col: str = "free"
    ad_col: str = "ad_supported"
    iap_col: str = "in_app_purchases"
    rating_col: str = "rating"
    installs_col: str = "min_installs"
    category_col: str = "category"
    price_col: str = "price"

    # Filters
    min_installs: int = 1
    min_rating_count: Optional[int] = None  # set if you want, requires rating_count col
    rating_count_col: str = "rating_count"

    # Export and plotting
    export_dir: str = "reports/figures"
    export_summary_path: str = "reports/monetisation_summary.csv"
    export_category_path: str = "reports/monetisation_by_category.csv"
    make_plots: bool = True


def _safe_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def _coerce_bool(series: pd.Series) -> pd.Series:
    if series.dtype == bool:
        return series
    s = series.astype(str).str.strip().str.lower()
    return s.isin(["true", "1", "yes", "y"])


def _clean(df: pd.DataFrame, cfg: MonetisationConfig) -> pd.DataFrame:
    df = df.copy()

    # Coerce required bools
    for c in [cfg.free_col, cfg.ad_col, cfg.iap_col]:
        if c in df.columns:
            df[c] = _coerce_bool(df[c])
        else:
            # If missing, assume False as safest default
            df[c] = False

    # Coerce numeric
    if cfg.rating_col in df.columns:
        df[cfg.rating_col] = _safe_numeric(df[cfg.rating_col])
    if cfg.installs_col in df.columns:
        df[cfg.installs_col] = _safe_numeric(df[cfg.installs_col])
    if cfg.price_col in df.columns:
        df[cfg.price_col] = _safe_numeric(df[cfg.price_col])

    if cfg.category_col in df.columns:
        df[cfg.category_col] = df[cfg.category_col].astype(str).str.strip()

    keep = df[cfg.installs_col].fillna(0) >= cfg.min_installs
    keep &= df[cfg.rating_col].between(0, 5, inclusive="both")

    if cfg.min_rating_count is not None and cfg.rating_count_col in df.columns:
        df[cfg.rating_count_col] = _safe_numeric(df[cfg.rating_count_col])
        keep &= df[cfg.rating_count_col].fillna(0) >= cfg.min_rating_count

    return df.loc[keep].copy()


def assign_archetype(row: pd.Series, cfg: MonetisationConfig) -> str:
    """
    Archetypes aligned to README:
    - Pure Free: free True, no ads, no IAP
    - Ad-Supported: free True, ads True, no IAP
    - IAP Freemium: free True, IAP True (ads optional)
    - Paid: free False (includes paid with or without IAP)
    """
    is_free = bool(row[cfg.free_col])
    has_ads = bool(row[cfg.ad_col])
    has_iap = bool(row[cfg.iap_col])

    if not is_free:
        return "Paid"
    if has_iap:
        return "IAP Freemium"
    if has_ads:
        return "Ad-Supported"
    return "Pure Free"


def monetisation_summary(df: pd.DataFrame, cfg: Optional[MonetisationConfig] = None) -> pd.DataFrame:
    cfg = cfg or MonetisationConfig()
    dfc = _clean(df, cfg)

    dfc["monetisation_type"] = dfc.apply(assign_archetype, axis=1, cfg=cfg)

    out = (
        dfc.groupby("monetisation_type", dropna=False)
        .agg(
            apps=("monetisation_type", "size"),
            avg_rating=(cfg.rating_col, "mean"),
            median_rating=(cfg.rating_col, "median"),
            median_installs=(cfg.installs_col, "median"),
            mean_installs=(cfg.installs_col, "mean"),
            share_of_apps=("monetisation_type", lambda s: len(s) / len(dfc)),
        )
        .reset_index()
    )

    order = ["Pure Free", "Ad-Supported", "IAP Freemium", "Paid"]
    out["monetisation_type"] = pd.Categorical(out["monetisation_type"], categories=order, ordered=True)
    out = out.sort_values("monetisation_type").reset_index(drop=True)

    return out


def monetisation_by_category(
    df: pd.DataFrame,
    cfg: Optional[MonetisationConfig] = None,
    min_apps: int = 200,
) -> pd.DataFrame:
    cfg = cfg or MonetisationConfig()
    dfc = _clean(df, cfg)

    if cfg.category_col not in dfc.columns:
        raise ValueError(f"Missing required column: {cfg.category_col}")

    dfc["monetisation_type"] = dfc.apply(assign_archetype, axis=1, cfg=cfg)

    out = (
        dfc.groupby([cfg.category_col, "monetisation_type"], dropna=False)
        .agg(
            apps=("monetisation_type", "size"),
            avg_rating=(cfg.rating_col, "mean"),
            median_rating=(cfg.rating_col, "median"),
            median_installs=(cfg.installs_col, "median"),
            mean_installs=(cfg.installs_col, "mean"),
        )
        .reset_index()
    )

    out = out[out["apps"] >= min_apps].copy()

    order = ["Pure Free", "Ad-Supported", "IAP Freemium", "Paid"]
    out["monetisation_type"] = pd.Categorical(out["monetisation_type"], categories=order, ordered=True)
    out = out.sort_values([cfg.category_col, "monetisation_type"]).reset_index(drop=True)
    return out


def plot_installs_by_monetisation(summary_df: pd.DataFrame, cfg: MonetisationConfig) -> Optional[str]:
    if summary_df.empty:
        return None

    x = summary_df["monetisation_type"].astype(str).to_list()
    y = summary_df["median_installs"].to_numpy()

    plt.figure()
    plt.bar(x, y)
    plt.yscale("log")
    plt.xlabel("Monetisation type")
    plt.ylabel("Median min_installs (log)")
    plt.title("Median installs by monetisation type")
    plt.grid(True, axis="y", linewidth=0.3, alpha=0.4)

    os.makedirs(cfg.export_dir, exist_ok=True)
    out_path = os.path.join(cfg.export_dir, "median_installs_by_monetisation.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=160)
    plt.close()
    return out_path


def run(
    df: pd.DataFrame,
    cfg: Optional[MonetisationConfig] = None,
) -> Tuple[pd.DataFrame, pd.DataFrame, Optional[str]]:
    cfg = cfg or MonetisationConfig()

    summary = monetisation_summary(df, cfg)
    by_cat = monetisation_by_category(df, cfg)

    if cfg.export_summary_path and not summary.empty:
        os.makedirs(os.path.dirname(cfg.export_summary_path), exist_ok=True)
        summary.to_csv(cfg.export_summary_path, index=False)

    if cfg.export_category_path and not by_cat.empty:
        os.makedirs(os.path.dirname(cfg.export_category_path), exist_ok=True)
        by_cat.to_csv(cfg.export_category_path, index=False)

    fig_path = None
    if cfg.make_plots:
        fig_path = plot_installs_by_monetisation(summary, cfg)

    return summary, by_cat, fig_path


if __name__ == "__main__":
    raw_path = os.getenv("RAW_DATA_PATH", "data/raw/Google-Playstore.csv")
    processed_dir = os.getenv("PROCESSED_DATA_PATH_PARQUET", "data/processed/")
    processed_path = os.path.join(processed_dir, "playstore_clean.parquet")

    if os.path.exists(processed_path):
        df_ = pd.read_parquet(processed_path)
    else:
        df_ = pd.read_csv(raw_path, low_memory=False)

    cfg_ = MonetisationConfig()
    summary_df, by_category_df, fig_path = run(df_, cfg_)

    print("Monetisation summary:")
    print(summary_df.to_string(index=False))

    if fig_path:
        print(f"Saved plot: {fig_path}")
