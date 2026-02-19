WITH stats AS (
  SELECT
    AVG(Value) AS mean_value,
    SQRT(AVG(Value * Value) - AVG(Value) * AVG(Value)) AS std_dev
  FROM dentistry_personnel
  WHERE Indicator = 'Dentists (per 10,000)'
    AND Value IS NOT NULL
),

scored AS (
  SELECT
    d.Location,
    d.Value,
    (d.Value - s.mean_value) / s.std_dev AS z_score
  FROM dentistry_personnel d
  CROSS JOIN stats s
  WHERE d.Indicator = 'Dentists (per 10,000)'
    AND d.Value IS NOT NULL
)

SELECT *
FROM scored
WHERE ABS(z_score) > 3
ORDER BY z_score DESC;