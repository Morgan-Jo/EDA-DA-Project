# Coffee Vending Machine Sales: Exploratory Data Analysis with SQL & Tableau

## Overview
This project explores transactional coffee sales data from a vending machine using a structured Exploratory Data Analysis (EDA) approach. Each dataset is analysed independently using SQL to produce descriptive statistics and clean analytical outputs, which are then visualised in Tableau.

The focus of the project is on understanding sales behaviour, time-based trends, and customer purchasing patterns before progressing to dashboarding and potential forecasting.

## About the Dataset

### Overview
This dataset contains detailed transaction-level records of coffee sales from a vending machine. It was created and maintained by an independent dataset author with the aim of providing an open, real-world dataset to the analytics community.

The data captures individual coffee purchases and is suitable for analysing purchasing patterns, sales trends, and customer preferences related to coffee products.

### Data Collection Period
The dataset spans from **March 2024 to the present**, capturing **daily transaction data**. The dataset is actively updated, allowing for both historical analysis and ongoing time series exploration.

### Dataset 
The dataset was download from Kaggle - [Coffee Sales](https://www.kaggle.com/datasets/ihelon/coffee-sales/data)


### Intended Analytical Use Cases

This dataset is well suited for:

- **Time Series Exploratory Data Analysis**
  - Daily, weekly, and monthly sales trends
  - Seasonality and demand patterns
  - Peak and low sales periods

- **Sales Trend & Baseline Analysis**
  - Next-day, next-week, and next-month sales baselines
  - Rolling averages and growth rates

- **Customer & Product Analysis**
  - Frequency of repeat purchases
  - Product popularity and sales contribution
  - Customer-level purchase behaviour (where identifiers exist)

## Tools & Technologies
- SQL (data profiling, aggregation, descriptive statistics)
- VS Code (SQL development environment)
- Tableau Public (visualisation and dashboards)
- CSV files loaded into a local SQL database

## EDA Approach

### 1. Data Profiling & Understanding
- Inspect schema, data types, and row counts
- Identify primary keys and analytical dimensions
- Check for missing values and data quality issues

### 2. Descriptive Statistics (SQL-First)
For each dataset:
- Transaction counts and sales totals
- Summary statistics for numerical fields
- Frequency distributions for categorical variables
- Time-based aggregations (daily, weekly, monthly)

### 3. Visual Exploration (Tableau)
- Line charts for sales trends
- Bar charts for product performance
- Histograms or boxplots for value distributions
- KPI tiles for key sales metrics

### 4. Pre-Dashboard Validation
- Validate aggregation logic
- Check for outliers and anomalies
- Ensure Tableau-ready outputs

## Join Rationale

Each dataset is analysed independently before any combination to ensure data quality, consistent definitions, and a clear understanding of structure and limitations. This reduces the risk of introducing misleading results through premature joins.

The datasets share the same transactional grain but differ slightly in schema. One dataset includes identifiable customer information, while the other represents anonymous cash transactions. To address this, both datasets are first standardised into staging views with aligned data types, consistent field names, and derived time dimensions.

The datasets are then combined using a **UNION ALL** approach rather than relational joins. This preserves all transactions without row duplication or loss and maintains source-level lineage for validation and analysis. A final analytics view is created to expose business-ready fields for Tableau, minimising transformation logic in the dashboard layer.

This approach ensures transparency, reproducibility, and a clean separation between raw data, transformations, and analysis.


## Dashboard
The Tableau dashboard presents:
- Overall sales trends over time
- Product-level performance insights
- Customer purchase patterns
- Interactive filters for time and product selection

Tableau Public link: [Coffee Vending Machine Sales — Exploratory Data Analysis Dashboard](https://public.tableau.com/app/profile/morgan.tonner/viz/CoffeeVendingMachineSalesExploratoryDataAnalysisDashboard/CoffeeVendingMachineSalesExploratoryDataAnalysisDashboard)

## Key Insights
- Clear sales patterns emerge at daily and weekly levels
- Certain products consistently drive the majority of revenue
- Purchase behaviour varies noticeably by time period

## Next Steps
- Extend analysis to forecasting models
- Compare weekday vs weekend behaviour
- Incorporate pricing or promotion effects if available

## Project Structure
```txt
coffee-vending-eda/
│
├── data/
│   └── processed/
│   └── raw/
│       ├── index_1.csv
│       └── index_2.cvs
│
├── sql/
│   ├── eda_queries.sql
│   ├── joins.sql
│   ├── setup_tables.sql
│   ├── tableau_ready_queries.sql
│   └── tableau_validation_and_export.sql
│
├── tableau/
│   └── Coffee Vending Machine Sales — Exploratory Data Analysis Dashboard.twb
│
├── database/
|      └── coffee_sale.db
|
└── README.md

```

## How to run
1. Place the dataset in the `data/` folder
2. Load the CSV into SQLite
3. Run queries from the `sql/` folder in order
4. Connect Tableau to the cleaned table or query output
5. Build dashboard using summary tables

## Author
Morgan J. Tonner

## Disclaimer
The data in this project was found on the Kaggle webiste and can be found [here](https://www.kaggle.com/datasets/ihelon/coffee-sales) and is intended solely for practice, learning, testing or portfolio use own. It is not for decision-making.