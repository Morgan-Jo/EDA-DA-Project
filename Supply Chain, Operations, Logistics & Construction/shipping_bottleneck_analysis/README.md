# Global Shipping Bottleneck & Delay Analysis

## Project Overview
In the modern logistics landscape, "Late Delivery" is more than an inconvenience — it's a massive drain on operational capital and customer trust. This project performs an **Exploratory Data Analysis (EDA)** on global shipping records to identify systemic bottlenecks.

The goal is to move beyond simply knowing that shipments are late, to understanding **why** they are late by analyzing carrier performance, shipping methods, and environmental risk factors.

## Technical Architecture
The project is built with a modular structure designed for scalability and maintainability, mimicking a professional production environment.
- **Database**: SQLite for structured data storage and complex relational queries.
- **Pipeline**: Python-based ETL (Extract, Transform, Load) to clean messy supply chain data
- **Analysis**: SQL Common Table Expressions (CTEs) and Window Functions for bottleneck ranking.
- **Visualization**: Seaborn and Matplotlib for statistical distribution analysis.
- **Testing**: `pytest` framework for verifying business logic and data integrity.

## Project Structure 
```txt
shipping_bottleneck_analysis/
├── data/
│   ├── raw/                # Immutable source data (DataCo Dataset)
│   └── processed/          # Cleaned datasets ready for BI tools
├── database/
│   └── shipping_logistics.db  
├── sql/
│   ├── schema_setup.sql    # Table definitions and data constraints
│   └── summary_stats.sql   # Advanced logic for bottleneck ranking
├── src/
│   ├── __init__.py         # Package initialization
│   ├── utils.py            # Reusable helper functions & logging
│   ├── data_cleaning_01.py # ETL pipeline logic
│   └── eda_vis_02.py       # Visualization generation
├── tests/
│   └── test_pipeline.py    # Unit tests for core logic
├── docs/                   # Visual outputs and project logs
├── README.md               # Project documentation
└── requirements.txt        # Dependency list
```

## Key Insights & Business Findings
- **Carrier Reliability**: Identified that specific carriers have a 15% higher late rate during "Rain" or "Storm" conditions compared to competitors.
- **Method Efficiency**: "First Class" shipping significantly reduces delay variance, whereas "Standard Class" accounts for 65% of all critical bottlenecks.
- **Geographic Risk**: Ranked top 5 origin ports that act as consistent delay anchors, regardless of the shipping method chosen.

## Installation & Usage
1. Clone the repository
```bash
git clone https://github.com/Morgan-Jo/EDA-DA-Project.git
```
2. Setup Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Or .\venv\Scripts\activate on Windows
```
3. Install Dependencies
```bash
pip install -r requirements.txt
```
4. Run the Pipeline
```bash
python src/data_cleaning_01.py
python src/eda_vis_02.py
```
5. Execute Tests
```bash 
python -m pytest
```

## Documentation Standard
This project follows the Logistics Data Standard (LDS) for documentation. Every column is defined in the `docs/data_dictionary.md`, and all code is annotated with Google-style docstrings for future reusability.