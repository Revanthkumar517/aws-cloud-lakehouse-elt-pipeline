-- Row count validation
SELECT COUNT(*) AS orders_count
FROM ecommerce_lakehouse.curated_orders;

-- Null key validation
SELECT COUNT(*) AS invalid_order_keys
FROM ecommerce_lakehouse.curated_orders
WHERE order_id IS NULL;

-- Revenue validation
SELECT
    order_status,
    COUNT(*) AS order_count,
    SUM(order_amount) AS total_order_amount
FROM ecommerce_lakehouse.curated_orders
GROUP BY order_status
ORDER BY total_order_amount DESC;

-- Daily sales mart query
SELECT
    order_date,
    COUNT(*) AS total_orders,
    SUM(order_amount) AS total_revenue
FROM ecommerce_lakehouse.curated_orders
WHERE order_status = 'completed'
GROUP BY order_date
ORDER BY order_date;
