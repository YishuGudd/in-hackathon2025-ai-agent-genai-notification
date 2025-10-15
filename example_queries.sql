-- Sample SQL queries for Snowflake data analytics

-- 1. Basic data exploration
SELECT * FROM your_table LIMIT 10;

-- 2. Count records
SELECT COUNT(*) as total_records FROM your_table;

-- 3. Aggregation by category
SELECT 
    category,
    COUNT(*) as count,
    AVG(value) as avg_value,
    MIN(value) as min_value,
    MAX(value) as max_value
FROM your_table
GROUP BY category
ORDER BY count DESC;

-- 4. Time-based analysis (last 30 days)
SELECT 
    DATE_TRUNC('day', timestamp_column) as date,
    COUNT(*) as daily_count,
    SUM(amount) as daily_total
FROM your_table
WHERE timestamp_column >= DATEADD(day, -30, CURRENT_DATE())
GROUP BY date
ORDER BY date;

-- 5. Join example
SELECT 
    a.*,
    b.additional_field
FROM table_a a
LEFT JOIN table_b b ON a.id = b.foreign_id
WHERE a.status = 'active';

-- 6. Window functions
SELECT 
    *,
    ROW_NUMBER() OVER (PARTITION BY category ORDER BY value DESC) as rank_in_category
FROM your_table;

-- 7. Get table information
SHOW TABLES;
DESCRIBE TABLE your_table;

-- 8. Check current context
SELECT 
    CURRENT_DATABASE() as database,
    CURRENT_SCHEMA() as schema,
    CURRENT_WAREHOUSE() as warehouse,
    CURRENT_ROLE() as role,
    CURRENT_USER() as user;

