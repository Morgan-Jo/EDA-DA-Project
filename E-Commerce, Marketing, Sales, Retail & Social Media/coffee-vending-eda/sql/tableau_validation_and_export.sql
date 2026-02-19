/* ============================================================
   Coffee Vending Machine Sales — Tableau Validation & Export
   File: tableau_validation_and_export.sql
   Engine: SQLite CLI

   Purpose:
   - Validate analytics dataset for NULLs
   - Create a Tableau-safe view
   - Export a clean CSV for dashboarding
   ============================================================ */


/* =========================
   1) NULL CHECK SUMMARY
   ========================= */

SELECT
  SUM(CASE WHEN sale_date IS NULL THEN 1 ELSE 0 END) AS null_sale_date,
  SUM(CASE WHEN sale_ts IS NULL THEN 1 ELSE 0 END) AS null_sale_ts,
  SUM(CASE WHEN sale_hour IS NULL THEN 1 ELSE 0 END) AS null_sale_hour,
  SUM(CASE WHEN sale_day IS NULL THEN 1 ELSE 0 END) AS null_sale_day,
  SUM(CASE WHEN sale_month IS NULL THEN 1 ELSE 0 END) AS null_sale_month,
  SUM(CASE WHEN cash_type IS NULL THEN 1 ELSE 0 END) AS null_cash_type,
  SUM(CASE WHEN coffee_name IS NULL THEN 1 ELSE 0 END) AS null_coffee_name,
  SUM(CASE WHEN amount IS NULL THEN 1 ELSE 0 END) AS null_amount,
  SUM(CASE WHEN customer_type IS NULL THEN 1 ELSE 0 END) AS null_customer_type,
  SUM(CASE WHEN source_dataset IS NULL THEN 1 ELSE 0 END) AS null_source
FROM analytics_coffee_sales;


/* =========================
   2) INSPECT BAD ROWS
   ========================= */

SELECT *
FROM analytics_coffee_sales
WHERE
  sale_date IS NULL
  OR amount IS NULL
  OR coffee_name IS NULL
LIMIT 50;


/* =========================
   3) CREATE TABLEAU-SAFE VIEW
   =========================
   Business rules:
   - Critical fields must not be NULL
   - Customer_id may be NULL (cash transactions)
   - Text fields default to 'unknown'
*/

DROP VIEW IF EXISTS tableau_coffee_sales;

CREATE VIEW tableau_coffee_sales AS
SELECT
  sale_date,
  sale_ts,
  sale_hour,
  sale_day,
  sale_month,
  COALESCE(TRIM(cash_type), 'unknown') AS cash_type,
  COALESCE(TRIM(coffee_name), 'unknown') AS coffee_name,
  customer_type,
  customer_id,
  COALESCE(amount, 0) AS amount,
  source_dataset
FROM analytics_coffee_sales
WHERE
  sale_date IS NOT NULL
  AND amount IS NOT NULL
  AND coffee_name IS NOT NULL;


/* =========================
   4) FINAL VALIDATION
   ========================= */

SELECT
  COUNT(*) AS total_rows,
  MIN(sale_date) AS min_date,
  MAX(sale_date) AS max_date,
  ROUND(SUM(amount), 2) AS total_revenue
FROM tableau_coffee_sales;


/* =========================
   5) EXPORT FOR TABLEAU
   =========================
   Output file:
   data/processed/tableau_coffee_sales.csv
*/

.headers on
.mode csv
.output "data/processed/tableau_coffee_sales.csv"

SELECT *
FROM tableau_coffee_sales
ORDER BY sale_date, sale_ts;

.output stdout
