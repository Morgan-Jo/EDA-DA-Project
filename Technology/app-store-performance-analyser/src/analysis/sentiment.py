"""
sentiment.py
Text sentiment scoring using TextBlob on app descriptions (proxy signal).

Outputs:
- polarity and subjectivity scores per app
- correlation between description polarity and rating
- export of sentiment-enriched dataset for downstream analysis

Expected columns:
- description (preferred) or app_name (fallback, not meaningful)
- rating
- min_installs (optional)
- category (optional)
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np
import pandas as pd
from scipy import stats

from textblob import TextBlob

import matplotlib.pyplot as plt


@dataclass
class SentimentConfig:
    text_col: str = "description"  # change if your dataset uses a different name
    rating_col: str = "rating"
    installs_col: str = "min_installs"
    category_col: str = "category"

    # Filters
    min_text_len: int = 20
    sample_n: int = 400_000  # TextBlob over 2.3M rows is slow, sample for speed
    random_state: int = 42

    # Export and plotting
    export_dir: str = "reports/figures"
    export_sentiment_path: str = "data/processed/playstore_with_sentiment.parquet"
    export_summary_path: str = "reports/sentiment_summary.csv"
    make_plots: bool = True


def _safe_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def _clean(df: pd.DataFrame, cfg: SentimentConfig) -> pd.DataFrame:
    df = df.copy()

    if cfg.rating_col in df.columns:
        df[cfg.rating_col] = _safe_numeric(df[cfg.rating_col])

    if cfg.installs_col in df.columns:
        df[cfg.installs_col] = _safe_numeric(df[cfg.installs_col])

    if cfg.category_col in df.columns:
        df[cfg.category_col] = df[cfg.category_col].astype(str).str.strip()

    if cfg.text_col not in df.columns:
        raise ValueError(
            f"Missing text column '{cfg.text_col}'. "
            f"Update SentimentConfig.text_col to match your dataset."
        )

    df[cfg.text_col] = df[cfg.text_col].astype(str)
    df["text_len"] = df[cfg.text_col].str.len()

    keep = df["text_len"] >= cfg.min_text_len
    if cfg.rating_col in df.columns:
        keep &= df[cfg.rating_col].between(0, 5, inclusive="both")

    return df.loc[keep].copy()


def _score_text(text: str) -> Tuple[float, float]:
    """
    Returns (polarity, subjectivity).
    TextBlob polarity: [-1, 1], subjectivity: [0, 1]
    """
    try:
        blob = TextBlob(text)
        return float(blob.sentiment.polarity), float(blob.sentiment.subjectivity)
    except Exception:
        return np.nan, np.nan


def score_sentiment(df: pd.DataFrame, cfg: Optional[SentimentConfig] = None) -> pd.DataFrame:
    cfg = cfg or SentimentConfig()
    dfc = _clean(df, cfg)

    # Sample for speed
    if cfg.sample_n and len(dfc) > cfg.sample_n:
        dfc = dfc.sample(n=cfg.sample_n, random_state=cfg.random_state)

    scores = dfc[cfg.text_col].apply(_score_text)
    dfc["sentiment_polarity"] = scores.apply(lambda t: t[0])
    dfc["sentiment_subjectivity"] = scores.apply(lambda t: t[1])

    return dfc


def sentiment_summary(df_scored: pd.DataFrame, cfg: Optional[SentimentConfig] = None) -> pd.DataFrame:
    cfg = cfg or SentimentConfig()

    dfc = df_scored.copy()
    dfc = dfc.dropna(subset=["sentiment_polarity", cfg.rating_col])

    if dfc.empty:
        return pd.DataFrame()

    x = dfc["sentiment_polarity"].to_numpy()
    y = dfc[cfg.rating_col].to_numpy()

    pearson_r, pearson_p = stats.pearsonr(x, y)
    spearman_r, spearman_p = stats.spearmanr(x, y)

    out = pd.DataFrame(
        [
            {
                "n": int(len(dfc)),
                "avg_polarity": float(np.nanmean(x)),
                "avg_subjectivity": float(np.nanmean(dfc["sentiment_subjectivity"].to_numpy())),
                "pearson_r_polarity_vs_rating": float(pearson_r),
                "pearson_p": float(pearson_p),
                "spearman_r_polarity_vs_rating": float(spearman_r),
                "spearman_p": float(spearman_p),
            }
        ]
    )
    return out


def plot_polarity_vs_rating(df_scored: pd.DataFrame, cfg: SentimentConfig) -> Optional[str]:
    dfc = df_scored.dropna(subset=["sentiment_polarity", cfg.rating_col]).copy()
    if dfc.empty:
        return None

    x = dfc["sentiment_polarity"].to_numpy()
    y = dfc[cfg.rating_col].to_numpy()

    plt.figure()
    plt.scatter(x, y, s=8, alpha=0.2)
    plt.xlabel("Description sentiment polarity (TextBlob)")
    plt.ylabel("Rating")
    plt.title("Sentiment polarity vs rating")
    plt.grid(True, linewidth=0.3, alpha=0.4)

    os.makedirs(cfg.export_dir, exist_ok=True)
    out_path = os.path.join(cfg.export_dir, "sentiment_polarity_vs_rating.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=160)
    plt.close()
    return out_path


def run(
    df: pd.DataFrame,
    cfg: Optional[SentimentConfig] = None,
) -> Tuple[pd.DataFrame, pd.DataFrame, Optional[str]]:
    cfg = cfg or SentimentConfig()

    scored = score_sentiment(df, cfg)
    summary = sentiment_summary(scored, cfg)

    # Exports
    if cfg.export_sentiment_path:
        os.makedirs(os.path.dirname(cfg.export_sentiment_path), exist_ok=True)
        scored.to_parquet(cfg.export_sentiment_path, index=False)

    if cfg.export_summary_path and not summary.empty:
        os.makedirs(os.path.dirname(cfg.export_summary_path), exist_ok=True)
        summary.to_csv(cfg.export_summary_path, index=False)

    fig_path = None
    if cfg.make_plots:
        fig_path = plot_polarity_vs_rating(scored, cfg)

    return scored, summary, fig_path


if __name__ == "__main__":
    raw_path = os.getenv("RAW_DATA_PATH", "data/raw/Google-Playstore.csv")
    processed_dir = os.getenv("PROCESSED_DATA_PATH_PARQUET", "data/processed/")
    processed_path = os.path.join(processed_dir, "playstore_clean.parquet")

    if os.path.exists(processed_path):
        df_ = pd.read_parquet(processed_path)
    else:
        df_ = pd.read_csv(raw_path, low_memory=False)

    cfg_ = SentimentConfig()

    # If your dataset uses a different description field name, set it here:
    # cfg_.text_col = "app_desc"

    scored_df, summary_df, fig_path = run(df_, cfg_)

    print("Sentiment summary:")
    if summary_df.empty:
        print("No sentiment summary produced. Check text_col and filtering.")
    else:
        print(summary_df.to_string(index=False))

    if fig_path:
        print(f"Saved plot: {fig_path}")
    print(f"Saved sentiment parquet: {cfg_.export_sentiment_path}")
