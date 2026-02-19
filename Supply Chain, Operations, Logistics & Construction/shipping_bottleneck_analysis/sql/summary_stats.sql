-- ANALYSING BOTTLENECKS BY CARRIER AND WEATHER
-- This CTE calculates aggregated stats to be used for the final report
WITH CarrierMetrics AS (
    SELECT 
        carrier_name,
        weather_condition,
        COUNT(order_id) as total_shipments,
        SUM(is_late) as late_count,
        AVG(days_diff) as avg_delay_days
    FROM v_shipping_performance
    GROUP BY carrier_name, weather_condition
)
SELECT 
    carrier_name,
    weather_condition,
    total_shipments,
    late_count,
    ROUND((late_count::DECIMAL / total_shipments) * 100, 2) as late_rate_percentage,
    ROUND(avg_delay_days, 1) as avg_days_overdue
FROM CarrierMetrics
WHERE total_shipments > 10 -- Filtering out low-volume noise
ORDER BY late_rate_percentage DESC;

-- RANKING PORTS BY RELIABILITY (Window Function)
-- Shows which ports are systemic bottlenecks regardless of carrier
SELECT 
    origin_port,
    COUNT(*) as volume,
    AVG(actual_days) as avg_transit_time,
    RANK() OVER (ORDER BY AVG(actual_days - scheduled_days) DESC) as bottleneck_rank
FROM v_shipping_performance
GROUP BY origin_port
HAVING COUNT(*) > 50;