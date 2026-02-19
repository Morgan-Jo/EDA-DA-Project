import pandas as pd
import numpy as np
import pytest

# Update these imports to match your actual function names
from src.data.feature_engineer import engineer_features


@pytest.fixture
def cleaned_like_df():
    """
    Synthetic already-clean-ish data that feature engineering can operate on.
    """
    return pd.DataFrame(
        {
            "app_id": ["a.one", "b.two", "c.three", "d.four"],
            "app_name": ["App One", "App Two", "App Three", "App Four"],
            "category": ["TOOLS", "GAME", "TOOLS", "EDUCATION"],
            "rating": [4.2, 4.8, 3.9, 4.0],
            "rating_count": [1200, 5000, 1500, 3000],
            "min_installs": [10_000, 1_000_000, 500, 50_000],
            "free": [True, True, False, True],
            "price": [0.0, 0.0, 2.99, 1.99],
            "ad_supported": [False, True, False, True],
            "in_app_purchases": [False, True, False, False],
            "last_updated": ["2021-06-01", "2021-06-29", "2020-06-01", "2019-06-30"],
        }
    )


def test_feature_engineer_returns_dataframe(cleaned_like_df):
    out = engineer_features(cleaned_like_df, snapshot_date="2021-06-30")
    assert isinstance(out, pd.DataFrame)


def test_feature_engineer_does_not_mutate_input(cleaned_like_df):
    original = cleaned_like_df.copy(deep=True)
    _ = engineer_features(cleaned_like_df, snapshot_date="2021-06-30")
    pd.testing.assert_frame_equal(cleaned_like_df, original)


def test_feature_engineer_expected_columns_exist(cleaned_like_df):
    out = engineer_features(cleaned_like_df, snapshot_date="2021-06-30")

    expected_cols = [
        "price_tier",
        "install_bucket",
        "days_since_update",
        "update_bucket",
        "monetisation_type",
    ]
    for c in expected_cols:
        assert c in out.columns, f"Missing expected engineered column: {c}"


def test_price_tier_logic(cleaned_like_df):
    out = engineer_features(cleaned_like_df, snapshot_date="2021-06-30")

    # Free apps should be labeled Free
    free_rows = out[out["price"] == 0]
    assert (free_rows["price_tier"] == "Free").all()

    # Paid apps should not be labeled Free
    paid_rows = out[out["price"] > 0]
    assert (paid_rows["price_tier"] != "Free").all()


def test_days_since_update_calculated(cleaned_like_df):
    out = engineer_features(cleaned_like_df, snapshot_date="2021-06-30")

    ds = out["days_since_update"]
    assert pd.api.types.is_numeric_dtype(ds), "days_since_update should be numeric"

    # Should be non-negative for dates before snapshot
    assert (ds.dropna() >= 0).all()


def test_update_bucket_values_reasonable(cleaned_like_df):
    out = engineer_features(cleaned_like_df, snapshot_date="2021-06-30")

    allowed = {"< 30 days", "30–90 days", "90–180 days", "180–365 days", "1–2 years", "2+ years"}
    buckets = set(out["update_bucket"].dropna().astype(str).unique())
    assert buckets.issubset(allowed), f"Unexpected update_bucket values: {buckets - allowed}"


def test_monetisation_type_logic(cleaned_like_df):
    out = engineer_features(cleaned_like_df, snapshot_date="2021-06-30")

    # Paid app should be "Paid"
    paid_row = out.loc[out["app_id"] == "c.three", "monetisation_type"].iloc[0]
    assert paid_row == "Paid"

    # Free + IAP should be IAP Freemium
    iap_row = out.loc[out["app_id"] == "b.two", "monetisation_type"].iloc[0]
    assert iap_row == "IAP Freemium"

    # Free + ads (no IAP) should be Ad-Supported
    ad_row = out.loc[out["app_id"] == "d.four", "monetisation_type"].iloc[0]
    assert ad_row == "Ad-Supported"

    # Free + no ads + no IAP should be Pure Free
    pure_row = out.loc[out["app_id"] == "a.one", "monetisation_type"].iloc[0]
    assert pure_row == "Pure Free"


def test_install_bucket_is_present_and_not_null(cleaned_like_df):
    out = engineer_features(cleaned_like_df, snapshot_date="2021-06-30")

    assert out["install_bucket"].isna().sum() == 0, "install_bucket should not be null for valid installs"
