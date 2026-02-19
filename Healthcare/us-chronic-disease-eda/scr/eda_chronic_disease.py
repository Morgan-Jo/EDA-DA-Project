import os
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Config
# -----------------------------
DATA_PATH = "data/U.S._Chronic_Disease_Indicators.csv"
OUTPUT_DIR = "outputs"
PLOTS_DIR = os.path.join(OUTPUT_DIR, "plots")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv(DATA_PATH)

print("\nDataset loaded successfully\n")

# -----------------------------
# 1) Understand Data Structure
# -----------------------------
print("First 5 rows:")
print(df.head())

print("\nDataset shape:", df.shape)

print("\nColumn info:")
print(df.info())

missing = df.isnull().sum().sort_values(ascending=False)
print("\nMissing values per column (top 20):")
print(missing.head(20))

missing.to_csv(os.path.join(OUTPUT_DIR, "missing_values.csv"))

# Plot: Missing values (Top 20)
top_missing = missing.head(20)
plt.figure(figsize=(10, 6))
top_missing.sort_values().plot(kind="barh")
plt.title("Top 20 Columns by Missing Values")
plt.xlabel("Missing Count")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "missing_values_top20.png"), dpi=200)
plt.close()

# -----------------------------
# 2) Summary Statistics
# -----------------------------
summary_stats = df.describe(include="all")
summary_stats.to_csv(os.path.join(OUTPUT_DIR, "summary_statistics.csv"))
print("\nSaved summary statistics to outputs/summary_statistics.csv")

# -----------------------------
# 3) Detect Anomalies (Outliers) for DataValue if present
# -----------------------------
anomalies = pd.DataFrame()

if "DataValue" in df.columns:
    # Ensure numeric
    df["DataValue"] = pd.to_numeric(df["DataValue"], errors="coerce")

    values = df["DataValue"].dropna()

    if len(values) > 0:
        # Z-score method
        z_scores = np.abs(stats.zscore(values))
        outliers_z = values[z_scores > 3]

        # IQR method
        Q1 = values.quantile(0.25)
        Q3 = values.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers_iqr = values[(values < lower_bound) | (values > upper_bound)]

        print(f"\nOutliers detected using Z-score: {len(outliers_z)}")
        print(f"Outliers detected using IQR: {len(outliers_iqr)}")
        print(f"IQR bounds: [{lower_bound:.3f}, {upper_bound:.3f}]")

        anomalies = df[df["DataValue"].isin(outliers_iqr)].copy()
        anomalies.to_csv(os.path.join(OUTPUT_DIR, "anomalies_detected.csv"), index=False)

        # Plot: Distribution of DataValue
        plt.figure(figsize=(10, 6))
        sns.histplot(values, bins=40, kde=True)
        plt.title("Distribution of DataValue")
        plt.xlabel("DataValue")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, "datavalue_distribution.png"), dpi=200)
        plt.close()

        # Plot: DataValue by Year (if Year exists)
        if "Year" in df.columns:
            df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

            year_series = (
                df.dropna(subset=["Year", "DataValue"])
                  .groupby("Year")["DataValue"]
                  .mean()
                  .sort_index()
            )

            if len(year_series) > 0:
                plt.figure(figsize=(10, 6))
                plt.plot(year_series.index, year_series.values)
                plt.title("Average DataValue by Year")
                plt.xlabel("Year")
                plt.ylabel("Average DataValue")
                plt.tight_layout()
                plt.savefig(os.path.join(PLOTS_DIR, "datavalue_by_year.png"), dpi=200)
                plt.close()

        # Plot: Top locations by avg DataValue (if LocationDesc exists)
        if "LocationDesc" in df.columns:
            top_loc = (
                df.dropna(subset=["LocationDesc", "DataValue"])
                  .groupby("LocationDesc")["DataValue"]
                  .mean()
                  .sort_values(ascending=False)
                  .head(15)
            )

            if len(top_loc) > 0:
                plt.figure(figsize=(10, 6))
                top_loc.sort_values().plot(kind="barh")
                plt.title("Top 15 Locations by Average DataValue")
                plt.xlabel("Average DataValue")
                plt.tight_layout()
                plt.savefig(os.path.join(PLOTS_DIR, "top_locations_by_avg_datavalue.png"), dpi=200)
                plt.close()

    else:
        print("\nDataValue exists but has no usable numeric values after conversion.")
else:
    print("\nColumn 'DataValue' not found, skipping outlier detection and DataValue plots.")

print("\nEDA completed.")
print(f"Tables saved to: {OUTPUT_DIR}/")
print(f"Plots saved to: {PLOTS_DIR}/")

