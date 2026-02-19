-- 1. Create Schema and Table
CREATE TABLE IF NOT EXISTS shipping_data (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_status VARCHAR(50),
    shipping_mode VARCHAR(50),
    scheduled_days INT,
    actual_days INT,
    origin_port VARCHAR(100),
    carrier_name VARCHAR(100),
    weather_condition VARCHAR(50), -- e.g., Clear, Rain, Storm
    order_date DATE,
    shipping_date DATE
);

-- 2. Data Cleaning: Handling Nulls and Negative Values
-- Senior-level touch: Ensure 'actual_days' cannot be less than zero
DELETE FROM shipping_data 
WHERE actual_days < 0 OR scheduled_days < 0;

-- 3. Feature Engineering: Create a view for easy EDA
-- This avoids modifying raw data while providing a "Late Flag"
CREATE OR REPLACE VIEW v_shipping_performance AS
SELECT 
    *,
    (actual_days - scheduled_days) AS days_diff,
    CASE 
        WHEN actual_days > scheduled_days THEN 1 
        ELSE 0 
    END AS is_late,
    CASE
        WHEN actual_days > (scheduled_days + 5) THEN 'Critical Delay'
        WHEN actual_days > scheduled_days THEN 'Minor Delay'
        ELSE 'On-Time/Early'
    END AS delay_category
FROM shipping_data;