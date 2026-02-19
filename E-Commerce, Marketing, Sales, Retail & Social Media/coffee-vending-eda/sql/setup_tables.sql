/* ============================================================
   Coffee Vending Machine Sales — Setup & Import
   File: setup_tables.sql
   Engine: SQLite (CLI)

   What this file does:
   1) Drops existing raw tables
   2) Recreates tables with correct schema
   3) Imports index_1.csv and index_2.csv
   4) Verifies row counts

   IMPORTANT:
   - Run this file from the PROJECT ROOT
   - SQLite CLI required (.import is CLI-only)
   ============================================================ */


/* =========================
   1) DROP TABLES IF EXIST
   ========================= */

DROP TABLE IF EXISTS coffee_sales_1;
DROP TABLE IF EXISTS coffee_sales_2;


/* =========================
   2) CREATE TABLES
   ========================= */

CREATE TABLE coffee_sales_1 (
  date        TEXT NOT NULL,
  datetime    TEXT NOT NULL,
  cash_type   TEXT NOT NULL,
  card        TEXT,
  money       REAL NOT NULL,
  coffee_name TEXT NOT NULL
);

CREATE TABLE coffee_sales_2 (
  date        TEXT NOT NULL,
  datetime    TEXT NOT NULL,
  cash_type   TEXT NOT NULL,
  money       REAL NOT NULL,
  coffee_name TEXT NOT NULL
);


/* =========================
   3) IMPORT CSV FILES
   =========================
   Assumes files exist in:
   data/raw/index_1.csv
   data/raw/index_2.csv
*/

.mode csv
.headers on

.import "data/raw/index_1.csv" coffee_sales_1
.import "data/raw/index_2.csv" coffee_sales_2


/* =========================
   4) LOAD VALIDATION
   ========================= */

SELECT 'coffee_sales_1' AS table_name, COUNT(*) AS rows FROM coffee_sales_1;
SELECT 'coffee_sales_2' AS table_name, COUNT(*) AS rows FROM coffee_sales_2;


/* =========================
   5) SCHEMA VALIDATION
   ========================= */

PRAGMA table_info(coffee_sales_1);
PRAGMA table_info(coffee_sales_2);
/* =========================
   END OF FILE
   ========================= */
