select
    customer_id,
    first_name,
    last_name,
    email,
    state,
    signup_date
from {{ ref('stg_customers') }}
