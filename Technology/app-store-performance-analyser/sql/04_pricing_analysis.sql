-- 04_pricing_analysis.sql
-- Purpose: Pricing strategy by price tier and category
-- Notes:
-- - Revenue proxy is NOT real revenue: price * min_installs for paid apps
-- - Filters to reduce noise: min_installs > 0 and rating_count >= 1000

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
        currency
    FROM apps
    WHERE price IS NOT NULL
      AND min_installs IS NOT NULL
      AND min_installs > 0
      AND rating IS NOT NULL
      AND rating BETWEEN 0 AND 5
      AND rating_count IS NOT NULL
      AND rating_count >= 1000
),
tiered AS (
    SELECT
        *,
        CASE
            WHEN price = 0 THEN 'Free'
            WHEN price > 0 AND price <= 0.99 THEN '0.01–0.99'
            WHEN price > 0.99 AND price <= 1.99 THEN '1.00–1.99'
            WHEN price > 1.99 AND price <= 2.99 THEN '2.00–2.99'
            WHEN price > 2.99 AND price <= 4.99 THEN '3.00–4.99'
            WHEN price > 4.99 AND price <= 9.99 THEN '5.00–9.99'
            WHEN price > 9.99 AND price <= 19.99 THEN '10.00–19.99'
            WHEN price > 19.99 AND price <= 49.99 THEN '20.00–49.99'
            ELSE '50+'
        END AS price_tier,
        CASE
            WHEN price > 0 THEN price * min_installs
            ELSE 0
        END AS revenue_proxy
    FROM filtered
),
paid_only AS (
    SELECT *
    FROM tiered
    WHERE price > 0
)
SELECT
    price_tier,
    COUNT(*) AS apps,
    MEDIAN(price) AS median_price,
    MEDIAN(min_installs) AS median_installs,
    AVG(min_installs) AS mean_installs,
    MEDIAN(revenue_proxy) AS median_revenue_proxy,
    AVG(revenue_proxy) AS mean_revenue_proxy,
    AVG(rating) AS avg_rating
FROM paid_only
GROUP BY price_tier
ORDER BY
    CASE price_tier
        WHEN '0.01–0.99' THEN 1
        WHEN '1.00–1.99' THEN 2
        WHEN '2.00–2.99' THEN 3
        WHEN '3.00–4.99' THEN 4
        WHEN '5.00–9.99' THEN 5
        WHEN '10.00–19.99' THEN 6
        WHEN '20.00–49.99' THEN 7
        WHEN '50+' THEN 8
        ELSE 99
    END;

-- Category x price tier matrix for Tableau heatmap

WITH filtered AS (
    SELECT
        category,
        rating,
        rating_count,
        min_installs,
        price
    FROM apps
    WHERE category IS NOT NULL
      AND price IS NOT NULL
      AND price > 0
      AND min_installs IS NOT NULL
      AND min_installs > 0
      AND rating IS NOT NULL
      AND rating BETWEEN 0 AND 5
      AND rating_count IS NOT NULL
      AND rating_count >= 1000
),
tiered AS (
    SELECT
        category,
        min_installs,
        rating,
        price,
        CASE
            WHEN price <= 0.99 THEN '0.01–0.99'
            WHEN price <= 1.99 THEN '1.00–1.99'
            WHEN price <= 2.99 THEN '2.00–2.99'
            WHEN price <= 4.99 THEN '3.00–4.99'
            WHEN price <= 9.99 THEN '5.00–9.99'
            WHEN price <= 19.99 THEN '10.00–19.99'
            WHEN price <= 49.99 THEN '20.00–49.99'
            ELSE '50+'
        END AS price_tier,
        price * min_installs AS revenue_proxy
    FROM filtered
)
SELECT
    category,
    price_tier,
    COUNT(*) AS apps,
    MEDIAN(min_installs) AS median_installs,
    AVG(min_installs) AS mean_installs,
    AVG(rating) AS avg_rating,
    MEDIAN(revenue_proxy) AS median_revenue_proxy
FROM tiered
GROUP BY category, price_tier
HAVING COUNT(*) >= 50
ORDER BY category, price_tier;
