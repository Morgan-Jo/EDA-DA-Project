-- Average dentists per 10,000 by region
SELECT 
  ParentLocation AS region,
  ROUND(AVG(Value), 2) AS avg_dentists
FROM dentistry_personnel
WHERE Indicator = 'Dentists (per 10,000)'
  AND Value IS NOT NULL
GROUP BY ParentLocation
ORDER BY avg_dentists DESC;

-- Top 10 countries
SELECT 
  Location,
  Value
FROM dentistry_personnel
WHERE Indicator = 'Dentists (per 10,000)'
ORDER BY Value DESC
LIMIT 10;

-- Bottom 10 countries (excluding zeros)
SELECT 
  Location,
  Value
FROM dentistry_personnel
WHERE Indicator = 'Dentists (per 10,000)'
  AND Value > 0
ORDER BY Value ASC
LIMIT 10;