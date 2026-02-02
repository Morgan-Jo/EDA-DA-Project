# Breast Cancer EDA (R + Shiny)

## Overview
This project demonstrates a complete Exploratory Data Analysis workflow using R, focused on:
- Understanding data structure
- Producing summary statistics
- Detecting anomalies and outliers
- Building an interactive Shiny dashboard

The project is designed to showcase practical data analysis skills and clear analytical thinking.

## Objectives
- Inspect and understand the dataset structure  
- Generate meaningful descriptive statistics  
- Visualise distributions and detect anomalies  
- Build an interactive dashboard for exploration  

## Tools used
- R  
- tidyverse  
- ggplot2  
- Shiny  
- skimr  

## Project Folder Structure
```txt
breast-cancer-eda/
│
├── data/
│   └── breast-cancer.csv
│
├── scripts/
│   └── eda_analysis.R
│
├── shiny/
│   └── app.R
│
├── outputs/
│   └── plots/
│
└── README.md
```

## Key analysis steps
- Data structure inspection (str, glimpse)  
- Missing value checks  
- Summary statistics  
- Feature distributions  
- IQR-based outlier detection  
- Interactive Shiny dashboard  

## Shiny dashboard features
- Variable selector  
- Summary statistics table  
- Interactive histogram  
- Boxplot for anomaly detection  

## How to run

1. Open project in RStudio  
2. Run EDA script:
```r
source("scripts/eda_analysis.R")
```
3. Run Shiny app:
```r
shiny::runApp("shiny")
```

## Author

Morgan J. Tonner

## Discliamer

The data in this project was found on the Kaggle webiste and can be found [here](https://www.kaggle.com/datasets/yasserh/breast-cancer-dataset) and is intended solely for practice, learning, testing or portfolio use own. It is not for decision-making.