import sqlite3
import pandas as pd
import logging
from datetime import datetime

# --- LOGGING SETUP ---
# Standardizes how errors are reported across all scripts
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='docs/project_log.log'
)

def get_db_connection(db_path: str):
    """Creates a thread-safe connection to the SQLite database."""
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        logging.error(f"Database connection failed: {e}")
        return None

def format_shipping_dates(df: pd.DataFrame, date_cols: list) -> pd.DataFrame:
    """
    Ensures all date columns are in datetime format.
    Handles common supply chain date formats (MM/DD/YYYY and YYYY-MM-DD).
    """
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

def categorize_lead_time(days: int) -> str:
    """
    Business Logic: Categorizes shipping speed based on industry benchmarks.
    """
    if days <= 2:
        return 'Express'
    elif 3 <= days <= 5:
        return 'Standard'
    else:
        return 'Delayed/Long-Haul'

def calculate_performance_delta(actual: float, scheduled: float) -> float:
    """
    Calculates the percentage variance between scheduled and actual delivery.
    Positive = Late, Negative = Early.
    """
    if scheduled == 0:
        return 0.0
    return round(((actual - scheduled) / scheduled) * 100, 2)

def save_summary_to_markdown(df: pd.DataFrame, filename: str, title: str):
    """
    Automatically generates a Markdown table for your GitHub README 
    or documentation updates.
    """
    with open(f"docs/{filename}.md", 'w') as f:
        f.write(f"## {title}\n\n")
        f.write(df.to_markdown(index=False))
    logging.info(f"Summary saved to docs/{filename}.md")