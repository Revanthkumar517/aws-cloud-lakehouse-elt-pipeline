select
    o.order_id,
    o.customer_id,
    o.product_id,
    o.order_date,
    o.quantity,
    o.order_status,
    o.unit_price,
    o.order_amount,
    c.state as customer_state,
    p.category as product_category,
    case
        when o.order_status = 'completed' then o.order_amount
        else 0
    end as completed_revenue
from {{ ref('stg_orders') }} o
left join {{ ref('dim_customers') }} c
    on o.customer_id = c.customer_id
left join {{ ref('dim_products') }} p
    on o.product_id = p.product_id
