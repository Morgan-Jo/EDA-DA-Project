"""
correlation.py
Rating vs installs correlation analysis for Google Play Store dataset.

Outputs:
- Correlation stats (Pearson + Spearman) overall and by category
- Optional scatter plot (rating vs min_installs) with log-scaled installs axis
- Optional CSV export of category-level correlations

Expected columns (minimum):
- rating
- min_installs
- category (optional for by-category breakdown)
- rating_count (optional for filtering)
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np
import pandas as pd
from scipy import stats

import matplotlib.pyplot as plt


@dataclass
class CorrelationConfig:
    min_rating_count: int = 1000
    min_installs_col: str = "min_installs"
    rating_col: str = "rating"
    category_col: str = "category"
    rating_count_col: str = "rating_count"

    # Plotting
    make_plot: bool = True
    sample_n: int = 200_000  # large datasets: sample for plotting
    random_state: int = 42

    # Exports
    export_dir: str = "reports/figures"
    export_csv_path: str = "reports/correlation_by_category.csv"


def _safe_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def _clean_for_correlation(df: pd.DataFrame, cfg: CorrelationConfig) -> pd.DataFrame:
    df = df.copy()

    # Coerce key columns
    if cfg.rating_col in df.columns:
        df[cfg.rating_col] = _safe_numeric(df[cfg.rating_col])
    if cfg.min_installs_col in df.columns:
        df[cfg.min_installs_col] = _safe_numeric(df[cfg.min_installs_col])
    if cfg.rating_count_col in df.columns:
        df[cfg.rating_count_col] = _safe_numeric(df[cfg.rating_count_col])

    # Basic validity filters
    keep = df[cfg.rating_col].between(0, 5, inclusive="both") if cfg.rating_col in df.columns else pd.Series(False, index=df.index)
    keep &= df[cfg.min_installs_col].notna() if cfg.min_installs_col in df.columns else False
    keep &= df[cfg.min_installs_col] > 0

    # Optional: rating_count threshold
    if cfg.rating_count_col in df.columns and cfg.min_rating_count is not None:
        keep &= df[cfg.rating_count_col].fillna(0) >= cfg.min_rating_count

    df = df.loc[keep].dropna(subset=[cfg.rating_col, cfg.min_installs_col])

    # Optional category cleanup
    if cfg.category_col in df.columns:
        df[cfg.category_col] = df[cfg.category_col].astype(str).str.strip()

    return df


def compute_correlations(
    df: pd.DataFrame,
    cfg: Optional[CorrelationConfig] = None,
) -> dict:
    """
    Returns a dictionary with overall Pearson/Spearman correlations and p-values.
    """
    cfg = cfg or CorrelationConfig()
    dfc = _clean_for_correlation(df, cfg)

    x = dfc[cfg.rating_col].to_numpy()
    y = dfc[cfg.min_installs_col].to_numpy()

    pearson_r, pearson_p = stats.pearsonr(x, y)
    spearman_r, spearman_p = stats.spearmanr(x, y)

    return {
        "n": int(len(dfc)),
        "pearson_r": float(pearson_r),
        "pearson_p": float(pearson_p),
        "spearman_r": float(spearman_r),
        "spearman_p": float(spearman_p),
    }


def correlations_by_category(
    df: pd.DataFrame,
    cfg: Optional[CorrelationConfig] = None,
    min_rows_per_category: int = 300,
) -> pd.DataFrame:
    """
    Computes Pearson/Spearman correlations per category.
    Returns a tidy DataFrame.
    """
    cfg = cfg or CorrelationConfig()
    dfc = _clean_for_correlation(df, cfg)

    if cfg.category_col not in dfc.columns:
        raise ValueError(f"Missing required column for by-category analysis: {cfg.category_col}")

    rows = []
    for cat, g in dfc.groupby(cfg.category_col, dropna=True):
        if len(g) < min_rows_per_category:
            continue

        x = g[cfg.rating_col].to_numpy()
        y = g[cfg.min_installs_col].to_numpy()

        try:
            pearson_r, pearson_p = stats.pearsonr(x, y)
        except Exception:
            pearson_r, pearson_p = np.nan, np.nan

        try:
            spearman_r, spearman_p = stats.spearmanr(x, y)
        except Exception:
            spearman_r, spearman_p = np.nan, np.nan

        rows.append(
            {
                "category": cat,
                "n": int(len(g)),
                "pearson_r": pearson_r,
                "pearson_p": pearson_p,
                "spearman_r": spearman_r,
                "spearman_p": spearman_p,
                "avg_rating": float(np.nanmean(x)),
                "median_installs": float(np.nanmedian(y)),
            }
        )

    out = pd.DataFrame(rows)
    if not out.empty:
        out = out.sort_values(["spearman_r", "n"], ascending=[False, False]).reset_index(drop=True)
    return out


def plot_rating_vs_installs(
    df: pd.DataFrame,
    cfg: Optional[CorrelationConfig] = None,
    title: str = "Rating vs Min Installs (log scale)",
    save_name: str = "rating_vs_installs.png",
) -> Optional[str]:
    """
    Scatter plot rating vs installs using log-scaled installs axis.
    Returns saved file path if saved.
    """
    cfg = cfg or CorrelationConfig()
    dfc = _clean_for_correlation(df, cfg)

    if dfc.empty:
        return None

    # Sample for performance
    if cfg.sample_n and len(dfc) > cfg.sample_n:
        dfp = dfc.sample(n=cfg.sample_n, random_state=cfg.random_state)
    else:
        dfp = dfc

    x = dfp[cfg.min_installs_col].to_numpy()
    y = dfp[cfg.rating_col].to_numpy()

    plt.figure()
    plt.scatter(x, y, s=6, alpha=0.2)
    plt.xscale("log")
    plt.xlabel(cfg.min_installs_col)
    plt.ylabel(cfg.rating_col)
    plt.title(title)
    plt.grid(True, which="both", linewidth=0.3, alpha=0.4)

    os.makedirs(cfg.export_dir, exist_ok=True)
    out_path = os.path.join(cfg.export_dir, save_name)
    plt.tight_layout()
    plt.savefig(out_path, dpi=160)
    plt.close()

    return out_path


def run(
    df: pd.DataFrame,
    cfg: Optional[CorrelationConfig] = None,
) -> Tuple[dict, pd.DataFrame, Optional[str]]:
    """
    Convenience runner to compute overall stats, category stats, and an optional plot.
    """
    cfg = cfg or CorrelationConfig()

    overall = compute_correlations(df, cfg)
    by_cat = correlations_by_category(df, cfg)

    plot_path = None
    if cfg.make_plot:
        plot_path = plot_rating_vs_installs(df, cfg)

    # Optional export
    if cfg.export_csv_path and not by_cat.empty:
        os.makedirs(os.path.dirname(cfg.export_csv_path), exist_ok=True)
        by_cat.to_csv(cfg.export_csv_path, index=False)

    return overall, by_cat, plot_path


if __name__ == "__main__":
    # Minimal CLI example using env var PROCESSED_DATA_PATH_PARQUET or RAW_DATA_PATH
    raw_path = os.getenv("RAW_DATA_PATH", "data/raw/Google-Playstore.csv")
    processed_dir = os.getenv("PROCESSED_DATA_PATH_PARQUET", "data/processed/")
    processed_path = os.path.join(processed_dir, "playstore_clean.parquet")

    if os.path.exists(processed_path):
        df_ = pd.read_parquet(processed_path)
    else:
        df_ = pd.read_csv(raw_path, low_memory=False)

    cfg_ = CorrelationConfig()
    overall_stats, by_category_df, fig_path = run(df_, cfg_)

    print("Overall correlation stats:")
    for k, v in overall_stats.items():
        print(f"  {k}: {v}")

    if fig_path:
        print(f"Saved plot: {fig_path}")

    if not by_category_df.empty:
        print(f"Saved category correlations CSV: {cfg_.export_csv_path}")
        print(by_category_df.head(10).to_string(index=False))
