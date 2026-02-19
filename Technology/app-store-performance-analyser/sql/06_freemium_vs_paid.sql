-- 06_freemium_vs_paid.sql
-- Purpose: Freemium vs paid model comparison

WITH filtered AS (
    SELECT
        app_id,
        app_name,
        category,
        rating,
        rating_count,
        min_installs,
        free,
        price,
        ad_supported,
        in_app_purchases
    FROM apps
    WHERE rating IS NOT NULL
      AND rating BETWEEN 0 AND 5
      AND min_installs IS NOT NULL
      AND min_installs > 0
      AND rating_count IS NOT NULL
      AND rating_count >= 1000
),
typed AS (
    SELECT
        *,
        CASE
            WHEN free = FALSE THEN 'Paid'
            WHEN free = TRUE AND in_app_purchases = TRUE THEN 'IAP Freemium'
            WHEN free = TRUE AND ad_supported = TRUE AND (in_app_purchases = FALSE OR in_app_purchases IS NULL) THEN 'Ad-Supported'
            WHEN free = TRUE THEN 'Pure Free'
            ELSE 'Unknown'
        END AS monetisation_type
    FROM filtered
)
SELECT
    monetisation_type,
    COUNT(*) AS apps,
    AVG(rating) AS avg_rating,
    MEDIAN(rating) AS median_rating,
    MEDIAN(min_installs) AS median_installs,
    AVG(min_installs) AS mean_installs,
    COUNT(*) * 1.0 / (SELECT COUNT(*) FROM typed) AS share_of_apps
FROM typed
GROUP BY monetisation_type
ORDER BY
    CASE monetisation_type
        WHEN 'Pure Free' THEN 1
        WHEN 'Ad-Supported' THEN 2
        WHEN 'IAP Freemium' THEN 3
        WHEN 'Paid' THEN 4
        ELSE 99
    END;

-- Category breakdown for Tableau (heatmap / bars)

WITH filtered AS (
    SELECT
        category,
        rating,
        rating_count,
        min_installs,
        free,
        ad_supported,
        in_app_purchases
    FROM apps
    WHERE category IS NOT NULL
      AND rating IS NOT NULL
      AND rating BETWEEN 0 AND 5
      AND min_installs IS NOT NULL
      AND min_installs > 0
      AND rating_count IS NOT NULL
      AND rating_count >= 1000
),
typed AS (
    SELECT
        *,
        CASE
            WHEN free = FALSE THEN 'Paid'
            WHEN free = TRUE AND in_app_purchases = TRUE THEN 'IAP Freemium'
            WHEN free = TRUE AND ad_supported = TRUE AND (in_app_purchases = FALSE OR in_app_purchases IS NULL) THEN 'Ad-Supported'
            WHEN free = TRUE THEN 'Pure Free'
            ELSE 'Unknown'
        END AS monetisation_type
    FROM filtered
)
SELECT
    category,
    monetisation_type,
    COUNT(*) AS apps,
    AVG(rating) AS avg_rating,
    MEDIAN(rating) AS median_rating,
    MEDIAN(min_installs) AS median_installs,
    AVG(min_installs) AS mean_installs
FROM typed
GROUP BY category, monetisation_type
HAVING COUNT(*) >= 200
ORDER BY category, monetisation_type;
