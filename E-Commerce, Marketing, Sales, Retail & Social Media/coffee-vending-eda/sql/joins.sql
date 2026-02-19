/* ============================================================
   Coffee Vending Machine Sales — join.sql
   Purpose: Join-ready transformations and final analytical table
   Role level: Data Analyst (3+ years experience)
   Engine: SQLite (VS Code friendly)

   Assumptions:
   - coffee_sales_1 and coffee_sales_2 already loaded
   - EDA completed separately on each dataset
   - Goal is a clean, analysis-ready fact table for Tableau
   ============================================================ */


/* =========================
   1) STANDARDISE BOTH DATASETS
   =========================
   Why:
   - Align schemas before union
   - Enforce consistent data types
   - Create explicit analytical fields
*/

DROP VIEW IF EXISTS stg_coffee_sales_1;
DROP VIEW IF EXISTS stg_coffee_sales_2;

CREATE VIEW stg_coffee_sales_1 AS
SELECT
  date(date)                     AS sale_date,
  datetime(datetime)             AS sale_ts,
  CAST(strftime('%H', datetime(datetime)) AS INTEGER) AS sale_hour,
  CAST(strftime('%w', date(date)) AS INTEGER)         AS sale_dow,
  cash_type,
  card                           AS customer_id,
  coffee_name,
  CAST(money AS REAL)            AS amount,
  'index_1'                      AS source_dataset
FROM coffee_sales_1
WHERE money IS NOT NULL
  AND money > 0;

CREATE VIEW stg_coffee_sales_2 AS
SELECT
  date(date)                     AS sale_date,
  datetime(datetime)             AS sale_ts,
  CAST(strftime('%H', datetime(datetime)) AS INTEGER) AS sale_hour,
  CAST(strftime('%w', date(date)) AS INTEGER)         AS sale_dow,
  cash_type,
  NULL                           AS customer_id,
  coffee_name,
  CAST(money AS REAL)            AS amount,
  'index_2'                      AS source_dataset
FROM coffee_sales_2
WHERE money IS NOT NULL
  AND money > 0;


/* =========================
   2) UNION INTO FACT TABLE
   =========================
   Why:
   - Same grain: one row per transaction
   - Preserve data lineage via source_dataset
*/

DROP TABLE IF EXISTS fact_coffee_sales;

CREATE TABLE fact_coffee_sales AS
SELECT * FROM stg_coffee_sales_1
UNION ALL
SELECT * FROM stg_coffee_sales_2;


/* =========================
   3) DERIVED ANALYTICAL FIELDS
   =========================
   Why:
   - Reduce logic in Tableau
   - Enable consistent filtering and grouping
*/

DROP VIEW IF EXISTS analytics_coffee_sales;

CREATE VIEW analytics_coffee_sales AS
SELECT
  sale_date,
  sale_ts,
  sale_hour,
  CASE sale_dow
    WHEN 0 THEN 'Sun'
    WHEN 1 THEN 'Mon'
    WHEN 2 THEN 'Tue'
    WHEN 3 THEN 'Wed'
    WHEN 4 THEN 'Thu'
    WHEN 5 THEN 'Fri'
    WHEN 6 THEN 'Sat'
  END                             AS sale_day,
  strftime('%Y-%m', sale_date)    AS sale_month,
  cash_type,
  coffee_name,
  customer_id,
  CASE
    WHEN customer_id IS NOT NULL THEN 'identified'
    ELSE 'anonymous'
  END                             AS customer_type,
  amount,
  source_dataset
FROM fact_coffee_sales;


/* =========================
   4) DATA INTEGRITY CHECKS
   =========================
   Why:
   - Validate join logic
   - Ensure no row loss or inflation
*/

-- Row counts by source
SELECT
  source_dataset,
  COUNT(*) AS transactions,
  ROUND(SUM(amount), 2) AS revenue
FROM analytics_coffee_sales
GROUP BY source_dataset;

-- Date range validation
SELECT
  MIN(sale_date) AS min_date,
  MAX(sale_date) AS max_date,
  COUNT(*)       AS total_transactions
FROM analytics_coffee_sales;

-- Duplicate detection (should return zero rows)
SELECT
  sale_ts,
  coffee_name,
  cash_type,
  amount,
  customer_id,
  COUNT(*) AS dup_count
FROM analytics_coffee_sales
GROUP BY sale_ts, coffee_name, cash_type, amount, customer_id
HAVING COUNT(*) > 1;


/* =========================
   5) FINAL OUTPUT CONFIRMATION
   =========================
   This is the table/view Tableau should connect to
*/

-- Recommended Tableau source
SELECT * FROM analytics_coffee_sales LIMIT 100;
