import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3

# --- SETTINGS ---
DB_PATH = 'database/shipping_logistics.db'
sns.set_theme(style="whitegrid")  # Professional, clean aesthetic

def fetch_data_from_db(query: str) -> pd.DataFrame:
    """Connects to the local database and returns a dataframe."""
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(query, conn)

def plot_late_rate_by_method(df: pd.DataFrame):
    """
    Visualizes the Late Delivery Rate across different Shipping Methods.
    Includes a 'Target' line for business benchmarking.
    """
    plt.figure(figsize=(10, 6))
    
    # Calculate means and sort for a cleaner visual flow
    order = df.groupby('shipping_mode')['is_late'].mean().sort_values(ascending=False).index

    # 1. Bar Plot for Late Rate
    ax = sns.barplot(
        x='shipping_mode', 
        y='is_late', 
        data=df, 
        order=order, 
        palette='viridis',
        errorbar=None # Focus on the mean for non-technical clarity
    )

    # Add labels and formatting
    plt.title('Late Delivery Rate by Shipping Method', fontsize=15, pad=20)
    plt.xlabel('Shipping Method', fontsize=12)
    plt.ylabel('Late Delivery Rate (Percentage)', fontsize=12)
    
    # Format Y-axis as percentage
    vals = ax.get_yticks()
    ax.set_yticklabels(['{:,.0%}'.format(x) for x in vals])

    # 2. Add a 'Business Goal' line (e.g., Target late rate < 10%)
    plt.axhline(0.1, color='red', linestyle='--', label='Max Acceptable Delay (10%)')
    plt.legend()

    plt.tight_layout()
    plt.savefig('docs/late_rate_by_method.png')
    plt.show()

def plot_weather_impact_heatmap(df: pd.DataFrame):
    """
    Analyzes the interaction between Shipping Method and Delivery Risk.
    This helps identify if 'First Class' shipping is resilient to issues.
    """
    # Create a pivot table for the heatmap
    pivot = df.pivot_table(
        index='shipping_mode', 
        columns='late_delivery_risk', 
        values='is_late', 
        aggfunc='mean'
    )

    plt.figure(figsize=(8, 5))
    sns.heatmap(pivot, annot=True, cmap='YlOrRd', fmt=".1%")
    plt.title('Risk Probability Heatmap: Mode vs. Late Rate', fontsize=14)
    plt.savefig('docs/risk_heatmap.png')
    plt.show()

def main():
    # Fetch the view created in our SQL script
    query = "SELECT shipping_mode, late_delivery_risk, is_late FROM v_shipping_performance"
    
    try:
        df = fetch_data_from_db(query)
        
        # Run Visualization Functions
        plot_late_rate_by_method(df)
        plot_weather_impact_heatmap(df)
        
        print("Visualizations generated and saved to /docs/")
        
    except Exception as e:
        print(f"Error generating visuals: {e}")

if __name__ == "__main__":
    main()