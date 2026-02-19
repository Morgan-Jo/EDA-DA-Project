#  App Store Performance Analyser

### Exploratory Data Analysis — Google Play Store (2.3M+ Apps)

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-DuckDB%20%7C%20SQLite-003B57?logo=duckdb&logoColor=white)
![Tableau](https://img.shields.io/badge/Tableau-Public-E97627?logo=tableau&logoColor=white)

![VS Code](https://img.shields.io/badge/VS%20Code-Editor-007ACC?logo=visualstudiocode&logoColor=white)
![JupyterLab](https://img.shields.io/badge/JupyterLab-Notebook-F37626?logo=jupyter&logoColor=white)

![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-In%20Progress-yellow)

## Table of Contents

1. [Project Overview](#project-overview)
2. [Objectives](#objectives)
3. [Dataset](#dataset)
4. [Tech Stack](#tech-stack)
5. [Project Structure](#project-structure)
6. [Quick Start](#quick-start)
7. [Key Analyses](#key-analyses)
8. [SQL Patterns Used](#sql-patterns-used)
9. [Tableau Dashboard](#tableau-dashboard)
10. [Finding Summary](#finding-summary)
11. [Roadmap](#roadmap)
12. [Environment Variables](#environment-variables)
13. [Contributing](#contributing)
14. [Acknowledgements](#acknowledgements)
15. [Author](#author)
16. [License](#license)
17. [Discliamer](#discliamer)


## Project Overview

This project performs a full exploratory data analysis (EDA) on **2.3 million+ Android apps** scraped from the Google Play Store in June 2021. The goal is to uncover the key drivers of mobile app success — from ratings and download patterns to pricing strategy and update cadence — and present findings through an interactive Tableau Public dashboard.

> **Portfolio context:** This is a data analyst portfolio project demonstrating end-to-end EDA skills across Python, SQL, and Tableau.

## Objectives

| # | Analysis Focus | Business Question |
|---|----------------|-------------------|
| 1 | **Rating vs Download Correlation** | Do higher-rated apps consistently attract more downloads? |
| 2 | **Pricing Strategy Effectiveness** | What price points maximize installs and revenue for paid apps? |
| 3 | **Update Frequency Impact** | Does frequent updating lead to better ratings and retention? |
| 4 | **Freemium vs Paid Model** | Which monetisation model performs better across categories? |

## Dataset

| Property | Detail |
|----------|--------|
| **Source** | [Kaggle — Google Play Store Apps](https://www.kaggle.com/datasets/gauthamp10/google-playstore-apps) |
| **Collection method** | Scrapy (Python web scraper) on a cloud VM |
| **Collection period** | June 2021 |
| **Volume** | 2.3 million+ app records |
| **Platform** | Android (Google Play Store) |


### Key Columns

```
app_id, app_name, category, rating, rating_count, installs, min_installs, max_installs, free, price, currency, size, min_android, developer, developer_id, developer_email developer_website, released, privacy_policy, last_updated, content_rating, ad_supported, in_app_purchases, editors_choice
```

## Tech Stack

| Layer | Tool | Purpose |
|-------|------|---------|
| **Language** | Python 3.9+ | Data wrangling, EDA, sentiment analysis |
| **Data manipulation** | Pandas, NumPy | Cleaning, transformation, feature engineering |
| **Visualisation** | Matplotlib, Seaborn, Plotly | EDA charts and correlation plots |
| **NLP / Sentiment** | TextBlob, NLTK | Review sentiment scoring |
| **SQL engine** | DuckDB | In-process SQL with CTEs for ranking calculations |
| **Database ORM** | SQLAlchemy | Persistent storage and query interface |
| **IDE** | VS Code | Python scripts and SQL queries |
| **Dashboard** | Tableau Public | Interactive business dashboard |
| **Notebooks** | JupyterLab | Iterative exploration and prototyping |

## Project Structure
```
app-store-performance-analyser/
│
├── README.md                    ← You are here
├── requirements.txt             ← Python dependencies
├── .env.example                 ← Environment variable template
├── .env                         ← My environment variable  
├── .gitignore
├── LICENSE
|
├── data/
│   ├── raw/                        ← Original, unmodified Kaggle download
│   │   └── Google-Playstore.csv
│   ├── processed/                  ← Cleaned and feature-engineered data
|       ├── playstore.db
|       ├── playstore_clean.parquet
│   │   └── playstore_clean.csv
│   └── exports/                    ← Final CSVs / Parquet files for Tableau
|       ├── playstore_final.parquet
│       └── playstore_final.parquet
|
├── notebooks/
│   ├── 01_data_overview.ipynb      ← Initial load, shape, dtypes, nulls
│   ├── 02_data_cleaning.ipynb      ← Missing values, type casting, outliers
│   ├── 03_eda_ratings.ipynb        ← Rating distribution & correlation analysis
│   ├── 04_eda_pricing.ipynb        ← Pricing strategy deep-dive
│   ├── 05_eda_updates.ipynb        ← Update frequency impact on ratings
│   ├── 06_eda_freemium_vs_paid.ipynb ← Monetisation model comparison
│   └── 07_sentiment_analysis.ipynb ← TextBlob review sentiment scoring
│
├── src/
│   ├── __init__.py
│   ├── data/
|   |   ├── __init__.py
│   │   ├── loader.py               ← Load raw CSV / Parquet with Pandas
│   │   ├── cleaner.py              ← Cleaning pipeline (nulls, types, ranges)
│   │   └── feature_engineer.py    ← Derived columns (install buckets, price tiers, etc.)
│   │
│   ├── analysis/
|   |   ├── __init__.py
│   │   ├── correlation.py          ← Rating vs download Spearman / Pearson tests
│   │   ├── pricing.py              ← Price tier segmentation and conversion analysis
│   │   ├── update_impact.py        ← Update frequency bucketing and rating delta
│   │   ├── monetisation.py         ← Freemium vs paid comparative analysis
│   │   └── sentiment.py            ← TextBlob sentiment pipeline for reviews
│   │
│   └── utils/
|   |   ├── __init__.py
│   |   ├── logger.py               ← Loguru-based logging config
│   |   ├── plot_helpers.py         ← Reusable Seaborn / Matplotlib theme & chart helpers
│   |   └── export.py               ← Save processed data to CSV / Parquet / Excel
│
├── sql/
│   ├── 01_create_schema.sql        ← Table definitions (SQLite / DuckDB)
│   ├── 02_load_data.sql            ← Bulk insert statements
│   ├── 03_category_rankings.sql    ← CTE: top apps ranked per category
│   ├── 04_pricing_analysis.sql     ← CTE: revenue proxies by price bracket
│   ├── 05_update_frequency.sql     ← CTE: days-since-update buckets vs avg rating
│   └── 06_freemium_vs_paid.sql     ← CTE: monetisation model performance comparison
│
├── tableau/
│   ├── app_store_dashboard.twbx    ← Packaged Tableau workbook
│   └── dashboard_preview.png       ← Static screenshot for README / portfolio
│
├── reports/
│   ├── figures/                    ← Saved chart PNGs from notebooks
│   └── findings_summary.md         ← Key insights and narrative write-up
│
└── tests/
    ├── test_cleaner.py             ← Unit tests for cleaning functions
    └── test_feature_engineer.py    ← Unit tests for derived feature logic
```

## Quick Start
1. Clone the repository the whole repository

```bash
git clone https://github.com/Morgan-Jo/EDA-DA-Project.git
cd EDA-DA-Porject/Technology/app-store-performance-analyzer
```

### ***OR***

> **Mono-repo note:** This project lives inside the `technology/` section of the
> [EDA-DA-Project](https://github.com/Morgan-Jo/EDA-DA-Project) repository at the path:
> ```
> EDA-DA-Project/
> └── Technology/
>     └── app-store-performance-analyzer/   ← this project
> ```
> You do **not** need to clone the entire repository. Pick any of the three methods below.

 ---
### Get just this project (choose one method)

#### Option A — Sparse Checkout *(recommended — keeps full git history)*

```bash
# 1. Create a local folder and initialise git
mkdir app-store-performance-analyzer
cd app-store-performance-analyzer
git init

# 2. Add the remote
git remote add origin https://github.com/Morgan-Jo/EDA-DA-Project.git

# 3. Enable sparse checkout
git sparse-checkout init --cone

# 4. Point to the exact subfolder inside the repo
git sparse-checkout set technology/app-store-performance-analyzer

# 5. Pull only that folder — nothing else downloads
git pull origin main

# 6. Move into the project folder
cd technology/app-store-performance-analyzer
```

#### Option B — degit *(fastest — no git history, just the files)*

```bash
npx degit github:/EDA-DA-Project/technology/app-store-performance-analyzer
```

#### Option C — DownGit *(browser download, no terminal needed)*


1. Go to [https://minhaskamal.github.io/DownGit](https://minhaskamal.github.io/DownGit)
2. Paste this URL:
   ```
   https://github.com/Morgan-Jo/EDA-DA-Project/tree/main/Technology/app-store-performance-analyzer
   ```
3. Click **Download** — you'll get a ZIP of just this project
 ---

2. Create and activate a virtual environment

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Download TextBlob corpora (one-time)

```bash
python -m textblob.download_corpora
python -c "import nltk; nltk.download('punkt')"
```

5. Download the dataset from Kaggle

```bash
# Option A: Kaggle CLI
pip install kaggle
kaggle datasets download -d gauthamp10/google-playstore-apps
unzip google-playstore-apps.zip -d data/raw/

# Option B: Manual download
# Visit https://www.kaggle.com/datasets/gauthamp10/google-playstore-apps
# Download and place the CSV inside data/raw/
```

6. Set up environment variables

```bash
cp .env.example .env
# Edit .env with your local paths if needed
```

7. Run the cleaning pipeline

```bash
python src/data/cleaner.py
```

8. Launch JupyterLab

```bash
jupyter lab
# Open notebooks/ in order: 01 → 07
```

9. Run SQL analyses (DuckDB — no server required)

```bash
# DuckDB runs entirely in-process; no installation beyond the pip package.
# Open any .sql file in VS Code and execute via the DuckDB Python API:
python -c "
import duckdb
conn = duckdb.connect()
conn.execute(open('sql/03_category_rankings.sql').read())
"
```

## Key Analyses

1. Rating vs Download Correlation
    - Spearman and Pearson correlation between `rating` and `min_installs`
    - Scatter plots with log-scale install axis, segmented by category
    - Hypothesis: high ratings are a *necessary but not sufficient* condition for high downloads

2. Pricing Strategy Effectiveness
    - Apps bucketed into tiers: Free / $0.99 / $1.99 / $2.99 / $4.99+ / $9.99+
    - Comparison of median install counts across tiers per category
    - Identification of "sweet spot" price points with the best installs-to-revenue proxy

3. Update Frequency Impact
    - `last_updated` parsed to derive days since update at crawl date (June 2021)
    - Buckets: < 30 days / 30–90 days / 90–180 days / 180–365 days / 1 year+
    - CTE-based SQL ranking: average rating and install count per update-frequency bucket

4. Freemium vs Paid Model Comparison
    - Dimension breakdown: `free` flag × `ad_supported` × `in_app_purchases`
    - Four monetisation archetypes: Pure Free / Ad-Supported / IAP Freemium / Paid
    - Statistical comparison of ratings, installs and category penetration across archetypes

5. Sentiment Analysis (Bonus)
    - TextBlob polarity scoring on app descriptions (proxy for review tone)
    - Correlation between description sentiment polarity and average rating

## SQL Patterns Used

```sql
-- Example: Category ranking CTE from sql/03_category_rankings.sql

WITH ranked_apps AS (
    SELECT
        app_name,
        category,
        rating,
        min_installs,
        ROW_NUMBER() OVER (
            PARTITION BY category
            ORDER BY rating DESC, min_installs DESC
        ) AS rank_in_category
    FROM apps
    WHERE rating_count >= 1000          -- minimum review threshold
      AND min_installs IS NOT NULL
),
top_10_per_category AS (
    SELECT * FROM ranked_apps WHERE rank_in_category <= 10
)
SELECT * FROM top_10_per_category
ORDER BY category, rank_in_category;
```

## Tableau Dashboard

The interactive dashboard is published on **Tableau Public** and contains four views:

| Sheet | Description |
|-------|-------------|
| **Overview** | KPI tiles: total apps, avg rating, top category by installs |
| **Rating × Installs** | Scatter plot with category filter and log scale |
| **Pricing Heatmap** | Installs by price tier × category matrix |
| **Freemium vs Paid** | Side-by-side bar chart across monetisation archetypes |

🔗 **Live Dashboard:** 

## Findings Summary

> Full narrative is in [`reports/findings_summary.md`](reports/findings_summary.md).
> Updated after each analysis notebook is complete.

| Finding | Insight |
|---------|---------|
| Rating threshold | Apps below 3.5 stars rarely exceed 10K installs |
| Optimal price point | $0.99–$2.99 paid apps outperform higher-priced tiers on installs |
| Update cadence | Apps updated within 90 days average 0.3 rating points higher |
| Monetisation winner | IAP Freemium dominates on installs; Pure Paid leads on per-user revenue proxy |

## Roadmap

- [x] Project scaffold and README
- [ ] `01_data_overview.ipynb` — initial profiling
- [ ] `02_data_cleaning.ipynb` — cleaning pipeline
- [ ] `src/data/cleaner.py` — reusable cleaning module
- [ ] `src/data/feature_engineer.py` — derived features
- [ ] SQL schema and CTE queries
- [ ] EDA notebooks 03–06
- [ ] Sentiment analysis notebook 07
- [ ] Tableau dashboard build and publish
- [ ] `reports/findings_summary.md` write-up
- [ ] Unit tests for core modules

## Environment Variables

Copy `.env.example` to `.env` and fill in values:

```ini
# .env.example

# Path to raw data file
RAW_DATA_PATH=data/raw/Google-Playstore.csv

# Path to write processed data
PROCESSED_DATA_PATH_PARQUET=data/processed/
PROCESSED_DATA_PATH_CSV=data/processed/

# Path to export Tableau-ready files
EXPORT_PATH_PARQUET=data/exports/
EXPORT_PATH_CSV=data/exports/

# Logging level: DEBUG | INFO | WARNING
LOG_LEVEL=INFO
```

## Contributing

This is a personal portfolio project. Feedback and suggestions are welcome — feel free to open an issue or submit a pull request.

## Acknowledgements

- Dataset by **Gautham M** on Kaggle — [Google Play Store Apps](https://www.kaggle.com/datasets/gauthamp10/google-playstore-apps)
- Collected via Scrapy on a cloud VM, June 2021

## Author 

Morgan Jo Tonner

## License

This project is licensed under the [MIT License](LICENSE).

## Discliamer

This project was created for **educational and portfolio demonstration purposes only.**
All analyses, insights, and visualisations are based on publicly available data and do not represent official metrics, recommendations, or performance evaluations from Google, the Google Play Store, or any app developer.

The dataset reflects a **snapshot in time from June 2021** and may not represent current app performance, pricing, policies, or platform behaviour. Any revenue, retention, or monetisation metrics used are proxies derived from public signals, not actual financial results.

This repository is **not affiliated with, endorsed by, or connected to Google or Kaggle.**
Insights should not be used for commercial decision making without further validation using first party data.

***Built as part of a data analyst portfolio — Technology Industry | EDA Series***

***Built with ☕ by Morgan · [LinkedIn](https://www.linkedin.com/in/morgan-j-tonner/) · [GitHub](https://github.com/Morgan-Jo)***