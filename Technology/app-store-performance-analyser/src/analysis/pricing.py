"""
pricing.py
Pricing strategy analysis for Google Play Store dataset.

Core ideas:
- Bucket apps into price tiers
- Compare installs and revenue proxy across tiers (overall and by category)
- Generate Tableau-friendly summary exports

Expected columns (minimum):
- price (numeric)
- min_installs (numeric)
- free (bool-like)
- category (optional)

Notes:
- "Revenue proxy" is not real revenue. A simple proxy is price * min_installs for paid apps.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional, List, Tuple

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


@dataclass
class PricingConfig:
    price_col: str = "price"
    installs_col: str = "min_installs"
    free_col: str = "free"
    category_col: str = "category"

    # Filters
    min_installs: int = 1
    drop_free_from_paid_analysis: bool = True

    # Price tiers (USD-like, since Kaggle often uses USD pricing)
    # You can tune these after you inspect the distribution.
    tier_edges: Tuple[float, ...] = (0.0, 0.99, 1.99, 2.99, 4.99, 9.99, 19.99, 49.99, np.inf)
    tier_labels: Tuple[str, ...] = (
        "Free",
        "0.01–0.99",
        "1.00–1.99",
        "2.00–2.99",
        "3.00–4.99",
        "5.00–9.99",
        "10.00–19.99",
        "20.00–49.99",
        "50+",
    )

    # Plotting and exports
    export_dir: str = "reports/figures"
    export_summary_path: str = "reports/pricing_summary.csv"
    export_category_path: str = "reports/pricing_by_category.csv"
    make_plots: bool = True


def _safe_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def _coerce_bool(series: pd.Series) -> pd.Series:
    # Handles True/False, "True"/"False", 0/1, "0"/"1"
    if series.dtype == bool:
        return series
    s = series.astype(str).str.strip().str.lower()
    return s.isin(["true", "1", "yes", "y"])


def _clean_for_pricing(df: pd.DataFrame, cfg: PricingConfig) -> pd.DataFrame:
    df = df.copy()

    if cfg.price_col in df.columns:
        df[cfg.price_col] = _safe_numeric(df[cfg.price_col])
    else:
        raise ValueError(f"Missing required column: {cfg.price_col}")

    if cfg.installs_col in df.columns:
        df[cfg.installs_col] = _safe_numeric(df[cfg.installs_col])
    else:
        raise ValueError(f"Missing required column: {cfg.installs_col}")

    if cfg.free_col in df.columns:
        df[cfg.free_col] = _coerce_bool(df[cfg.free_col])
    else:
        # If free column not present, infer from price == 0
        df[cfg.free_col] = df[cfg.price_col].fillna(0).eq(0)

    if cfg.category_col in df.columns:
        df[cfg.category_col] = df[cfg.category_col].astype(str).str.strip()

    # basic filters
    df = df[df[cfg.installs_col].fillna(0) >= cfg.min_installs]
    df = df[df[cfg.price_col].notna()]
    df = df[df[cfg.price_col] >= 0]

    return df


def add_price_tiers(df: pd.DataFrame, cfg: Optional[PricingConfig] = None) -> pd.DataFrame:
    cfg = cfg or PricingConfig()
    dfc = _clean_for_pricing(df, cfg)

    # price tiers include free as a separate label
    # We treat price == 0 as Free, otherwise bucket.
    price = dfc[cfg.price_col].to_numpy()

    tier = pd.cut(
        price,
        bins=list(cfg.tier_edges),
        labels=list(cfg.tier_labels),
        include_lowest=True,
        right=True,
    ).astype(str)

    # Ensure true Free label for price==0
    tier = np.where(dfc[cfg.price_col].eq(0), "Free", tier)

    dfc["price_tier"] = tier

    # Revenue proxy: paid only
    dfc["revenue_proxy"] = np.where(
        dfc[cfg.price_col].gt(0),
        dfc[cfg.price_col] * dfc[cfg.installs_col],
        0.0,
    )

    return dfc


def pricing_summary(df: pd.DataFrame, cfg: Optional[PricingConfig] = None) -> pd.DataFrame:
    """
    Overall summary by price tier.
    """
    cfg = cfg or PricingConfig()
    dfc = add_price_tiers(df, cfg)

    # Paid-only analysis if requested
    if cfg.drop_free_from_paid_analysis:
        paid = dfc[dfc[cfg.price_col] > 0].copy()
    else:
        paid = dfc.copy()

    if paid.empty:
        return pd.DataFrame()

    out = (
        paid.groupby("price_tier", dropna=False)
        .agg(
            apps=("price_tier", "size"),
            median_price=(cfg.price_col, "median"),
            median_installs=(cfg.installs_col, "median"),
            mean_installs=(cfg.installs_col, "mean"),
            median_revenue_proxy=("revenue_proxy", "median"),
            mean_revenue_proxy=("revenue_proxy", "mean"),
        )
        .reset_index()
    )

    # Order tiers using cfg labels, excluding Free if paid-only
    tier_order: List[str] = list(cfg.tier_labels)
    if cfg.drop_free_from_paid_analysis and "Free" in tier_order:
        tier_order.remove("Free")

    out["price_tier"] = pd.Categorical(out["price_tier"], categories=tier_order, ordered=True)
    out = out.sort_values("price_tier").reset_index(drop=True)

    return out


def pricing_by_category(df: pd.DataFrame, cfg: Optional[PricingConfig] = None, min_apps_per_bucket: int = 50) -> pd.DataFrame:
    """
    Summary by category and price tier.
    Useful for Tableau heatmaps (installs by tier x category).
    """
    cfg = cfg or PricingConfig()
    dfc = add_price_tiers(df, cfg)

    if cfg.category_col not in dfc.columns:
        raise ValueError(f"Missing required column for category breakdown: {cfg.category_col}")

    if cfg.drop_free_from_paid_analysis:
        dfc = dfc[dfc[cfg.price_col] > 0]

    out = (
        dfc.groupby([cfg.category_col, "price_tier"], dropna=False)
        .agg(
            apps=("price_tier", "size"),
            median_price=(cfg.price_col, "median"),
            median_installs=(cfg.installs_col, "median"),
            mean_installs=(cfg.installs_col, "mean"),
            median_revenue_proxy=("revenue_proxy", "median"),
            mean_revenue_proxy=("revenue_proxy", "mean"),
        )
        .reset_index()
    )

    out = out[out["apps"] >= min_apps_per_bucket].copy()

    # Tier ordering
    tier_order: List[str] = list(cfg.tier_labels)
    if cfg.drop_free_from_paid_analysis and "Free" in tier_order:
        tier_order.remove("Free")

    out["price_tier"] = pd.Categorical(out["price_tier"], categories=tier_order, ordered=True)
    out = out.sort_values([cfg.category_col, "price_tier"]).reset_index(drop=True)

    return out


def plot_installs_by_price_tier(
    summary_df: pd.DataFrame,
    cfg: Optional[PricingConfig] = None,
    save_name: str = "installs_by_price_tier.png",
) -> Optional[str]:
    """
    Simple plot: median installs by price tier.
    """
    cfg = cfg or PricingConfig()
    if summary_df.empty:
        return None

    x = summary_df["price_tier"].astype(str).to_list()
    y = summary_df["median_installs"].to_numpy()

    plt.figure()
    plt.plot(x, y, marker="o")
    plt.yscale("log")
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Price tier")
    plt.ylabel("Median min_installs (log)")
    plt.title("Median installs by price tier")
    plt.grid(True, which="both", linewidth=0.3, alpha=0.4)

    os.makedirs(cfg.export_dir, exist_ok=True)
    out_path = os.path.join(cfg.export_dir, save_name)
    plt.tight_layout()
    plt.savefig(out_path, dpi=160)
    plt.close()

    return out_path


def run(
    df: pd.DataFrame,
    cfg: Optional[PricingConfig] = None,
) -> Tuple[pd.DataFrame, pd.DataFrame, Optional[str]]:
    """
    Convenience runner:
    - overall pricing summary
    - pricing summary by category
    - optional plot
    - CSV exports for Tableau
    """
    cfg = cfg or PricingConfig()

    summary = pricing_summary(df, cfg)
    by_cat = pricing_by_category(df, cfg)

    # exports
    if cfg.export_summary_path and not summary.empty:
        os.makedirs(os.path.dirname(cfg.export_summary_path), exist_ok=True)
        summary.to_csv(cfg.export_summary_path, index=False)

    if cfg.export_category_path and not by_cat.empty:
        os.makedirs(os.path.dirname(cfg.export_category_path), exist_ok=True)
        by_cat.to_csv(cfg.export_category_path, index=False)

    fig_path = None
    if cfg.make_plots:
        fig_path = plot_installs_by_price_tier(summary, cfg)

    return summary, by_cat, fig_path


if __name__ == "__main__":
    raw_path = os.getenv("RAW_DATA_PATH", "data/raw/Google-Playstore.csv")
    processed_dir = os.getenv("PROCESSED_DATA_PATH_PARQUET", "data/processed/")
    processed_path = os.path.join(processed_dir, "playstore_clean.parquet")

    if os.path.exists(processed_path):
        df_ = pd.read_parquet(processed_path)
    else:
        df_ = pd.read_csv(raw_path, low_memory=False)

    cfg_ = PricingConfig()
    summary_df, by_category_df, fig_path = run(df_, cfg_)

    print("Pricing summary (by tier):")
    if summary_df.empty:
        print("No rows after filtering. Check price/min_installs columns and filters.")
    else:
        print(summary_df.to_string(index=False))

    if fig_path:
        print(f"Saved plot: {fig_path}")

    if not by_category_df.empty:
        print(f"Saved category pricing CSV: {cfg_.export_category_path}")
