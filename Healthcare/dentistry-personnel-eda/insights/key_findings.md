# Global Dentistry Personnel Analysis

## Overview

This analysis examined global dentist availability using the metric dentists per 10,000 population. The objective was to identify structural patterns, regional disparities, time based trends, and extreme values that may indicate workforce concentration or access challenges. Insights are based on cleaned SQL outputs and visualised through a Google Looker Studio dashboard.

## 1. Dentist availability varies sharply across regions

Average dentist density differs substantially by region.
- **Europe** shows the highest average dentist availability, with an average of **4.28 dentists per 10,000 population** across reporting countries.
- The **Americas** and **Western Pacific** regions also perform relatively strongly, though with greater internal variability.
- **Africa** and **South East Asia** consistently report the lowest averages, indicating limited access to dental professionals at a regional level.

These differences appear structural rather than temporary, reflecting long term workforce distribution and healthcare investment patterns.

## 2. Country level distribution is highly skewed

At the country level, dentist density is extremely uneven.

### Highest dentist density

The top performing countries report dentist densities close to or above 10 dentists per 10,000 population:
- Greece leads globally with an average of **11.94**
- Niue, Cuba, Argentina, and Monaco also report values **above 10**
- High performing countries are concentrated mainly in **Europe**, the **Americas**, and the **Western Pacific**

### Lowest dentist density

At the opposite end:
- Somalia reports **0 dentists per 10,000**
- Several African countries cluster tightly between **0.01 and 0.03**
- The bottom ten countries are dominated by **Africa** and the **Eastern Mediterranean**

This long tail of extremely low values highlights significant access gaps and potential data completeness issues.

## 3. Global trends show gradual improvement, not rapid change

Trend analysis by region shows:
- A **slow upward trend** in dentist availability over time in most regions
- No evidence of rapid global convergence between high and low coverage regions
- Periods of stability and gradual change rather than sharp inflections

This suggests that dentist workforce growth is incremental and closely tied to long term education and health system capacity rather than short term policy shifts.

## 4. Outliers materially influence summary statistics

The distribution of dentist density includes several extreme values:
- The **maximum observed value is 18.42 dentists per 10,000**
- The **minimum is 0**, which may represent either true absence or reporting limitations
- The standard deviation of **3.42** and variance of **11.69** indicate wide dispersion around the mean

These outliers significantly affect global averages and reinforce the importance of reviewing both aggregated and country level views.

## 5. Data quality and reporting differences remain a key consideration

Several patterns suggest underlying data limitations:
- Zero or near zero values are unlikely to reflect complete absence of dentists in all cases
- Reporting coverage varies by country and year
- Aggregated regional metrics can mask severe country level shortages

These factors were considered when interpreting trends and ranking outputs.

## Summary

This analysis demonstrates that global dentist availability is **uneven, highly skewed, and slow to change over time**. While some regions and countries maintain strong workforce coverage, many countries remain at critically low levels. Long term structural investment appears to be the primary driver of improvement rather than short term change.

From an analytical perspective, the project highlights the importance of:
- Validating insights across multiple aggregation levels
- Identifying and contextualising outliers
- Communicating limitations alongside headline metrics

## Next steps

Potential extensions include:
- Linking dentist availability to population growth or oral health outcomes
- Segmenting trends by income level or development indicators
- Applying alternative anomaly detection methods such as IQR or percentile based thresholds
- Automating data refresh and dashboard updates for longitudinal monitoring