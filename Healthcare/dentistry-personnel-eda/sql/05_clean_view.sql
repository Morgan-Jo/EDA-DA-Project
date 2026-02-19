DROP TABLE IF EXISTS dentistry_clean;

CREATE TABLE dentistry_clean AS
SELECT
    ParentLocation AS Region,
    Location       AS Country,
    Period         AS Year,
    Value          AS Dentists_Per_10000
FROM dentistry_personnel
WHERE Indicator = 'Dentists (per 10,000)'
  AND Value IS NOT NULL;
