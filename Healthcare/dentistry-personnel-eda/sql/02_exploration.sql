-- Row count
SELECT COUNT(*) FROM dentistry_personnel;

-- Column preview
SELECT *
FROM dentistry_personnel
LIMIT 10;

-- Check missing values
SELECT 
  COUNT(*) AS total_rows,
  SUM(CASE WHEN Value IS NULL THEN 1 ELSE 0 END) AS missing_values
FROM dentistry_personnel;

-- Distinct indicators
SELECT DISTINCT Indicator
FROM dentistry_personnel;