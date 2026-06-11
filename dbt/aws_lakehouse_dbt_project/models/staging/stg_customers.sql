select
    cast(customer_id as integer) as customer_id,
    first_name,
    last_name,
    email,
    state,
    cast(signup_date as date) as signup_date,
    ingestion_timestamp
from {{ source('ecommerce_lakehouse', 'curated_customers') }}
where customer_id is not null
