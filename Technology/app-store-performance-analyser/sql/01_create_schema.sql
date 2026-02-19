-- 01_create_schema.sql
-- Target: DuckDB (also largely compatible with SQLite)
-- Purpose: Create the core apps table for Google-Playstore.csv

CREATE TABLE IF NOT EXISTS apps (
    app_id              TEXT,
    app_name            TEXT,
    category            TEXT,

    rating              DOUBLE,
    rating_count        BIGINT,

    installs            TEXT,
    min_installs        BIGINT,
    max_installs        BIGINT,

    free                BOOLEAN,
    price               DOUBLE,
    currency            TEXT,

    size                TEXT,
    min_android         TEXT,

    developer           TEXT,
    developer_id        TEXT,
    developer_email     TEXT,
    developer_website   TEXT,

    released            TEXT,
    privacy_policy      TEXT,
    last_updated        TEXT,

    content_rating      TEXT,

    ad_supported        BOOLEAN,
    in_app_purchases    BOOLEAN,
    editors_choice      BOOLEAN
);

-- Optional: Helpful indexes for SQLite (DuckDB ignores CREATE INDEX unless supported in newer versions)
-- CREATE INDEX IF NOT EXISTS idx_apps_category ON apps(category);
-- CREATE INDEX IF NOT EXISTS idx_apps_rating ON apps(rating);
-- CREATE INDEX IF NOT EXISTS idx_apps_min_installs ON apps(min_installs);
