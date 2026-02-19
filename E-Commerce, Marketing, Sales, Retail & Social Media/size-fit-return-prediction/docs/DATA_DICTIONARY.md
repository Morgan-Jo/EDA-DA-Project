# DATA DICTIONARY — Size & Fit Return Prediction

**Project:** Size & Fit Return Prediction  
**Version:** 1.0  
**Last Updated:** 2026-02-18 
**Updated By:** Morgan Jo Tonner

> This document defines every field used in the analysis — both original dataset fields and derived/calculated fields created during cleaning.

---

## How to Update This Document

1. Add new rows to the relevant table when new fields are created
2. Update the `Last Updated` date in the header above
3. Record the change in `CHANGELOG.md` with a reference to this file
4. Never delete old field definitions — mark deprecated fields with ~~strikethrough~~ and add a note

---

## Section 1 — Original Dataset Fields

### 1A. ModCloth Dataset (`modcloth_final_data.json`)

| Field Name | Data Type | Description | Example Values | Notes / Nulls |
|---|---|---|---|---|
| `item_id` | Text | Unique identifier for the product | "item_001" | Rarely null |
| `user_id` | Text | Anonymised customer identifier | "user_4521" | May be null |
| `rating` | Integer | Customer product rating (1–5 stars) | 1, 2, 3, 4, 5 | Some nulls present |
| `review_text` | Text | Full customer review in plain English | "Runs small, sized up" | Can be null |
| `fit` | Text | Customer's fit assessment | "small", "fit", "large" | Key analysis field |
| `size` | Text/Numeric | Size the customer ordered | "M", "10", "XL" | Mixed formats |
| `size_chart` | Text | Standard size on the size chart | "M", "10" | May differ from `size` |
| `height` | Text/Numeric | Customer self-reported height | "5ft 4in", "64" | Mixed formats; needs cleaning |
| `weight` | Numeric | Customer self-reported weight (lbs) | 130, 145, 200 | Some outliers |
| `age` | Numeric | Customer age in years | 25, 34, 52 | Some nulls |
| `bust` | Numeric | Customer bust measurement (inches) | 34, 36, 40 | Frequent nulls |
| `waist` | Numeric | Customer waist measurement (inches) | 28, 30, 34 | Frequent nulls |
| `hips` | Numeric | Customer hip measurement (inches) | 36, 38, 42 | Frequent nulls |
| `cup_size` | Text | Bra cup size | "A", "B", "C", "D" | Frequent nulls |
| `category` | Text | Product clothing category | "dress", "top", "bottom", "outerwear" | Key segmentation field |
| `quality` | Integer | Customer quality rating (1–5) | 1, 2, 3, 4, 5 | May be null |
| `usual_size` | Text/Numeric | The size the customer usually wears | "M", "10" | Key for size_ratio calc |

### 1B. Rent the Runway Dataset (`renttherunway_final_data.json`)

| Field Name | Data Type | Description | Example Values | Notes / Nulls |
|---|---|---|---|---|
| `item_id` | Text | Unique identifier for the rental item | "item_789" | Rarely null |
| `user_id` | Text | Anonymised customer identifier | "user_9023" | May be null |
| `rating` | Integer | Customer rating (1–10 scale on this platform) | 1–10 | Note: different scale to ModCloth |
| `review_text` | Text | Full customer review | "Perfect for my event, ran a little small" | Can be null |
| `fit` | Text | Customer fit assessment | "small", "fit", "large" | Key analysis field |
| `size` | Text | Size rented | "4", "6", "8", "10" | Numeric sizing used |
| `height` | Text | Customer height in format "Xft Xin" | "5ft 4in" | Requires parsing |
| `weight` | Text | Customer weight as text string | "130lbs" | Requires cleaning |
| `age` | Numeric | Customer age | 28, 35 | Some nulls |
| `bust` | Numeric | Bust measurement (inches) | 34, 36 | Frequent nulls |
| `waist` | Numeric | Waist measurement (inches) | 28, 30 | Frequent nulls |
| `hips` | Numeric | Hip measurement (inches) | 36, 38 | Frequent nulls |
| `body_type` | Text | Customer self-reported body type | "hourglass", "pear", "straight" | Unique to this dataset |
| `cup_size` | Text | Bra cup size | "A", "B", "C", "D", "DD" | Frequent nulls |
| `rented_for` | Text | Occasion item was rented for | "wedding", "party", "work" | Good segmentation field |
| `category` | Text | Product category | "dress", "gown", "romper" | Key segmentation field |

---

## Section 2 — Derived / Calculated Fields

These fields are **created during analysis** — they do not exist in the raw data.

| Field Name | Created In | Data Type | Formula / Logic | Purpose |
|---|---|---|---|---|
| `platform` | Power Query | Text | `"ModCloth"` or `"RentTheRunway"` — hardcoded per query | Identifies data source after merging |
| `height_inches` | Power Query | Decimal | Parsed from "Xft Xin" string → `ft * 12 + in` | Standardised numeric height for analysis |
| `weight_clean` | Power Query | Decimal | Strip "lbs" suffix → convert to number | Standardised numeric weight |
| `fit_flag` | Power Query | Integer (0/1) | 1 if `review_text` contains fit-related keywords, else 0 | Binary indicator for fit-mention reviews |
| `size_ratio` | Power Query | Decimal | `size_ordered / usual_size` (numeric sizes only) | Measures how far ordered size deviates from usual size |
| `size_ratio_bucket` | Power Query | Text | Bucketed from `size_ratio`: <0.9, 0.9–1.0, 1.0–1.1, >1.1 | Categorical grouping for pivot analysis |
| `height_bucket` | Excel Column | Text | `IF(height_inches<62, "Under 5'2\"", IF(height_inches<66, "5'2\"-5'5\"", ...))` | Height range grouping for histograms |
| `weight_bucket` | Excel Column | Text | Bucketed in 10 lb intervals: "<120", "120–130", etc. | Weight range grouping for histograms |
| `return_flag` | Excel Column | Integer (0/1) | 1 if `review_text` contains "returning", "returned", "sending back" | Proxy for return behaviour (see Limitations) |
| `fit_keyword_group` | Excel Column | Text | Categorises review into: "Runs Small", "Runs Large", "True to Size", "Tight", "Loose", "Other" | Groups fit keyword sentiment |
| `rating_normalised` | Excel Column | Decimal | ModCloth: `rating / 5`; RentTheRunway: `rating / 10` | Normalises ratings to 0–1 scale for cross-platform comparison |

---

## Section 3 — Lookup / Reference Tables

### 3A. Standard Size Chart (`LOOKUP_SizeCharts` sheet)

Used to compare ordered sizes against standard industry measurement ranges.

| Column | Description |
|---|---|
| `size_label` | Standard size (XS, S, M, L, XL, 0, 2, 4, etc.) |
| `bust_min` | Minimum bust measurement for this size (inches) |
| `bust_max` | Maximum bust measurement |
| `waist_min` | Minimum waist measurement |
| `waist_max` | Maximum waist measurement |
| `hips_min` | Minimum hip measurement |
| `hips_max` | Maximum hip measurement |
| `height_petite_max` | Max height for petite classification (inches) |
| `height_tall_min` | Min height for tall classification |
| `source` | Where this size chart data came from |

---

## Section 4 — Categorical Value Definitions

### `fit` field values

| Value | Meaning |
|---|---|
| `"small"` | Customer says item fits small / they had to size up |
| `"fit"` | Customer says item fits as expected / true to size |
| `"large"` | Customer says item fits large / they should have sized down |
| null | Customer did not provide fit feedback |

### `size_ratio_bucket` values

| Value | Meaning | Interpretation |
|---|---|---|
| `"Ordered Too Small"` | size_ratio < 0.9 | Customer ordered a smaller size than usual — item may run large |
| `"True to Size (Small)"` | 0.9 ≤ size_ratio ≤ 1.0 | Slightly smaller than usual — borderline |
| `"True to Size (Large)"` | 1.0 < size_ratio ≤ 1.1 | Slightly larger than usual — borderline |
| `"Ordered Too Big"` | size_ratio > 1.1 | Customer ordered a larger size than usual — item may run small |
| `"Unknown"` | size_ratio = null | Cannot calculate — missing size data |

---

## Section 5 — Known Data Quality Issues

| Issue | Affected Field(s) | Severity | Resolution Applied |
|---|---|---|---|
| Mixed height formats | `height` (RTR) | Medium | Parsed in Power Query — see Phase 2B |
| Mixed size formats (numeric vs. letter) | `size`, `usual_size` | High | Size ratio only calculated where both values are numeric |
| Self-reported measurements | `height`, `weight`, `bust`, `waist`, `hips` | Medium | Accepted as-is; noted as limitation in report |
| Return proxy only (no actual return records) | `return_flag` | High | Clearly noted as proxy in all outputs |
| Different rating scales per platform | `rating` | Medium | Normalised field `rating_normalised` created |
| Null-heavy measurement fields | `bust`, `waist`, `hips` | Medium | Excluded from analyses requiring these fields |
| ModCloth vs. RTR category naming inconsistency | `category` | Low | Manual lookup table in `LOOKUP_SizeCharts` maps to standard categories |

---

*Last updated: 2026-02-19 | Version: 1.0*