import pytest
import pandas as pd
import numpy as np
from scripts.utils import categorize_lead_time, calculate_performance_delta
from scripts.data_cleaning_01 import clean_shipping_data

# --- UNIT TESTS FOR BUSINESS LOGIC ---

def test_categorize_lead_time():
    """Tests if shipping days are correctly bucketed into business categories."""
    assert categorize_lead_time(1) == 'Express'
    assert categorize_lead_time(4) == 'Standard'
    assert categorize_lead_time(10) == 'Delayed/Long-Haul'

def test_calculate_performance_delta():
    """Tests the percentage calculation for delivery variance."""
    # Actual 5, Scheduled 4 -> 25% late
    assert calculate_performance_delta(5, 4) == 25.0
    # Actual 2, Scheduled 4 -> -50% (Early)
    assert calculate_performance_delta(2, 4) == -50.0
    # Handle division by zero
    assert calculate_performance_delta(5, 0) == 0.0

# --- UNIT TESTS FOR DATA CLEANING ---

def test_clean_shipping_data_logic():
    """
    Tests if the cleaning script correctly filters negative days 
    and standardizes column names.
    """
    # Create a mock dataframe
    mock_data = pd.DataFrame({
        'DAYS FOR SHIPPING (REAL)': [5, -1, 3],
        'days for shipment (scheduled)': [4, 4, 4],
        'Shipping Mode': ['Standard', 'First Class', 'Second Class'],
        'Order City': ['London', np.nan, 'New York']
    })
    
    cleaned_df = clean_shipping_data(mock_data)
    
    # Check 1: Negative days should be removed
    assert cleaned_df.shape[0] == 2
    
    # Check 2: Column names should be snake_case
    assert 'days_for_shipping_real' in cleaned_df.columns
    
    # Check 3: Missing city should be 'Unknown'
    assert cleaned_df['order_city'].iloc[1] == 'Unknown'

# --- DATA INTEGRITY TEST ---

def test_no_missing_critical_values():
    """Ensures critical columns for EDA have no nulls after cleaning."""
    # This would typically load your processed CSV
    df = pd.read_csv('data/processed/cleaned_shipping_data.csv')
    critical_cols = ['days_for_shipping_real', 'shipping_mode', 'is_late']
    
    for col in critical_cols:
        if col in df.columns:
            assert df[col].isnull().sum() == 0