-- Replace bucket name before running.
-- Database should match Terraform variable athena_database.

CREATE DATABASE IF NOT EXISTS ecommerce_lakehouse;

CREATE EXTERNAL TABLE IF NOT EXISTS ecommerce_lakehouse.curated_customers (
    customer_id int,
    first_name string,
    last_name string,
    email string,
    state string,
    signup_date date,
    ingestion_timestamp timestamp
)
STORED AS PARQUET
LOCATION 's3://replace-with-your-bucket/curated/ecommerce/customers/';

CREATE EXTERNAL TABLE IF NOT EXISTS ecommerce_lakehouse.curated_products (
    product_id int,
    product_name string,
    category string,
    unit_price double,
    ingestion_timestamp timestamp
)
STORED AS PARQUET
LOCATION 's3://replace-with-your-bucket/curated/ecommerce/products/';

CREATE EXTERNAL TABLE IF NOT EXISTS ecommerce_lakehouse.curated_orders (
    order_id int,
    customer_id int,
    product_id int,
    order_date date,
    quantity int,
    unit_price double,
    order_amount double,
    ingestion_timestamp timestamp
)
PARTITIONED BY (order_status string)
STORED AS PARQUET
LOCATION 's3://replace-with-your-bucket/curated/ecommerce/orders/';

MSCK REPAIR TABLE ecommerce_lakehouse.curated_orders;
