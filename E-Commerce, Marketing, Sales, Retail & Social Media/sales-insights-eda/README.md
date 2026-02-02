# Sales Retail Insights: EDA & Anomaly Detection

## Project Overview
This project performs a deep-dive Exploratory Data Analysis (EDA) on a retail sales dataset. The primary objective is to understand the underlying data structure, derive summary statistics for business reporting, and identify statistical anomalies that may indicate data entry errors or exceptional sales events.

## Dataset
The dataset `sales1.csv` contains 1,000 transaction records with the following attributes:
- **Transaction Details**: Product ID, Sale Date, Sales Representative.
- **Geographic Information**: City.
- **Financial Metrics**: Sales Amount, Discount Applied, Payment Method.
- **Categorical Tags**: Product Category, Customer Type, Sales Channel.

## Tech Stack
- **Language**: Python 3.10
- **Libraries**: Pandas, NumPy
- **Visualization**: Tableau (for final dashboarding)

## Methodology
1. **Data Structural Audit**: Validating schema and data types.
2. **Summary Statistics**: Calculating mean, median, variance, and categorical counts.
3. **Outlier Detection**: Using the IQR method to flag transactions that deviate significantly from the norm.

## Key Findings
- The average transaction value is approximately $5,170.
- 'Electronics' is the most frequent product category.
- No missing values were detected, ensuring a high-quality dataset for analysis.

## Project Folder Structure
```txt
sales-insights-eda/
|
├── data/
|   └── processed/
|       └── cleaned_sales_data.csv
│   └── raw
|       └── sales1.csv
│
├── scripts/
│   └── data_processing.py
|
├── tableau/
│   └── sales_dashboard.txb
│
├── README.md
└── requirements.txt
```

## How to run
```bash
pip install -r requirements.txt
python scripts/data_processing.py
```

## Author

Morgan J. Tonner

## Discliamer

The data in this project was randomly generated on [Mockaroo](https://mockaroo.com/) and is intended solely for practice, learning, testing or portfolio use own. It does not reflect real-world sales, customers, or businesses, and should not be considered reliable for any real-time analysis or decision-making.
