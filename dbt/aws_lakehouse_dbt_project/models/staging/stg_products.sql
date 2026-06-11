select
    cast(product_id as integer) as product_id,
    product_name,
    category,
    cast(unit_price as double) as unit_price,
    ingestion_timestamp
from {{ source('ecommerce_lakehouse', 'curated_products') }}
where product_id is not null
