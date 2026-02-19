# U.S. Chronic Disease Indicators – Exploratory Data Analysis

## Project Overview
This project explores the U.S. Chronic Disease Indicators dataset using Python. The goal is to demonstrate core data analysis skills including understanding data structure, generating summary statistics, and detecting anomalies in real-world public health data.

The analysis is designed to reflect how a data analyst would approach a new dataset in a professional setting.

## Objectives
- Inspect and understand dataset structure  
- Generate meaningful summary statistics  
- Identify missing values, outliers, and anomalies  
- Produce reusable, clean Python analysis code  

## Tools Used
- Python  
- pandas  
- numpy  
- matplotlib  
- seaborn  
- scipy  

## Project Structure
```txt
us-chronic-disease-eda/
│
├── data/
│   └── U.S._Chronic_Disease_Indicators.csv
│
├── outputs/
│   ├── summary_statistics.csv
│   ├── missing_values.csv
|   ├──    anomalies_detected.csv
│   └── plots/
│       ├── missing_values_top20.png
│       ├── datavalue_distribution.png
│       └── top_locations_by_avg_datavalue.png
│
├── src/
│   └── eda_chronic_disease.py
│
├── README.md
└── requirements.txt
```


## How to Run
1. Clone the repository  
2. Install dependencies:
```r
pip install -r requirements.txt
```
3. Run the script:
```r
python src/eda_chronic_disease.py
```


## Outputs
The script generates:
- Summary statistics table  
- Missing value report  
- Detected anomalies report  

All outputs are saved in the `/outputs` folder.

## Dataset Source
U.S. Chronic Disease Indicators - can be found [here](https://catalog.data.gov/dataset/u-s-chronic-disease-indicators).

## Author
Morgan J. Tonner

## Disclaimer
The data in this project was download US Gov catalog and is intended solely for practice, learning, testing or portfolio use own.