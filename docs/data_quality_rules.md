# Data Quality Rules

## Raw Orders Validation

| Column | Rule | Tool |
|---|---|---|
| order_id | Not null | Great Expectations |
| order_id | Unique | Great Expectations |
| customer_id | Not null | Great Expectations |
| product_id | Not null | Great Expectations |
| quantity | Between 1 and 10 | Great Expectations |
| order_status | Must be completed, cancelled, returned, or pending | Great Expectations |

## dbt Model Tests

| Model | Column | Rule |
|---|---|---|
| stg_customers | customer_id | not_null, unique |
| stg_products | product_id | not_null, unique |
| stg_orders | order_id | not_null, unique |
| stg_orders | customer_id | not_null |
| stg_orders | product_id | not_null |
| fct_orders | order_id | not_null, unique |
| fct_orders | order_amount | not_null |

## Athena Validation Queries

| Check | Purpose |
|---|---|
| Row count | Confirm curated tables loaded |
| Null key count | Catch invalid primary keys |
| Revenue by status | Validate revenue aggregation |
| Daily revenue | Check reporting readiness |

## Production Improvements

- Add anomaly detection for revenue spikes
- Add freshness checks
- Add duplicate file detection
- Add schema drift alerts
- Add bad-record quarantine folder
- Add incremental processing by order date
