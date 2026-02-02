import pandas as pd
import numpy as np

# File Path
input_file_path = 'data/raw/sales1.csv'
output_file_path = 'data/processed/cleaned_sales_data.csv'

# 1. Load Data
df = pd.read_csv(input_file_path)

# 2. Understand Data Structure
print("--- Data Structure ---")
print(df.info())
print(f"\nShape of dataset: {df.shape}")

# Convert Sale_Date to datetime
df['Sale_Date'] = pd.to_datetime(df['Sale_Date'], dayfirst=True)

# 3. Summary Statistics
print("\n--- Numerical Summary ---")
print(df[['Sales_Amount', 'Discount']].describe())

print("\n--- Categorical Summary ---")
for col in ['Product_Category', 'City', 'Sales_Rep', 'Sales_Channel']:
    print(f"\nTop values for {col}:")
    print(df[col].value_counts().head(5))

# 4. Detect Anomalies (Using IQR for Sales_Amount)
Q1 = df['Sales_Amount'].quantile(0.25)
Q3 = df['Sales_Amount'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

anomalies = df[(df['Sales_Amount'] < lower_bound) | (df['Sales_Amount'] > upper_bound)]

print("\n--- Anomaly Detection ---")
print(f"Lower Bound: {lower_bound:.2f}")
print(f"Upper Bound: {upper_bound:.2f}")
print(f"Number of Outliers Detected: {len(anomalies)}")

if not anomalies.empty:
    print("\nSample Outlier Records:")
    print(anomalies.head())
else:
    print("No statistical outliers found in Sales_Amount.")

# 5. Export Clean Data for Tableau
# We create a CSV for the Tableau dashboard
df.to_csv(output_file_path, index=False)
print("\nSuccess: 'cleaned_sales_data.csv' exported for Tableau.")