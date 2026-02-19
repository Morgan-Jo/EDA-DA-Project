# 📋 PROJECT PLAN — Size & Fit Return Prediction EDA

**Project:** Size & Fit Return Prediction — Retail Apparel  
**Tool:** Microsoft Excel (Power Query, Pivot Tables, Charts)  
**Framework:** Root Cause Analysis (RCA)  
**Analyst:** Morgan Jo Tonner
**Start Date:** 2026-02-18  
**Status:** 🟡 In Progress


## How to Read This Plan

This plan is written so **anyone** can follow it — technical or not. Each phase has:
- A plain-English summary of what we're doing and **why**
- Exact step-by-step instructions for Excel
- A checklist so you can tick off your progress
- Estimated time for each phase


## Project Phases at a Glance

| Phase | Name | Who | Est. Time | Status |
|---|---|---|---|---|
| 0 | Setup & Environment | Analyst | 1 hour | 🟩 Completed |
| 1 | Data Acquisition | Analyst | 30 min | ⬜ Not started |
| 2 | Data Cleaning (Power Query) | Analyst | 3–4 hours | ⬜ Not started |
| 3 | Data Merging | Analyst | 1–2 hours | ⬜ Not started |
| 4 | Keyword Extraction (Fit Reviews) | Analyst | 1–2 hours | ⬜ Not started |
| 5 | Size Ratio Analysis (Pivot Tables) | Analyst | 2 hours | ⬜ Not started |
| 6 | Measurement Distribution (Histograms) | Analyst | 2 hours | ⬜ Not started |
| 7 | Root Cause Analysis | Analyst | 2–3 hours | ⬜ Not started |
| 8 | Reporting & Visuals | Analyst | 2–3 hours | ⬜ Not started |
| 9 | Documentation & GitHub Upload | Analyst | 1 hour | ⬜ Not started |

**Total Estimated Time: ~16–20 hours**


## PHASE 0 — Setup & Environment

### What & Why
Before we touch the data, we get organised. A clean folder structure prevents confusion later and makes the project easy for others (and future-you) to navigate.

### Steps

- [x] **0.1** Create the project folder structure as defined in `README.md`
- [x] **0.2** Download and install Excel (Microsoft 365 recommended for full Power Query support)
- [x] **0.3** Create a blank Excel workbook named `SizeFit_RCA_Analysis.xlsx` and save it in `excel/workbooks/`
- [x] **0.4** In the workbook, create the following blank sheets in this order:
  - `START_HERE`
  - `PQ_ModCloth`
  - `PQ_RunwayMerge`
  - `RCA_FitKeywords`
  - `PIVOT_SizeRatios`
  - `PIVOT_Demographics`
  - `HIST_Measurements`
  - `CHART_ReturnReasons`
  - `RCA_Fishbone`
  - `LOOKUP_SizeCharts`
  - `DOCS`
- [x] **0.5** Colour-code the sheet tabs:
  - 🟦 Blue: Data sheets (PQ_*)
  - 🟩 Green: Analysis sheets (PIVOT_*, HIST_*, CHART_*)
  - 🟧 Orange: Insight sheets (RCA_*)
  - ⬜ Grey: Reference/Documentation sheets (LOOKUP_*, DOCS, START_HERE)
- [x] **0.6** On `START_HERE`, create a navigation table with hyperlinks to each sheet, a project description paragraph, and a "last updated" date cell
- [x] **0.7** Initialise `CHANGELOG.md` with v1.0 entry


## PHASE 1 — Data Acquisition

### What & Why (Plain English)
We are getting our raw data. Think of this like going to the library and collecting the books we'll study. The data comes from Kaggle — a website where data analysts share datasets.

### Steps

- [x] **1.1** Go to [Kaggle.com](https://www.kaggle.com) and create a free account if you don't have one
- [x] **1.2** Search for: **"Clothing Fit Dataset for Size Recommendation"** or **"modcloth renttherunway fit"**
  - Target dataset: one containing both `modcloth_final_data.json` and `renttherunway_final_data.json`
  - Recommended search: "fit prediction women clothing kaggle"
- [x] **1.3** Download both JSON files
- [x] **1.4** Place both files in `data/raw/`
- [x] **1.5** Do NOT rename the files — keep original names for reproducibility
- [x] **1.6** Note the download date and Kaggle URL in `CHANGELOG.md`
- [x] **1.7** Create a `data/raw/SOURCE_INFO.txt` file recording:
  - Kaggle dataset URL
  - Download date
  - File sizes
  - Dataset author/owner

> **Non-technical note:** JSON files look like messy text if you open them in Notepad — that's normal. Excel's Power Query tool will turn them into clean, readable tables for us automatically.


## PHASE 2 — Data Cleaning with Power Query

### What & Why (Plain English)
Raw data is almost never perfect. This phase is like sorting through a messy pile of customer feedback cards — removing blanks, fixing typos in formatting, and making sure everything is in a consistent layout. We use Excel's built-in Power Query tool to do this without touching or breaking the original files.

### 2A — Load ModCloth Data

- [x] **2A.1** Open `SizeFit_RCA_Analysis.xlsx`
- [x] **2A.2** Go to **Data tab → Get Data → From File → From JSON**
- [x] **2A.3** Navigate to `data/raw/modcloth_final_data.json` and click Import
- [x] **2A.4** In the Power Query Editor that opens, click **"To Table"** button (top left) if data shows as a list
- [x] **2A.5** Click the expand icon (double arrows) on the `Column1` header to expand all fields
- [x] **2A.6** Apply the following transformations in order:

| Step # | Action | How To Do It In Power Query |
|---|---|---|
| 1 | Rename columns to snake_case | Right-click column header → Rename |
| 2 | Remove completely empty rows | Home → Remove Rows → Remove Blank Rows |
| 3 | Change `height` to number | Click column → Transform → Data Type → Decimal Number |
| 4 | Change `weight` to number | Same as above |
| 5 | Change `size` to text | Click column → Transform → Data Type → Text |
| 6 | Remove rows where both `size` AND `height` are null | Home → Remove Rows → Remove Rows with Errors (then filter) |
| 7 | Add `fit_flag` column | Add Column → Custom Column → formula below |
| 8 | Add `platform` column | Add Column → Custom Column → `= "ModCloth"` |
| 9 | Add `size_ratio` column | Add Column → Custom Column → formula below |

**fit_flag formula (M language):**
```
if Text.Contains(Text.Lower([review_text]), "fit") or
   Text.Contains(Text.Lower([review_text]), "small") or
   Text.Contains(Text.Lower([review_text]), "large") or
   Text.Contains(Text.Lower([review_text]), "tight") or
   Text.Contains(Text.Lower([review_text]), "big") or
   Text.Contains(Text.Lower([review_text]), "loose")
then 1 else 0
```

**size_ratio formula (M language):**
```
if [usual_size] <> null and [usual_size] <> 0
then [size_ordered] / [usual_size]
else null
```

- [x] **2A.7** Go to **Home → Close & Load To...** → Select "Table" → Load to sheet `PQ_ModCloth`
- [x] **2A.8** Note the row count once loaded (record in CHANGELOG.md)

### 2B — Load Rent the Runway Data

- [ ] **2B.1** Repeat steps 2A.2–2A.5 for `renttherunway_final_data.json`
- [ ] **2B.2** Apply same column renames as ModCloth (match schema)
- [ ] **2B.3** Extra step — parse height: Rent the Runway stores height as "5ft 4in"
  - Add Custom Column: `height_inches`
  - Formula to convert "5ft 4in" → decimal:
  ```
  let
    h = Text.Trim([height]),
    ft = Number.FromText(Text.BeforeDelimiter(h, "ft")),
    inPart = Text.Trim(Text.BetweenDelimiters(h, "ft", "in")),
    inches = if inPart = "" then 0 else Number.FromText(inPart)
  in
    ft * 12 + inches
  ```
- [ ] **2B.4** Add `fit_flag` column (same formula as ModCloth)
- [ ] **2B.5** Add `platform` column = `"RentTheRunway"`
- [ ] **2B.6** Do NOT load yet — keep query open for Phase 3


## PHASE 3 — Data Merging

### What & Why (Plain English)
We have two separate datasets. To compare them and look for patterns across both, we need to combine them into one big table — like stacking two piles of cards into one unified deck.

### Steps

- [ ] **3.1** In Power Query, create a new query: **Home → Append Queries as New**
- [ ] **3.2** Select both the ModCloth query and the RentTheRunway query
- [ ] **3.3** Click OK — Power Query will stack them vertically (append)
- [ ] **3.4** Rename this new combined query to: `MergedFitData`
- [ ] **3.5** Add a `size_ratio_bucket` column to categorise size_ratio:
  ```
  if [size_ratio] = null then "Unknown"
  else if [size_ratio] < 0.9 then "Ordered Too Small"
  else if [size_ratio] <= 1.0 then "True to Size (Small)"
  else if [size_ratio] <= 1.1 then "True to Size (Large)"
  else "Ordered Too Big"
  ```
- [ ] **3.6** Load to sheet `PQ_RunwayMerge`
- [ ] **3.7** Record final merged row count in CHANGELOG.md


## PHASE 4 — Keyword Extraction (Fit Review Text)

### What & Why (Plain English)
Customers write reviews that tell us HOW clothes fit them. Words like "runs small," "too tight," or "perfect fit" are clues. This phase counts and categorises those clues systematically.

### Steps

- [ ] **4.1** Go to sheet `RCA_FitKeywords`
- [ ] **4.2** Set up a keyword frequency table with these columns:
  - `keyword` | `count_modcloth` | `count_runway` | `count_total` | `% of fit-flagged reviews`
- [ ] **4.3** Keywords to track:

| Keyword Group | Keywords to Count |
|---|---|
| Runs Small | "runs small", "too small", "size up", "smaller than" |
| Runs Large | "runs large", "too big", "size down", "larger than" |
| Tight Fit | "tight", "too tight", "constricting", "snug" |
| Loose Fit | "loose", "too loose", "baggy", "roomy" |
| Perfect Fit | "perfect fit", "true to size", "fits perfectly", "fits well" |
| Return Intent | "returning", "returned", "sending back", "not keeping" |

- [ ] **4.4** Use `COUNTIF` formulas pointing to `PQ_RunwayMerge` review column:
  ```excel
  =COUNTIF(PQ_RunwayMerge[review_text],"*runs small*")
  ```
- [ ] **4.5** Create a Pareto chart (bar chart sorted high to low with cumulative % line) showing keyword frequency
- [ ] **4.6** Add a slicer or dropdown to filter by platform

---

## PHASE 5 — Size Ratio Analysis (Pivot Tables)

### What & Why (Plain English)
Now we answer the central question: Do people who ordered the "wrong" size return more? We use Pivot Tables — Excel's way of summarising large amounts of data into digestible summaries.

### Steps

- [ ] **5.1** Click anywhere in the `PQ_RunwayMerge` table
- [ ] **5.2** Go to **Insert → PivotTable** → Place in sheet `PIVOT_SizeRatios`

**Pivot Table 1 — Size Ratio vs. Return Flag:**
- [ ] **5.3** Configure:
  - **Rows:** `size_ratio_bucket`
  - **Columns:** `category` (dress, top, bottom, etc.)
  - **Values:** Count of `return_flag` AND % of row total
- [ ] **5.4** Add Slicers for: `platform`, `fit_flag`
- [ ] **5.5** Apply conditional formatting: Red = high return %, Green = low return %

**Pivot Table 2 — Size Ratio vs. Fit Feedback:**
- [ ] **5.6** Add second pivot in same sheet:
  - **Rows:** `size_ratio_bucket`
  - **Values:** Average `fit_score` (if available: 1=small, 3=fit, 5=large)
- [ ] **5.7** Create a clustered bar chart from Pivot Table 1

**Pivot Table 3 — Category vs. Return Rate (PIVOT_Demographics sheet):**
- [ ] **5.8** In `PIVOT_Demographics` sheet:
  - **Rows:** `height_bucket` (you'll need to create this — see note below)
  - **Columns:** `size_ratio_bucket`
  - **Values:** Count of records, % with fit complaints

> **Creating height_bucket:** In the merged data table, add a helper column:
> `=IF([@height_inches]<62,"Under 5'2\"", IF([@height_inches]<66,"5'2\"-5'5\"", IF([@height_inches]<70,"5'6\"-5'9\"","Over 5'9\"")))`

---

## PHASE 6 — Measurement Distribution Histograms

### What & Why (Plain English)
Brand size charts assume customers fit within certain height and weight ranges. But what if most customers are actually outside those ranges? A histogram shows us the shape of our customer measurements — like a profile of who's actually shopping.

### Steps

- [ ] **6.1** Go to sheet `HIST_Measurements`
- [ ] **6.2** Extract height and weight columns from `PQ_RunwayMerge` (copy values only to a helper range)

**Histogram 1 — Customer Height Distribution:**
- [ ] **6.3** Select height data → Insert → Chart → Histogram
- [ ] **6.4** Set bin width to 2 inches
- [ ] **6.5** Add vertical reference lines (drawn as error bars or shapes) showing standard size chart height ranges:
  - Petite range: 60"–63" (5'0"–5'3")
  - Regular range: 63"–67" (5'3"–5'7")
  - Tall range: 67"+ (5'7"+)
- [ ] **6.6** Label the chart clearly: "Customer Height vs. Size Chart Ranges"

**Histogram 2 — Customer Weight Distribution:**
- [ ] **6.7** Select weight data → Insert → Chart → Histogram
- [ ] **6.8** Set bin width to 10 lbs
- [ ] **6.9** Add reference lines for approximate size chart weight thresholds
- [ ] **6.10** Overlay a second series showing average weight of customers who complained about fit

**Histogram 3 — Size Ratio Distribution:**
- [ ] **6.11** Select `size_ratio` column → Insert → Histogram
- [ ] **6.12** Set bin width to 0.1
- [ ] **6.13** This shows how concentrated or spread the "wrong size" orders are
- [ ] **6.14** Add a normal distribution curve overlay if desired (calculated manually with NORM.DIST formula)

---

## PHASE 7 — Root Cause Analysis

### What & Why (Plain English)
We've found patterns. Now we ask "why?" repeatedly until we find the actual root causes — not just symptoms. This is like a detective's "so what?" moment. We use the "5 Whys" technique.

### Fishbone / Ishikawa Diagram (Manual Build in Excel)

- [ ] **7.1** Go to sheet `RCA_Fishbone`
- [ ] **7.2** Draw a fishbone diagram using Excel shapes (Insert → Shapes):
  - Central arrow pointing right to "Effect: High Fit-Related Return Rate"
  - 6 diagonal bones representing cause categories:
    1. **Brand/Product** (size chart inaccuracy, inconsistent grading)
    2. **Customer** (measurement error, size chart misreading)
    3. **Platform** (poor size guidance, no fit quiz)
    4. **Product Design** (stretch fabric vs. rigid, style-specific fit)
    5. **Data/Information** (missing size info, vague product descriptions)
    6. **Demographics** (customer measurement spread outside standard ranges)

- [ ] **7.3** For each bone, add text boxes with specific data-backed findings from Phases 4–6
- [ ] **7.4** Link findings to the fishbone with comment boxes referencing specific pivot results

### 5 Whys Analysis Table

- [ ] **7.5** Below the fishbone, create a 5 Whys table:

| Why # | Question | Answer (Data-Backed) |
|---|---|---|
| Why 1 | Why do customers return items? | X% cite fit/size issues (from keyword analysis) |
| Why 2 | Why do fit/size issues occur? | X% of returns ordered outside their usual size |
| Why 3 | Why did they order outside their usual size? | Size ratio analysis shows [pattern] |
| Why 4 | Why did size ratio mismatch happen? | Product descriptions / size charts [finding] |
| Why 5 | Why are size charts inaccurate/insufficient? | Customer measurements span [range] vs. chart [range] |

- [ ] **7.6** Summarise root causes in plain English in a text box at the bottom of the sheet

---

## PHASE 8 — Reporting & Visuals

### What & Why (Plain English)
Time to package our findings so anyone — managers, stakeholders, customers — can understand them without needing to dig through spreadsheets.

### Steps

- [ ] **8.1** Export key charts as PNG files to `visuals/`:
  - Pareto chart of return keywords
  - Size ratio vs. return rate chart
  - Height/weight histograms with size chart overlays
  - Fishbone diagram screenshot
- [ ] **8.2** Create a summary report document `reports/Final_Findings_Report.md` with:
  - Executive Summary (3–5 bullet points for non-technical readers)
  - Methodology section (for technical readers)
  - Key Findings with charts embedded
  - Limitations
  - Recommendations
- [ ] **8.3** Create a one-page `reports/Executive_Summary.md` with only top 3 findings and recommendations (for stakeholders)
- [ ] **8.4** In the `START_HERE` Excel sheet, add a "Key Insights" summary section with the top 5 findings in plain text
- [ ] **8.5** Apply consistent colour theme across all charts (use brand colours or a professional palette)

---

## PHASE 9 — Documentation & GitHub Upload

### What & Why (Plain English)
This phase makes the project shareable and professional. Good documentation means someone else (or you, 6 months from now) can pick this project up and understand everything that was done and why.

### Steps

- [ ] **9.1** Finalise `DATA_DICTIONARY.md` with all field definitions
- [ ] **9.2** Update `CHANGELOG.md` with all phases completed
- [ ] **9.3** Review `README.md` — update Key Findings section with real results
- [ ] **9.4** Create `01_data/raw/.gitignore` to exclude raw JSON files from GitHub (data too large)
- [ ] **9.5** Create a `.gitignore` in root to exclude temp files
- [ ] **9.6** Initialise a Git repository in the project folder:
  ```bash
  git init
  git add .
  git commit -m "v1.0 - Initial project setup and documentation"
  ```
- [ ] **9.7** Push to GitHub:
  ```bash
  git remote add origin https://github.com/Morgan-Jo/EDA-DA-Project.git
  git push -u origin main
  ```
- [ ] **9.8** Add GitHub Topics to the repository: `excel`, `data-analysis`, `retail`, `eda`, `power-query`, `root-cause-analysis`
- [ ] **9.9** Add a project description on GitHub: "Excel-based EDA investigating size & fit return patterns in retail apparel using Power Query, Pivot Tables, and Root Cause Analysis"

---

## Project Completion Checklist

- [ ] All 9 phases complete
- [ ] All Excel sheets named and colour-coded
- [ ] README.md Key Findings section updated with real data
- [ ] All charts exported to 04_visuals/
- [ ] Final report written in 05_reports/
- [ ] DATA_DICTIONARY.md complete
- [ ] CHANGELOG.md up to date
- [ ] GitHub repository live and public

---

*Last updated: 2026-02-19 | Version: 1.1*