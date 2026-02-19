# Global Dentistry Personnel Analysis (EDA with SQL + Looker Studio)

## Overview
This project explores a real-world healthcare workforce dataset focused on dentistry personnel across countries and regions. The aim is to demonstrate data exploration, summary statistics, and anomaly detection using SQL, with visualisation in Google Looker Studio.

## Dataset
- File: dentistry-personnel.csv  
- Source: WHO / NHWA-style global workforce dataset  
- Rows: 7,598  
- Columns: 34  
- Example metric: Dentists per 10,000 population  

## Tools Used
- SQL (queries written in VS Code)
- Google Looker Studio (dashboard visualisations)
- GitHub for documentation and portfolio

## Key Questions Explored
- Which regions have the highest average dentist density?
- Which countries rank highest and lowest?
- Are there extreme outliers in reported values?
- Do any countries show unusual spikes across years?

## Project Structure
```txt
dentistry-personnel-eda/
│
├── data/
│   ├── raw/
│   │   └── dentistry-personnel.csv
│   └── processed/
|
├── db/
│   └── dentistry.db
|
├── sql/
│   ├── 01_create_table.sql
│   ├── 02_exploration.sql
│   ├── 03_summary_stats.sql
│   ├── 04_anomaly_detection.sql
│   └── 05_clean_view.sql
│
├── dashboards/
│   ├── Dentistry_Report_Dashboard.pdf 
│   └── looker_dashboard_link.md
│
├── README.md
│
└── insights/
    └── key_findings.md
```

## Example Outputs
- Average dentists per 10,000 by region  
- Top 10 and bottom 10 countries  
- Outlier detection using standard deviation  
- Time series trends  

## Dashboard
[View the Looker Studio Dashboard](https://lookerstudio.google.com/reporting/efa98d5e-638d-47c1-8ee1-66b5819895ae) 

## Running locally

1. Create database inside /db  
2. Load dataset from /data/raw into the database  
3. Run SQL scripts from /sql in order:
   - `01_create_table.sql` 
   - `02_exploration.sql` 
   - `03_summary_stats.sql`  
   - `04_anomaly_detection.sql`
   - `05_clean_view.sql`  

## Author

Morgan J. Tonner

## Discliamer

The data in this project was collected and download from the World Health Organization **(WHO)** and is intended solely for practice, learning, testing or portfolio use own. The Dentistry Personnel data can be found [here](https://www.who.int/data/gho/data/themes/topics/health-workforce).