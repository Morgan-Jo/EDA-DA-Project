-- 03_category_rankings.sql
-- Purpose: Rank top apps per category by rating, then min_installs
-- Works in DuckDB and SQLite (window functions supported in modern SQLite)

WITH filtered AS (
    SELECT
        app_id,
        app_name,
        category,
        rating,
        rating_count,
        min_installs,
        free,
        price
    FROM apps
    WHERE category IS NOT NULL
      AND rating IS NOT NULL
      AND rating BETWEEN 0 AND 5
      AND min_installs IS NOT NULL
      AND min_installs > 0
      AND rating_count IS NOT NULL
      AND rating_count >= 1000
),
ranked_apps AS (
    SELECT
        app_id,
        app_name,
        category,
        rating,
        rating_count,
        min_installs,
        free,
        price,
        ROW_NUMBER() OVER (
            PARTITION BY category
            ORDER BY rating DESC, min_installs DESC, rating_count DESC
        ) AS rank_in_category
    FROM filtered
),
top_10_per_category AS (
    SELECT *
    FROM ranked_apps
    WHERE rank_in_category <= 10
)
SELECT *
FROM top_10_per_category
ORDER BY category, rank_in_category;
