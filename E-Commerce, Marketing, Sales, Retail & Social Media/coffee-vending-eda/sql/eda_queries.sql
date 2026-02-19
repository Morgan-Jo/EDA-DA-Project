/* ============================================================
   Coffee Vending Machine Sales — EDA Queries (SQL-First)
   File: eda_queries.sql
   Engine: SQLite (VS Code + SQLite extension friendly)

   Purpose:
   - Profile each source dataset separately (before joining)
   - Validate data quality
   - Produce descriptive statistics + EDA-ready tables
   - Then create a unified view for combined EDA

   Expected source tables:
   - coffee_sales_1(date, datetime, cash_type, card, money, coffee_name)
   - coffee_sales_2(date, datetime, cash_type, money, coffee_name)

   How to use:
   Run section-by-section in VS Code. Export result grids if needed.
   ============================================================ */


/* =========================
   A) DATASET 1: coffee_sales_1
   ========================= */

/* A1) Row count + date range */
SELECT
  'coffee_sales_1' AS dataset,
  COUNT(*)         AS rows,
  MIN(date(date))  AS min_date,
  MAX(date(date))  AS max_date
FROM coffee_sales_1;

/* A2) Schema check (SQLite) */
PRAGMA table_info(coffee_sales_1);

/* A3) Null / blank checks */
SELECT
  SUM(CASE WHEN date IS NULL OR TRIM(date) = '' THEN 1 ELSE 0 END)               AS null_date,
  SUM(CASE WHEN datetime IS NULL OR TRIM(datetime) = '' THEN 1 ELSE 0 END)       AS null_datetime,
  SUM(CASE WHEN cash_type IS NULL OR TRIM(cash_type) = '' THEN 1 ELSE 0 END)     AS null_cash_type,
  SUM(CASE WHEN card IS NULL OR TRIM(card) = '' THEN 1 ELSE 0 END)               AS null_card,
  SUM(CASE WHEN money IS NULL THEN 1 ELSE 0 END)                                 AS null_money,
  SUM(CASE WHEN coffee_name IS NULL OR TRIM(coffee_name) = '' THEN 1 ELSE 0 END) AS null_coffee_name
FROM coffee_sales_1;

/* A4) Duplicate transaction check (same timestamp + product + payment + amount + card) */
SELECT
  date(date) AS sale_date,
  datetime(datetime) AS sale_ts,
  cash_type,
  card,
  coffee_name,
  money,
  COUNT(*) AS dup_count
FROM coffee_sales_1
GROUP BY sale_date, sale_ts, cash_type, card, coffee_name, money
HAVING COUNT(*) > 1
ORDER BY dup_count DESC, sale_ts;

/* A5) Basic descriptive stats for money */
SELECT
  COUNT(*)                  AS transactions,
  ROUND(SUM(money), 2)      AS revenue,
  ROUND(AVG(money), 2)      AS avg_ticket,
  ROUND(MIN(money), 2)      AS min_ticket,
  ROUND(MAX(money), 2)      AS max_ticket
FROM coffee_sales_1;

/* A6) Price points distribution */
SELECT
  money,
  COUNT(*) AS purchases
FROM coffee_sales_1
GROUP BY money
ORDER BY purchases DESC, money;

/* A7) Payment type split */
SELECT
  cash_type,
  COUNT(*)                 AS transactions,
  ROUND(SUM(money), 2)     AS revenue,
  ROUND(AVG(money), 2)     AS avg_ticket
FROM coffee_sales_1
GROUP BY cash_type
ORDER BY revenue DESC;

/* A8) Product popularity */
SELECT
  coffee_name,
  COUNT(*)                 AS purchases,
  ROUND(SUM(money), 2)     AS revenue,
  ROUND(AVG(money), 2)     AS avg_price
FROM coffee_sales_1
GROUP BY coffee_name
ORDER BY purchases DESC;

/* A9) Daily trend */
SELECT
  date(date)               AS sale_date,
  COUNT(*)                 AS transactions,
  ROUND(SUM(money), 2)     AS revenue,
  ROUND(AVG(money), 2)     AS avg_ticket
FROM coffee_sales_1
GROUP BY sale_date
ORDER BY sale_date;

/* A10) Hour-of-day trend */
SELECT
  CAST(strftime('%H', datetime(datetime)) AS INTEGER) AS hour,
  COUNT(*)                 AS transactions,
  ROUND(SUM(money), 2)     AS revenue
FROM coffee_sales_1
GROUP BY hour
ORDER BY hour;

/* A11) Day-of-week trend */
SELECT
  CAST(strftime('%w', date(date)) AS INTEGER) AS dow_num,
  CASE CAST(strftime('%w', date(date)) AS INTEGER)
    WHEN 0 THEN 'Sun'
    WHEN 1 THEN 'Mon'
    WHEN 2 THEN 'Tue'
    WHEN 3 THEN 'Wed'
    WHEN 4 THEN 'Thu'
    WHEN 5 THEN 'Fri'
    WHEN 6 THEN 'Sat'
  END AS dow,
  COUNT(*)                 AS transactions,
  ROUND(SUM(money), 2)     AS revenue
FROM coffee_sales_1
GROUP BY dow_num, dow
ORDER BY dow_num;

/* A12) Customer (card) coverage + top customers */
SELECT
  COUNT(DISTINCT card) AS distinct_customers,
  SUM(CASE WHEN card IS NULL OR TRIM(card) = '' THEN 1 ELSE 0 END) AS missing_card_rows
FROM coffee_sales_1;

SELECT
  card AS customer_id,
  COUNT(*)                 AS purchases,
  ROUND(SUM(money), 2)     AS revenue,
  ROUND(AVG(money), 2)     AS avg_ticket,
  MIN(date(date))          AS first_purchase,
  MAX(date(date))          AS last_purchase
FROM coffee_sales_1
WHERE card IS NOT NULL AND TRIM(card) <> ''
GROUP BY card
ORDER BY revenue DESC
LIMIT 25;


/* =========================
   B) DATASET 2: coffee_sales_2
   ========================= */

/* B1) Row count + date range */
SELECT
  'coffee_sales_2' AS dataset,
  COUNT(*)         AS rows,
  MIN(date(date))  AS min_date,
  MAX(date(date))  AS max_date
FROM coffee_sales_2;

/* B2) Schema check (SQLite) */
PRAGMA table_info(coffee_sales_2);

/* B3) Null / blank checks */
SELECT
  SUM(CASE WHEN date IS NULL OR TRIM(date) = '' THEN 1 ELSE 0 END)               AS null_date,
  SUM(CASE WHEN datetime IS NULL OR TRIM(datetime) = '' THEN 1 ELSE 0 END)       AS null_datetime,
  SUM(CASE WHEN cash_type IS NULL OR TRIM(cash_type) = '' THEN 1 ELSE 0 END)     AS null_cash_type,
  SUM(CASE WHEN money IS NULL THEN 1 ELSE 0 END)                                 AS null_money,
  SUM(CASE WHEN coffee_name IS NULL OR TRIM(coffee_name) = '' THEN 1 ELSE 0 END) AS null_coffee_name
FROM coffee_sales_2;

/* B4) Duplicate transaction check */
SELECT
  date(date) AS sale_date,
  datetime(datetime) AS sale_ts,
  cash_type,
  coffee_name,
  money,
  COUNT(*) AS dup_count
FROM coffee_sales_2
GROUP BY sale_date, sale_ts, cash_type, coffee_name, money
HAVING COUNT(*) > 1
ORDER BY dup_count DESC, sale_ts;

/* B5) Basic descriptive stats for money */
SELECT
  COUNT(*)                  AS transactions,
  ROUND(SUM(money), 2)      AS revenue,
  ROUND(AVG(money), 2)      AS avg_ticket,
  ROUND(MIN(money), 2)      AS min_ticket,
  ROUND(MAX(money), 2)      AS max_ticket
FROM coffee_sales_2;

/* B6) Price points distribution */
SELECT
  money,
  COUNT(*) AS purchases
FROM coffee_sales_2
GROUP BY money
ORDER BY purchases DESC, money;

/* B7) Payment type split */
SELECT
  cash_type,
  COUNT(*)                 AS transactions,
  ROUND(SUM(money), 2)     AS revenue,
  ROUND(AVG(money), 2)     AS avg_ticket
FROM coffee_sales_2
GROUP BY cash_type
ORDER BY revenue DESC;

/* B8) Product popularity */
SELECT
  coffee_name,
  COUNT(*)                 AS purchases,
  ROUND(SUM(money), 2)     AS revenue,
  ROUND(AVG(money), 2)     AS avg_price
FROM coffee_sales_2
GROUP BY coffee_name
ORDER BY purchases DESC;

/* B9) Daily trend */
SELECT
  date(date)               AS sale_date,
  COUNT(*)                 AS transactions,
  ROUND(SUM(money), 2)     AS revenue,
  ROUND(AVG(money), 2)     AS avg_ticket
FROM coffee_sales_2
GROUP BY sale_date
ORDER BY sale_date;

/* B10) Hour-of-day trend */
SELECT
  CAST(strftime('%H', datetime(datetime)) AS INTEGER) AS hour,
  COUNT(*)                 AS transactions,
  ROUND(SUM(money), 2)     AS revenue
FROM coffee_sales_2
GROUP BY hour
ORDER BY hour;

/* B11) Day-of-week trend */
SELECT
  CAST(strftime('%w', date(date)) AS INTEGER) AS dow_num,
  CASE CAST(strftime('%w', date(date)) AS INTEGER)
    WHEN 0 THEN 'Sun'
    WHEN 1 THEN 'Mon'
    WHEN 2 THEN 'Tue'
    WHEN 3 THEN 'Wed'
    WHEN 4 THEN 'Thu'
    WHEN 5 THEN 'Fri'
    WHEN 6 THEN 'Sat'
  END AS dow,
  COUNT(*)                 AS transactions,
  ROUND(SUM(money), 2)     AS revenue
FROM coffee_sales_2
GROUP BY dow_num, dow
ORDER BY dow_num;


/* =========================
   C) CONSISTENCY CHECKS (before combining)
   ========================= */

/* C1) Compare coffee_name values between datasets */
SELECT
  coffee_name,
  'in_sales_1' AS present_in
FROM coffee_sales_1
GROUP BY coffee_name
UNION ALL
SELECT
  coffee_name,
  'in_sales_2' AS present_in
FROM coffee_sales_2
GROUP BY coffee_name
ORDER BY coffee_name, present_in;

/* C2) Compare price points by product between datasets */
SELECT
  coffee_name,
  'coffee_sales_1' AS dataset,
  ROUND(MIN(money), 2) AS min_price,
  ROUND(MAX(money), 2) AS max_price,
  COUNT(*) AS purchases
FROM coffee_sales_1
GROUP BY coffee_name

UNION ALL

SELECT
  coffee_name,
  'coffee_sales_2' AS dataset,
  ROUND(MIN(money), 2) AS min_price,
  ROUND(MAX(money), 2) AS max_price,
  COUNT(*) AS purchases
FROM coffee_sales_2
GROUP BY coffee_name
ORDER BY coffee_name, dataset;


/* =========================
   D) UNIFIED VIEW (combined EDA)
   ========================= */

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


/* D1) Combined row count + date range */
SELECT
  'v_coffee_sales' AS dataset,
  COUNT(*)         AS rows,
  MIN(sale_date)   AS min_date,
  MAX(sale_date)   AS max_date
FROM v_coffee_sales;

/* D2) Combined descriptive stats */
SELECT
  COUNT(*)                  AS transactions,
  ROUND(SUM(money), 2)      AS revenue,
  ROUND(AVG(money), 2)      AS avg_ticket,
  ROUND(MIN(money), 2)      AS min_ticket,
  ROUND(MAX(money), 2)      AS max_ticket
FROM v_coffee_sales;

/* D3) Combined daily revenue */
SELECT
  sale_date,
  COUNT(*)                 AS transactions,
  ROUND(SUM(money), 2)     AS revenue,
  ROUND(AVG(money), 2)     AS avg_ticket
FROM v_coffee_sales
GROUP BY sale_date
ORDER BY sale_date;

/* D4) Combined product leaderboard */
SELECT
  coffee_name,
  COUNT(*)                 AS purchases,
  ROUND(SUM(money), 2)     AS revenue,
  ROUND(AVG(money), 2)     AS avg_price
FROM v_coffee_sales
GROUP BY coffee_name
ORDER BY revenue DESC, purchases DESC;

/* D5) Combined payment split */
SELECT
  cash_type,
  COUNT(*)                 AS transactions,
  ROUND(SUM(money), 2)     AS revenue,
  ROUND(AVG(money), 2)     AS avg_ticket
FROM v_coffee_sales
GROUP BY cash_type
ORDER BY revenue DESC;

/* D6) Combined time-of-day + day-of-week heatmap export */
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

/* D7) Card customers only: repeat behaviour baseline */
SELECT
  customer_id,
  COUNT(*)                 AS purchases,
  ROUND(SUM(money), 2)     AS revenue,
  ROUND(AVG(money), 2)     AS avg_ticket,
  MIN(sale_date)           AS first_purchase,
  MAX(sale_date)           AS last_purchase
FROM v_coffee_sales
WHERE customer_id IS NOT NULL AND TRIM(customer_id) <> ''
GROUP BY customer_id
ORDER BY purchases DESC, revenue DESC;
