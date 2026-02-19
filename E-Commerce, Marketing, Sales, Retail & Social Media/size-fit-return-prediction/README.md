# Size & Fit Return Prediction — Retail Apparel EDA

![Microsoft Excel](https://img.shields.io/badge/Excel-Data%20Analysis-217346?logo=microsoft-excel&logoColor=white)
![VS Code](https://img.shields.io/badge/VS%20Code-Editor-007ACC?logo=visualstudiocode&logoColor=white)

![Git](https://img.shields.io/badge/Git-Version%20Control-F05032?logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github&logoColor=white)

![License](https://img.shields.io/badge/License-MIT-green?style=flat)
![Status](https://img.shields.io/badge/Status-In%20Progress-yellow)

> **An Excel-based Exploratory Data Analysis project using Root Cause Analysis to understand why customers return clothing due to sizing and fit issues.**


## Table of Contents

- [Project Overview](#project-overview)
- [Who This Is For](#who-this-is-for)
- [Dataset](#dataset)
- [Project Structure](#project-structure)
- [How to Use This Project](#how-to-use-this-project)
- [Key Questions Answered](#key-questions-answered)
- [Excel Workbook Guide](#excel-workbook-guide)
- [Technical Details](#technical-details)
- [Key Findings Summary](#key-findings-summary)
- [Limitations](#limitations)
- [Changelog](#changelog)
- [Author](#author)
- [License](#license)
- [Discliamer](#discliamer)


## Project Overview

Returns are one of the costliest problems in retail apparel. This project investigates **why customers return items due to poor size or fit**, using real-world e-commerce data from two platforms: **ModCloth** and **Rent the Runway**.

Using **Microsoft Excel** as the sole analytical tool, this project:
- Cleans and merges unstructured customer review text using **Power Query**
- Identifies size ratios that drive high return rates using **Pivot Tables**
- Visualises customer measurement distributions vs. brand size charts using **Histograms**
- Applies a **Root Cause Analysis (RCA) framework** to pinpoint the "why" behind fit returns

**Framework:** Root Cause Analysis (5-Whys + Fishbone methodology adapted for data)  
**Tool:** Microsoft Excel (Power Query, Pivot Tables, Charts, Data Validation)  
**Industry:** Retail Apparel / E-Commerce


## Who This Is For

### Non-Technical Readers
You don't need to know how to code. This project was built entirely in Excel — a tool most people already know. Think of it like a very thorough investigation into why clothes don't fit. We looked at thousands of customer reviews and measurements to find patterns, then traced those patterns back to their root causes. The final outputs are charts, tables, and a plain-English report you can read in the `05_reports/` folder.

### Technical Readers
This is an EDA project built entirely in Excel using:
- **Power Query (M language)** for ETL from raw JSON → structured tables
- **Pivot Tables & Slicers** for dynamic cross-tabulation of size ratios vs. return rates
- **Statistical histograms** for measurement distribution analysis
- **Conditional formatting & DAX-style calculated columns** for flagging outliers
- All steps are reproducible and documented in the Data Dictionary and Change Log


## Dataset

| Property | Details |
|---|---|
| **Source** | [Kaggle – Clothing Fir Dataset for Size Recommendation](https://www.kaggle.com/datasets/rmisra/clothing-fit-dataset-for-size-recommendation) |
| **Files** | `modcloth_final_data.json`, `renttherunway_final_data.json` |
| **Platforms** | ModCloth (women's fashion retail), Rent the Runway (dress rental) |
| **Key Fields** | Customer height, weight, age, size ordered, fit feedback, review text, return reason |
| **Volume** | ~192,000+ records combined (varies by version) |
| **License** | Public / Research use — check Kaggle listing for terms |


## Project Structure

```
size-fit-return-prediction/
│
├── data/
│   ├── raw/                        ← Place downloaded JSON files here (not tracked by Git)
│   ├── processed/                  ← Cleaned outputs exported from Power Query
│   └── reference/                  ← Size charts, measurement standards, lookup tables
│
├── excel/
│   ├── workbooks/                  ← Main Excel analysis files (.xlsx)
│   └── templates/                  ← Blank reusable templates (pivot, histogram, RCA)
│
├── docs/
│   ├── project_plan.md             ← Full project plan (this links to PROJECT_PLAN.md)
│   ├── data_dictionary.md          ← Field definitions, transformations, data types
│   └── change_log/                 ← Version history of all workbook and doc changes
│
|
├── 04_visuals/                     ← Exported charts and screenshots (PNG/PDF)
|
├── reports/                        ← Final written findings (plain-English + technical)
│
├── README.md                       ← You are here
├── LICENSE
└── .gitignore
```


## How to Use This Project

### Step 1 — Download the Data
1. Go to [Kaggle](https://www.kaggle.com/datasets/) and search for "**Clothing Fit Dataset for Size Recommendation**""
2. Download both JSON files:
   - `modcloth_final_data.json`
   - `renttherunway_final_data.json`
3. Place both files into the `data/raw/` folder

### Step 2 — Open the Main Workbook
1. Open `excel/workbooks/SizeFit_RCA_Analysis.xlsx`
2. Go to **Data → Queries & Connections** to see the Power Query steps
3. Update the file path to your local `data/raw/` folder in the Power Query source step
4. Click **Refresh All**

### Step 3 — Explore the Analysis Sheets
Each sheet in the workbook has a purpose (see [Excel Workbook Guide](#excel-workbook-guide) below)

### Step 4 — Read the Report
Open `reports/Final_Findings_Report.pdf` for a plain-English summary of all insights

---

## Key Questions Answered

1. Which size ratios (ordered size vs. recommended size) are most associated with returns?
2. Do customers who mention "fit," "small," or "large" in reviews return more often?
3. How do customer height/weight distributions compare to brand size chart assumptions?
4. Which product categories have the worst fit consistency?
5. What are the root causes of size-related returns (brand sizing? inaccurate charts? customer error?)?

---

## Excel Workbook Guide

| Sheet Name | What It Does | Skill Level Needed |
|---|---|---|
| `START_HERE` | Navigation guide with hyperlinks to all sheets | Beginner |
| `PQ_ModCloth` | Power Query output – cleaned ModCloth data | Intermediate |
| `PQ_RunwayMerge` | Merged dataset from both sources | Intermediate |
| `RCA_FitKeywords` | Keyword extraction from review text (fit, small, large, tight) | Intermediate |
| `PIVOT_SizeRatios` | Pivot table: size ordered vs. return rate by category | Beginner |
| `PIVOT_Demographics` | Pivot table: height/weight segments vs. fit satisfaction | Beginner |
| `HIST_Measurements` | Histograms comparing customer measurements to size chart ranges | Beginner |
| `CHART_ReturnReasons` | Bar/Pareto chart of return reason frequency | Beginner |
| `RCA_Fishbone` | Root Cause Analysis summary (manually built, data-linked) | Beginner |
| `LOOKUP_SizeCharts` | Reference size chart data used in comparisons | Reference |
| `DOCS` | In-workbook documentation and data dictionary snapshot | Reference |

---

## Technical Details

<details>
<summary>Click to expand — Power Query transformation steps</summary>

### ModCloth Power Query Steps
1. Source: JSON file load from `data/raw/modcloth_final_data.json`
2. Expand nested records (if applicable)
3. Rename columns to standard naming convention (snake_case)
4. Filter rows: remove records where `size` and `height` are both null
5. Add column: `fit_flag` = if review text contains "fit", "small", "large", "tight", "big" then 1 else 0
6. Add column: `size_ratio` = `size_ordered` / `usual_size` (where available)
7. Change data types: height → number, weight → number, size → text
8. Load to sheet: `PQ_ModCloth`

### Rent the Runway Power Query Steps
1. Source: JSON file load from `data/raw/renttherunway_final_data.json`
2. Expand nested records
3. Rename columns to match ModCloth schema
4. Parse height: convert "5ft 4in" format → decimal inches
5. Add column: `fit_flag` (same logic as above)
6. Add column: `platform` = "RentTheRunway"
7. Append to ModCloth query → load to `PQ_RunwayMerge`

### Size Ratio Logic
- `size_ratio < 0.9` → Ordered too small → likely "fits large" complaint
- `size_ratio > 1.1` → Ordered too big → likely "fits small" complaint  
- `size_ratio = 1.0` → True to size order

</details>

<details>
<summary>Click to expand — Pivot Table Configuration</summary>

### PIVOT_SizeRatios
- **Rows:** `size_ratio_bucket` (binned: <0.9, 0.9–1.0, 1.0–1.1, >1.1)
- **Columns:** `category` (dress, top, bottom, etc.)
- **Values:** Count of `return_flag`, % of total (show values as)
- **Slicer:** `platform`, `fit_flag`

### PIVOT_Demographics  
- **Rows:** `height_bucket` (binned in 2-inch intervals)
- **Columns:** `weight_bucket` (binned in 10 lb intervals)
- **Values:** Average `fit_feedback_score` (1=small, 3=fit, 5=large)
- **Slicer:** `category`, `size_ordered`

</details>

---

## Key Findings Summary

> Full findings in `reports/Final_Findings_Report.pdf`

- **[To be updated upon analysis completion]**
- Placeholder: Customers outside standard measurement ranges (height <5'2" or >5'9", weight >180 lbs) showed disproportionately high fit-complaint rates
- Placeholder: Rental platform reviews showed 2x more "too small" complaints vs. retail platform
- Placeholder: Dresses and jumpsuits had the highest size-related return rates by category

---

## Limitations

- Return data is inferred from review text keywords, not confirmed transactional return records
- Height/weight data is self-reported and may contain inaccuracies
- Size chart comparisons are approximated — exact brand size charts were not available in the dataset
- This analysis is descriptive/exploratory — no predictive model is built

---

## Changelog

See [CHANGELOG.md](docs/CHANGELOG.md) for the full version history.

| Version | Date | Summary |
|---|---|---|
| v1.0 | 2026-02-18 | Initial project setup, folder structure, documentation |

## Author 

Morgan Jo Tonner

## License

This project is licensed under the [MIT License](LICENSE).

## Discliamer

This project is an independent educational and portfolio analysis created for demonstration purposes only. It is not affiliated with, endorsed by, or connected to Kaggle, ModCloth, Rent the Runway, or any associated brands.

The dataset used is publicly available via Kaggle and is subject to its original licensing terms. All analysis has been conducted for research and learning purposes only.

Findings presented in this repository are exploratory in nature and should not be interpreted as commercial advice, operational recommendations, or definitive conclusions about any brand, retailer, or customer segment.

All customer data included in the dataset is anonymised and publicly distributed for research use.

*Last updated: 2026-02-18 | Version: 1.0*

***Built as part of a data analyst portfolio — Retail Apparel Industry | EDA Series***

***Built with ☕ by Morgan · [LinkedIn](https://www.linkedin.com/in/morgan-j-tonner/) · [GitHub](https://github.com/Morgan-Jo)***