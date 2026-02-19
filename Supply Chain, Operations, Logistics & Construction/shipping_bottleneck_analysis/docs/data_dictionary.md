# Data Dictionary: Global Shipping & Bottleneck Analysis

**Verision**: 1.0

**Status**: Active

**Last Updated**: 03/02/2026

## Overview
This document defines the fields used in the `shipping_logistics.db` and the final processed datasets. The data is grain-level per Shipping Order Item.

## Core Shipping Tables

**Table**: `shipping_data` **(Processed)**

This table contains the cleaned and standardized records from the DataCo Smart Supply Chain dataset.

| Column Name | Data Type | Description | Nullable | Example |
|--------|------------|-------------|----------|----------|
| order_id | INTEGER | Unique identifier for the customer order. | No | 18051 |
| shipping_mode |,VARCHAR | "The method used for transit (e.g., Standard, First Class)." | No | Second Class |
| scheduled_days |INTEGER | The target number of days for delivery agreed upon at checkout. | No | 4 |
| actual_days | INTEGER | The real-world number of days it took for the shipment to arrive. |No | 5 |
| days_diff | INTEGER | Calculated field: actual_days - scheduled_days. | No | 1 | 
| is_late | BOOLEAN |Flag (1 or 0) indicating if actual_days > scheduled_days. | No | 1 | 
| late_delivery_risk | FLOAT | A pre-calculated risk probability score from the source data. | Yes | 0.85 |
| order_city | VARCHAR | The destination or port city for the shipment. | No | London |
| order_region | VARCHAR | "Geographic region (e.g., Western Europe, Central America)." | No | Southeast Asia |
| order_status| VARCHAR | "The current state of the order (e.g., COMPLETE, PENDING)." | No | CLOSED| 

## Derived Business Metrics (Logic)
These definitions ensure consistent reporting across Python scripts and SQL views.

1. Late Delivery Rate (LDR)

    - **Formula**: (Total Late Shipments / Total Shipments) * 100
    - **Business Goal**: Any carrier or port with an LDR exceeding 15% is flagged as a high-priority bottleneck.

2. Delay Categorization

    To provide better context for non-technical managers, delays are binned into three categories:

    - **On-Time/Early**: days_diff <= 0
    - **Minor Delay**: 1 <= days_diff <= 3
    - **Critical Delay**: days_diff > 3

## Variable Mapping: Environmental Factors

While the raw dataset often uses numerical risks, for this analysis, we map them to qualitative categories in the `utils.py` script:

- **Risk Level 0**: "Stable" - No major weather or political disruptions reported.
- **Risk Level 1**: "Alert" - Minor weather delays (e.g., heavy rain) likely at origin port
- **Risk Level 2**: "High" - Major disruption (e.g., storm, strike) expected.
