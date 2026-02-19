from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import numpy as np
import pandas as pd

from src.data.loader import get_paths, load_env, read_parquet, write_csv, write_parquet


@dataclass(frozen=True)
class FeatureConfig:
    snapshot_date: datetime


def _get_snapshot_date() -> datetime:
    """
    Uses env DATA_SNAPSHOT_DATE if provided, otherwise defaults to June 1st 2021.
    Format: YYYY-MM-DD
    """
    raw = os.getenv("DATA_SNAPSHOT_DATE", "2021-06-01")
    try:
        return datetime.strptime(raw, "%Y-%m-%d")
    except ValueError:
        return datetime(2021, 6, 1)


def _install_bucket(min_installs: pd.Series) -> pd.Categorical:
    """
    Bucket installs into readable ranges for Tableau filters and EDA comparisons.
    """
    x = min_installs.astype("Float64")

    bins = [-np.inf, 0, 10, 100, 1_000, 10_000, 100_000, 1_000_000, 10_000_000, 100_000_000, np.inf]
    labels = [
        "0",
        "1-10",
        "11-100",
        "101-1K",
        "1K-10K",
        "10K-100K",
        "100K-1M",
        "1M-10M",
        "10M-100M",
        "100M+",
    ]
    return pd.cut(x, bins=bins, labels=labels, ordered=True)


def _price_tier(price: pd.Series, free_flag: Optional[pd.Series] = None) -> pd.Categorical:
    """
    Create price tiers aligned to your README.
    Free / 0.99 / 1.99 / 2.99 / 4.99+ / 9.99+
    """
    p = price.astype("Float64")

    # If free flag exists, prefer it for correctness
    if free_flag is not None:
        is_free = free_flag.astype("boolean").fillna(False)
    else:
        is_free = (p.fillna(0) == 0)

    tier = pd.Series(pd.NA, index=p.index, dtype="string")
    tier.loc[is_free] = "Free"

    paid = ~is_free
    tier.loc[paid & (p > 0) & (p <= 0.99)] = "$0.99"
    tier.loc[paid & (p > 0.99) & (p <= 1.99)] = "$1.99"
    tier.loc[paid & (p > 1.99) & (p <= 2.99)] = "$2.99"
    tier.loc[paid & (p > 2.99) & (p <= 4.99)] = "$4.99"
    tier.loc[paid & (p > 4.99) & (p <= 9.99)] = "$9.99"
    tier.loc[paid & (p > 9.99)] = "$9.99+"

    # Order with Free first
    categories = ["Free", "$0.99", "$1.99", "$2.99", "$4.99", "$9.99", "$9.99+"]
    return pd.Categorical(tier, categories=categories, ordered=True)


def _update_bucket(days_since_update: pd.Series) -> pd.Categorical:
    x = days_since_update.astype("Float64")

    bins = [-np.inf, 30, 90, 180, 365, np.inf]
    labels = ["< 30 days", "30-90 days", "90-180 days", "180-365 days", "1 year+"]
    return pd.cut(x, bins=bins, labels=labels, ordered=True)


def _monetisation_archetype(
    free_flag: Optional[pd.Series],
    ad_supported: Optional[pd.Series],
    iap: Optional[pd.Series],
) -> pd.Categorical:
    """
    Four archetypes:
      Pure Free, Ad-Supported, IAP Freemium, Paid
    """
    idx = None
    for s in [free_flag, ad_supported, iap]:
        if s is not None:
            idx = s.index
            break
    if idx is None:
        return pd.Categorical([])

    free = free_flag.astype("boolean") if free_flag is not None else pd.Series(pd.NA, index=idx, dtype="boolean")
    ads = ad_supported.astype("boolean") if ad_supported is not None else pd.Series(pd.NA, index=idx, dtype="boolean")
    iap_s = iap.astype("boolean") if iap is not None else pd.Series(pd.NA, index=idx, dtype="boolean")

    free_filled = free.fillna(False)
    ads_filled = ads.fillna(False)
    iap_filled = iap_s.fillna(False)

    archetype = pd.Series(pd.NA, index=idx, dtype="string")

    archetype.loc[free_filled & ~ads_filled & ~iap_filled] = "Pure Free"
    archetype.loc[free_filled & ads_filled & ~iap_filled] = "Ad-Supported"
    archetype.loc[free_filled & iap_filled] = "IAP Freemium"
    archetype.loc[~free_filled] = "Paid"

    categories = ["Pure Free", "Ad-Supported", "IAP Freemium", "Paid"]
    return pd.Categorical(archetype, categories=categories, ordered=False)


def add_features(df: pd.DataFrame, cfg: FeatureConfig) -> pd.DataFrame:
    """
    Add analyst-friendly features for EDA and Tableau.
    Keeps everything additive so you can always trace back to raw fields.
    """
    out = df.copy()

    # Best available installs metric for analysis
    if "min_installs" in out.columns:
        installs_base = out["min_installs"]
    elif "installs" in out.columns:
        installs_base = out["installs"]
    else:
        installs_base = pd.Series(pd.NA, index=out.index, dtype="Int64")

    out["installs_base"] = installs_base.astype("Int64")
    out["install_bucket"] = _install_bucket(out["installs_base"])

    # Pricing
    price = out["price"] if "price" in out.columns else pd.Series(pd.NA, index=out.index, dtype="Float64")
    free_flag = out["free"] if "free" in out.columns else None
    out["price_tier"] = _price_tier(price, free_flag=free_flag)

    # Update cadence
    if "last_updated" in out.columns:
        snap = pd.Timestamp(cfg.snapshot_date)
        last_updated = pd.to_datetime(out["last_updated"], errors="coerce")
        out["days_since_update"] = (snap - last_updated).dt.days.astype("Int64")
        out.loc[out["days_since_update"] < 0, "days_since_update"] = pd.NA
        out["update_bucket"] = _update_bucket(out["days_since_update"])
    else:
        out["days_since_update"] = pd.Series(pd.NA, index=out.index, dtype="Int64")
        out["update_bucket"] = pd.Categorical([pd.NA] * len(out))

    # Rating group for quick slicing
    if "rating" in out.columns:
        r = out["rating"].astype("Float64")
        out["rating_band"] = pd.cut(
            r,
            bins=[-np.inf, 2.5, 3.5, 4.0, 4.5, np.inf],
            labels=["< 2.5", "2.5-3.5", "3.5-4.0", "4.0-4.5", "4.5+"],
            ordered=True,
        )
    else:
        out["rating_band"] = pd.Categorical([pd.NA] * len(out))

    # Monetisation archetype
    out["monetisation_archetype"] = _monetisation_archetype(
        free_flag=out["free"] if "free" in out.columns else None,
        ad_supported=out["ad_supported"] if "ad_supported" in out.columns else None,
        iap=out["in_app_purchases"] if "in_app_purchases" in out.columns else None,
    )

    # Revenue proxy (clearly labelled as proxy, not real revenue)
    # Use installs_base * price for paid apps as a simple proxy.
    out["revenue_proxy"] = pd.Series(pd.NA, index=out.index, dtype="Float64")
    if "price" in out.columns:
        p = out["price"].astype("Float64")
        installs = out["installs_base"].astype("Float64")
        is_paid = out["price_tier"].astype("string") != "Free"
        out.loc[is_paid, "revenue_proxy"] = (p * installs).astype("Float64")

    return out


def run_feature_pipeline(env_path: Optional[str] = None) -> None:
    """
    Reads processed parquet, adds features, writes final exports for Tableau.
    """
    load_env(env_path)
    paths = get_paths()

    df = read_parquet(paths.processed_parquet)
    cfg = FeatureConfig(snapshot_date=_get_snapshot_date())
    df_feat = add_features(df, cfg)

    # Save to exports
    write_parquet(df_feat, paths.export_parquet)
    write_csv(df_feat, paths.export_csv)


if __name__ == "__main__":
    run_feature_pipeline()
    print("Feature engineering complete. Tableau exports written to data/exports/.")
