-- 05_update_frequency.sql
-- Purpose: Update frequency buckets vs rating and installs
-- DuckDB version (date parsing + datediff)

WITH filtered AS (
    SELECT
        app_id,
        app_name,
        category,
        rating,
        rating_count,
        min_installs,
        last_updated
    FROM apps
    WHERE last_updated IS NOT NULL
      AND rating IS NOT NULL
      AND rating BETWEEN 0 AND 5
      AND min_installs IS NOT NULL
      AND min_installs > 0
      AND rating_count IS NOT NULL
      AND rating_count >= 1000
),
dated AS (
    SELECT
        *,
        -- Snapshot reference date for the June 2021 scrape
        DATE '2021-06-30' AS snapshot_date,

        -- Parse last_updated to date (DuckDB is flexible with common date strings)
        TRY_CAST(last_updated AS DATE) AS last_updated_date
    FROM filtered
),
diffed AS (
    SELECT
        app_id,
        app_name,
        category,
        rating,
        rating_count,
        min_installs,
        snapshot_date,
        last_updated_date,
        CASE
            WHEN last_updated_date IS NULL THEN NULL
            ELSE datediff('day', last_updated_date, snapshot_date)
        END AS days_since_update
    FROM dated
),
bucketed AS (
    SELECT
        *,
        CASE
            WHEN days_since_update IS NULL THEN NULL
            WHEN days_since_update < 30 THEN '< 30 days'
            WHEN days_since_update < 90 THEN '30–90 days'
            WHEN days_since_update < 180 THEN '90–180 days'
            WHEN days_since_update < 365 THEN '180–365 days'
            WHEN days_since_update < 730 THEN '1–2 years'
            ELSE '2+ years'
        END AS update_bucket
    FROM diffed
    WHERE days_since_update IS NOT NULL
      AND days_since_update >= 0
)
SELECT
    update_bucket,
    COUNT(*) AS apps,
    AVG(days_since_update) AS avg_days_since_update,
    MEDIAN(days_since_update) AS median_days_since_update,
    AVG(rating) AS avg_rating,
    MEDIAN(rating) AS median_rating,
    MEDIAN(min_installs) AS median_installs,
    AVG(min_installs) AS mean_installs
FROM bucketed
GROUP BY update_bucket
ORDER BY
    CASE update_bucket
        WHEN '< 30 days' THEN 1
        WHEN '30–90 days' THEN 2
        WHEN '90–180 days' THEN 3
        WHEN '180–365 days' THEN 4
        WHEN '1–2 years' THEN 5
        WHEN '2+ years' THEN 6
        ELSE 99
    END;
