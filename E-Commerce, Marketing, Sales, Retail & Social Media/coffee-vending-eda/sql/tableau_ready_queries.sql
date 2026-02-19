/* ============================================================
   Coffee Vending Machine Sales — Tableau-Ready Export Queries
   Engine: SQLite (works well with VS Code + SQLite extensions)

   What this file does:
   1) Builds a unified VIEW (v_coffee_sales) from two source tables
   2) Provides Tableau-ready SELECT statements you can export to CSV

   Expected source tables:
   - coffee_sales_1(date, datetime, cash_type, card, money, coffee_name)
   - coffee_sales_2(date, datetime, cash_type, money, coffee_name)

   Tip:
   Run each SELECT block and export the results to /data/processed/
   ============================================================ */


/* -----------------------------
   0) Unified view for analysis
   ----------------------------- */

DROP VIEW IF EXISTS v_coffee_sales;

CREATE VIEW v_coffee_sales AS
SELECT
  date(date)         AS sale_date,
  datetime(datetime) AS sale_ts,
  cash_type,
  card               AS customer_id,
  CAST(money AS REAL) AS money,
  coffee_name,
  'index_1'          AS source
FROM coffee_sales_1

UNION ALL

SELECT
  date(date)         AS sale_date,
  datetime(datetime) AS sale_ts,
  cash_type,
  NULL               AS customer_id,
  CAST(money AS REAL) AS money,
  coffee_name,
  'index_2'          AS source
FROM coffee_sales_2;


/* -----------------------------------------
   1) Daily trend (core time series export)
   Filename suggestion: tableau_daily_trend.csv
   ----------------------------------------- */
SELECT
  sale_date,
  COUNT(*)                 AS transactions,
  ROUND(SUM(money), 2)     AS revenue,
  ROUND(AVG(money), 2)     AS avg_ticket,
  ROUND(MIN(money), 2)     AS min_ticket,
  ROUND(MAX(money), 2)     AS max_ticket
FROM v_coffee_sales
GROUP BY sale_date
ORDER BY sale_date;


/* -----------------------------------------
   2) Weekly trend (Monday week start)
   Filename suggestion: tableau_weekly_trend.csv
   ----------------------------------------- */
SELECT
  date(sale_date, '-' || ((CAST(strftime('%w', sale_date) AS INTEGER) + 6) % 7) || ' days') AS week_start,
  COUNT(*)                 AS transactions,
  ROUND(SUM(money), 2)     AS revenue,
  ROUND(AVG(money), 2)     AS avg_ticket
FROM v_coffee_sales
GROUP BY week_start
ORDER BY week_start;


/* -----------------------------------------
   3) Monthly trend
   Filename suggestion: tableau_monthly_trend.csv
   ----------------------------------------- */
SELECT
  strftime('%Y-%m', sale_date) AS year_month,
  COUNT(*)                      AS transactions,
  ROUND(SUM(money), 2)          AS revenue,
  ROUND(AVG(money), 2)          AS avg_ticket
FROM v_coffee_sales
GROUP BY year_month
ORDER BY year_month;


/* -----------------------------------------
   4) Product performance (leaderboard)
   Filename suggestion: tableau_product_leaderboard.csv
   ----------------------------------------- */
SELECT
  coffee_name,
  COUNT(*)                 AS purchases,
  ROUND(SUM(money), 2)     AS revenue,
  ROUND(AVG(money), 2)     AS avg_price,
  ROUND(MIN(money), 2)     AS min_price,
  ROUND(MAX(money), 2)     AS max_price
FROM v_coffee_sales
GROUP BY coffee_name
ORDER BY revenue DESC, purchases DESC;


/* ---------------------------------------------------
   5) Product performance over time (daily x product)
   Filename suggestion: tableau_product_daily.csv
   --------------------------------------------------- */
SELECT
  sale_date,
  coffee_name,
  COUNT(*)                 AS purchases,
  ROUND(SUM(money), 2)     AS revenue,
  ROUND(AVG(money), 2)     AS avg_price
FROM v_coffee_sales
GROUP BY sale_date, coffee_name
ORDER BY sale_date, coffee_name;


/* -----------------------------------------
   6) Payment method over time (daily x cash_type)
   Filename suggestion: tableau_payment_daily.csv
   ----------------------------------------- */
SELECT
  sale_date,
  cash_type,
  COUNT(*)                 AS transactions,
  ROUND(SUM(money), 2)     AS revenue,
  ROUND(AVG(money), 2)     AS avg_ticket
FROM v_coffee_sales
GROUP BY sale_date, cash_type
ORDER BY sale_date, cash_type;


/* -----------------------------------------
   7) Hourly sales (time-of-day)
   Filename suggestion: tableau_hourly_sales.csv
   ----------------------------------------- */
SELECT
  CAST(strftime('%H', sale_ts) AS INTEGER) AS hour,
  COUNT(*)                 AS transactions,
  ROUND(SUM(money), 2)     AS revenue,
  ROUND(AVG(money), 2)     AS avg_ticket
FROM v_coffee_sales
GROUP BY hour
ORDER BY hour;


/* -----------------------------------------
   8) Day-of-week performance
   Filename suggestion: tableau_dow_sales.csv
   ----------------------------------------- */
SELECT
  CAST(strftime('%w', sale_date) AS INTEGER) AS dow_num,
  CASE CAST(strftime('%w', sale_date) AS INTEGER)
    WHEN 0 THEN 'Sun'
    WHEN 1 THEN 'Mon'
    WHEN 2 THEN 'Tue'
    WHEN 3 THEN 'Wed'
    WHEN 4 THEN 'Thu'
    WHEN 5 THEN 'Fri'
    WHEN 6 THEN 'Sat'
  END AS dow,
  COUNT(*)                 AS transactions,
  ROUND(SUM(money), 2)     AS revenue,
  ROUND(AVG(money), 2)     AS avg_ticket
FROM v_coffee_sales
GROUP BY dow_num, dow
ORDER BY dow_num;


/* -----------------------------------------
   9) Heatmap table (day-of-week x hour)
   Filename suggestion: tableau_heatmap_dow_hour.csv
   ----------------------------------------- */
SELECT
  CAST(strftime('%w', sale_date) AS INTEGER) AS dow_num,
  CASE CAST(strftime('%w', sale_date) AS INTEGER)
    WHEN 0 THEN 'Sun'
    WHEN 1 THEN 'Mon'
    WHEN 2 THEN 'Tue'
    WHEN 3 THEN 'Wed'
    WHEN 4 THEN 'Thu'
    WHEN 5 THEN 'Fri'
    WHEN 6 THEN 'Sat'
  END AS dow,
  CAST(strftime('%H', sale_ts) AS INTEGER) AS hour,
  COUNT(*)                 AS transactions,
  ROUND(SUM(money), 2)     AS revenue
FROM v_coffee_sales
GROUP BY dow_num, dow, hour
ORDER BY dow_num, hour;


/* -----------------------------------------
   10) Customer export (card-only customers)
   Filename suggestion: tableau_customers.csv
   ----------------------------------------- */
SELECT
  customer_id,
  COUNT(*)                 AS purchases,
  ROUND(SUM(money), 2)     AS revenue,
  ROUND(AVG(money), 2)     AS avg_ticket,
  MIN(sale_date)           AS first_purchase_date,
  MAX(sale_date)           AS last_purchase_date
FROM v_coffee_sales
WHERE customer_id IS NOT NULL
GROUP BY customer_id
ORDER BY revenue DESC;


/* -----------------------------------------
   11) Customer x Product matrix (card-only)
   Filename suggestion: tableau_customer_product.csv
   ----------------------------------------- */
SELECT
  customer_id,
  coffee_name,
  COUNT(*)                 AS purchases,
  ROUND(SUM(money), 2)     AS revenue,
  ROUND(AVG(money), 2)     AS avg_price
FROM v_coffee_sales
WHERE customer_id IS NOT NULL
GROUP BY customer_id, coffee_name
ORDER BY purchases DESC, revenue DESC;


/* -----------------------------------------
   12) Next-day revenue alignment (EDA momentum)
   Filename suggestion: tableau_next_day_revenue.csv
   ----------------------------------------- */
WITH daily AS (
  SELECT sale_date, SUM(money) AS revenue
  FROM v_coffee_sales
  GROUP BY sale_date
)
SELECT
  sale_date,
  ROUND(revenue, 2) AS revenue,
  ROUND(LEAD(revenue) OVER (ORDER BY sale_date), 2) AS next_day_revenue
FROM daily
ORDER BY sale_date;


/* -----------------------------------------
   13) Next-week revenue alignment
   Filename suggestion: tableau_next_week_revenue.csv
   ----------------------------------------- */
WITH weekly AS (
  SELECT
    date(sale_date, '-' || ((CAST(strftime('%w', sale_date) AS INTEGER) + 6) % 7) || ' days') AS week_start,
    SUM(money) AS revenue
  FROM v_coffee_sales
  GROUP BY week_start
)
SELECT
  week_start,
  ROUND(revenue, 2) AS revenue,
  ROUND(LEAD(revenue) OVER (ORDER BY week_start), 2) AS next_week_revenue
FROM weekly
ORDER BY week_start;


/* -----------------------------------------
   14) Next-month revenue alignment
   Filename suggestion: tableau_next_month_revenue.csv
   ----------------------------------------- */
WITH monthly AS (
  SELECT
    strftime('%Y-%m', sale_date) AS year_month,
    SUM(money) AS revenue
  FROM v_coffee_sales
  GROUP BY year_month
)
SELECT
  year_month,
  ROUND(revenue, 2) AS revenue,
  ROUND(LEAD(revenue) OVER (ORDER BY year_month), 2) AS next_month_revenue
FROM monthly
ORDER BY year_month;

/* =========================
   15) SANITY CHECK
   ========================= */

SELECT
  COUNT(*)        AS total_rows,
  MIN(sale_date)  AS min_date,
  MAX(sale_date)  AS max_date,
  ROUND(SUM(amount), 2) AS total_revenue
FROM analytics_coffee_sales;


/* =========================
   16) EXPORT DATASET
   =========================
   Output path:
   data/processed/analytics_coffee_sales.csv
*/

.headers on
.mode csv
.output "data/processed/analytics_coffee_sales.csv"

SELECT
  sale_date,
  sale_ts,
  sale_hour,
  sale_day,
  sale_month,
  cash_type,
  coffee_name,
  customer_type,
  customer_id,
  amount,
  source_dataset
FROM analytics_coffee_sales
ORDER BY sale_date, sale_ts;

.output stdout