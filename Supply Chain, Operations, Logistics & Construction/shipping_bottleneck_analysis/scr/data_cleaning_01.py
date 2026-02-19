import pandas as pd
import numpy as np
import sqlite3
import os
from typing import Tuple

# --- CONFIGURATION ---
RAW_DATA_PATH = 'data/raw/DataCoSupplyChainDataset.csv'
PROCESSED_DATA_PATH = 'data/processed/cleaned_shipping_data.csv'
DB_PATH = 'database/shipping_logistics.db'

def load_and_audit(path: str) -> pd.DataFrame:
    """Loads dataset and performs an initial integrity check."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Dataset not found at {path}")
    
    df = pd.read_csv(path, encoding='ISO-8859-1')
    print(f"Initial Load: {df.shape[0]} rows, {df.shape[1]} columns")
    return df

def clean_shipping_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes column names, handles missing values, and fixes 
    data type inconsistencies for shipping analysis.
    """
    # 1. Standardize column names (Lowercase, snake_case)
    df.columns = [col.lower().replace(' ', '_').replace('(', '').replace(')', '') for col in df.columns]

    # 2. Subset relevant columns for Bottleneck Analysis
    # Focused on: Dates, Port/Region, Carrier, and Scheduled vs Real days
    cols_to_keep = [
        'type', 'days_for_shipping_real', 'days_for_shipment_scheduled',
        'delivery_status', 'late_delivery_risk', 'category_name',
        'order_city', 'order_country', 'order_region', 'shipping_mode'
    ]
    df = df[cols_to_keep].copy()

    # 3. Handle Missing Values
    # Fill missing weather or city data with 'Unknown' to maintain row count
    df['order_city'] = df['order_city'].fillna('Unknown')

    # 4. Remove logical errors
    # Real shipping days cannot be negative
    df = df[df['days_for_shipping_real'] >= 0]

    return df

def export_to_sql(df: pd.DataFrame, db_name: str):
    """Stores the cleaned data into a SQLite table for summary_stats.sql access."""
    conn = sqlite3.connect(db_name)
    try:
        df.to_sql('shipping_data', conn, if_exists='replace', index=False)
        print(f"Successfully exported {len(df)} rows to {db_name}")
    finally:
        conn.close()

def main():
    """Main execution pipeline."""
    try:
        # Load
        raw_df = load_and_audit(RAW_DATA_PATH)
        
        # Transform
        clean_df = clean_shipping_data(raw_df)
        
        # Save CSV for Tableau/PowerBI or local backup
        clean_df.to_csv(PROCESSED_DATA_PATH, index=False)
        
        # Save to SQL for the summary_stats.sql logic
        export_to_sql(clean_df, DB_PATH)
        
        print("Pipeline completed successfully.")
        
    except Exception as e:
        print(f"Pipeline failed: {e}")

if __name__ == "__main__":
    main()