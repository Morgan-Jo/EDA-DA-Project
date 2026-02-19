-- 02_load_data.sql
-- DuckDB ingestion: load CSV directly into the apps table

-- Change this if your file path differs
-- Example: data/raw/Google-Playstore.csv
-- DuckDB supports header detection and type inference

INSERT INTO apps
SELECT
    app_id,
    app_name,
    category,

    TRY_CAST(rating AS DOUBLE) AS rating,
    TRY_CAST(rating_count AS BIGINT) AS rating_count,

    installs,
    TRY_CAST(min_installs AS BIGINT) AS min_installs,
    TRY_CAST(max_installs AS BIGINT) AS max_installs,

    -- "free" can be True/False, 1/0, or strings depending on dataset version
    CASE
        WHEN lower(CAST(free AS VARCHAR)) IN ('true','1','yes','y') THEN TRUE
        ELSE FALSE
    END AS free,

    TRY_CAST(price AS DOUBLE) AS price,
    currency,

    size,
    min_android,

    developer,
    developer_id,
    developer_email,
    developer_website,

    released,
    privacy_policy,
    last_updated,

    content_rating,

    CASE
        WHEN lower(CAST(ad_supported AS VARCHAR)) IN ('true','1','yes','y') THEN TRUE
        ELSE FALSE
    END AS ad_supported,

    CASE
        WHEN lower(CAST(in_app_purchases AS VARCHAR)) IN ('true','1','yes','y') THEN TRUE
        ELSE FALSE
    END AS in_app_purchases,

    CASE
        WHEN lower(CAST(editors_choice AS VARCHAR)) IN ('true','1','yes','y') THEN TRUE
        ELSE FALSE
    END AS editors_choice

FROM read_csv_auto(
    'data/raw/Google-Playstore.csv',
    header = true,
    ignore_errors = true
);
