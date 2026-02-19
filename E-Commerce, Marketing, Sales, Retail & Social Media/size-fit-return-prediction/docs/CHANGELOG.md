# 📝 CHANGELOG — Size & Fit Return Prediction

> This file records every meaningful change made to the project — workbooks, documentation, data, or analysis.  
> **How to update:** Add a new entry at the TOP of the relevant version section. Always include Date, Who, and What changed.

---

## Format Guide

```
## [Version] — YYYY-MM-DD

### Added
- New things created

### Changed  
- Modifications to existing things

### Fixed
- Bugs or errors corrected

### Removed
- Things deleted or deprecated

### Data
- Notes about raw data downloads, row counts, or dataset changes

### Notes
- Any context, decisions made, or things to revisit
```

---

## [v1.0] — 2026-02-18

### Added
- Initial project folder structure created
- `README.md` — full GitHub README for technical and non-technical audiences
- `PROJECT_PLAN.md` — 9-phase step-by-step project plan
- `DATA_DICTIONARY.md` — all original and derived field definitions
- `CHANGELOG.md` — this file
- `data/raw/` — placeholder folder for raw JSON files (not tracked in Git)
- `data/processed/` — placeholder for Power Query outputs
- `data/reference/` — placeholder for size chart reference data
- `excel/workbooks/` — placeholder for main Excel workbook
- `excel/templates/` — placeholder for reusable templates
- `docs/` — placeholder for changlog, data dictionary and project plan
- `visuals/` — placeholder for exported chart images
- `reports/` — placeholder for final reports

### Notes
- Project initiated
- Kaggle data not yet downloaded — see Phase 1 of PROJECT_PLAN.md
- All phases in PROJECT_PLAN.md are currently "Not Started"

<!-- FUTURE ENTRIES GO ABOVE THIS LINE -->

## [v1.1] - 2026-02-19

### Added
- Excel workbook 'SizeFit_RCA_Analysis.xlsx' created
- Excel workbook tab and sheet initialised
- Downloaded JSON files
- Stored JSON in 'data/raw'
- Created SOURCE_INFO.txt documenting:
  - Kaggle URL
  - Dataset author
  - Download date
  - File sizes
  - Licensing reference

### Changed
- Update README.md with Discliamer and License

<!-- FUTURE ENTRIES GO ABOVE THIS LINE -->

## [v1.2] — 2026-02-19

### Added
- Implemented Power Query workflow for ModCloth dataset (JSON Lines format)
- Created structured query `PQ_ModCloth`
- Added `fit_flag` column based on structured `fit` field
- Added `platform` column with constant value "ModCloth"
- Standardised column naming to snake_case format
- Applied consistent data types across all fields

### Changed
- Updated data import method from “From JSON” to manual NDJSON parsing via M script
- Revised project logic to remove dependency on `review_text` (not present in ModCloth dataset)
- Removed `size_ratio` calculation for ModCloth due to absence of `usual_size` field
- Adjusted RCA framework to focus on structured `fit` classification (small / fit / large)

### Fixed
- Resolved JSON parsing error caused by NDJSON format
- Corrected query expansion logic using `Record.FieldNames` method
- Removed rows where `size` was null to ensure usable sizing analysis

### Removed
- Deprecated original keyword-based `fit_flag` logic tied to `review_text`
- Removed incomplete JSON connector import attempt

### Data
- ModCloth cleaned row count: 82,790 records
- Null `size` records removed
- Data types validated for numeric and categorical fields
- Raw JSON file remains unchanged in `data/raw/`

### Notes
- ModCloth dataset does not include `usual_size`; size_ratio metric will not be computed for this platform
- Future cross-platform comparison will require schema alignment during Phase 3
- Height remains in text format ("5ft 6in") and may require standardisation later

<!-- FUTURE ENTRIES GO ABOVE THIS LINE -->

