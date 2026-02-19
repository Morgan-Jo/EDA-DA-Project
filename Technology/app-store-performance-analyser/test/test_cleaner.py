import pandas as pd
import numpy as np
import pytest

# Update these imports to match your actual function names
from src.data.cleaner import clean_dataframe


@pytest.fixture
def raw_df_minimal():
    """
    Minimal synthetic input that mimics a few key Play Store columns
    with common data issues: strings for numbers, bad dates, nulls, booleans as text.
    """
    return pd.DataFrame(
        {
            "app_id": ["a.one", "b.two", "c.three"],
            "app_name": ["App One", "App Two", "App Three"],
            "category": ["TOOLS", "GAME", "TOOLS"],
            "rating": ["4.2", "not_a_number", "5"],
            "rating_count": ["1200", None, "5000"],
            "min_installs": ["10000", "0", None],
            "max_installs": ["50000", "10", "100"],
            "free": ["True", "False", "true"],
            "price": ["0", "2.99", "-1"],  # negative should be handled or set null
            "ad_supported": ["FALSE", "True", None],
            "in_app_purchases": ["0", "1", "yes"],
            "last_updated": ["2021-06-01", "bad_date", "2021/06/20"],
        }
    )


def test_cleaner_returns_dataframe(raw_df_minimal):
    cleaned = clean_dataframe(raw_df_minimal)
    assert isinstance(cleaned, pd.DataFrame)


def test_cleaner_does_not_mutate_input(raw_df_minimal):
    raw_copy = raw_df_minimal.copy(deep=True)
    _ = clean_dataframe(raw_df_minimal)
    pd.testing.assert_frame_equal(raw_df_minimal, raw_copy)


def test_cleaner_numeric_columns_cast(raw_df_minimal):
    cleaned = clean_dataframe(raw_df_minimal)

    # These should be numeric after cleaning
    for col in ["rating", "rating_count", "min_installs", "max_installs", "price"]:
        assert col in cleaned.columns, f"Missing expected column: {col}"
        assert pd.api.types.is_numeric_dtype(cleaned[col]), f"{col} should be numeric dtype"


def test_cleaner_boolean_columns_cast(raw_df_minimal):
    cleaned = clean_dataframe(raw_df_minimal)

    for col in ["free", "ad_supported", "in_app_purchases"]:
        assert col in cleaned.columns, f"Missing expected column: {col}"
        # In pandas, bool dtype can become 'boolean' (nullable) depending on implementation
        assert (
            pd.api.types.is_bool_dtype(cleaned[col])
            or str(cleaned[col].dtype) == "boolean"
        ), f"{col} should be boolean or nullable boolean dtype"


def test_cleaner_rating_range_enforced(raw_df_minimal):
    cleaned = clean_dataframe(raw_df_minimal)

    # Any non-null ratings should be between 0 and 5
    ratings = cleaned["rating"].dropna()
    assert ((ratings >= 0) & (ratings <= 5)).all()


def test_cleaner_installs_non_negative(raw_df_minimal):
    cleaned = clean_dataframe(raw_df_minimal)

    installs = cleaned["min_installs"].dropna()
    assert (installs >= 0).all()


def test_cleaner_last_updated_parsed_or_null(raw_df_minimal):
    cleaned = clean_dataframe(raw_df_minimal)

    assert "last_updated" in cleaned.columns

    # Accept either datetime dtype or object if you store it as string consistently,
    # but bad dates should become null-like (NaT/None/NaN).
    bad_row = cleaned.loc[cleaned["app_id"] == "b.two", "last_updated"].iloc[0]

    if pd.api.types.is_datetime64_any_dtype(cleaned["last_updated"]):
        assert pd.isna(bad_row)
    else:
        # If you keep it as string, ensure bad date got nulled or removed
        assert bad_row in [None, ""] or (isinstance(bad_row, float) and np.isnan(bad_row)) or pd.isna(bad_row)


def test_cleaner_negative_prices_handled(raw_df_minimal):
    cleaned = clean_dataframe(raw_df_minimal)

    # Negative prices should not survive as negative numbers
    prices = cleaned["price"].dropna()
    assert (prices >= 0).all()
