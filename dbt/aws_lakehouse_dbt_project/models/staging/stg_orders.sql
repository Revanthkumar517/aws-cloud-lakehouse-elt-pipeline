select
    cast(order_id as integer) as order_id,
    cast(customer_id as integer) as customer_id,
    cast(product_id as integer) as product_id,
    cast(order_date as date) as order_date,
    cast(quantity as integer) as quantity,
    order_status,
    cast(unit_price as double) as unit_price,
    cast(order_amount as double) as order_amount,
    ingestion_timestamp
from {{ source('ecommerce_lakehouse', 'curated_orders') }}
where order_id is not null
