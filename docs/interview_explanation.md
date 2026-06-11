# Interview Explanation

## 30-Second Version

I built an AWS cloud lakehouse ELT pipeline for mock e-commerce data. The pipeline lands raw CSV files in S3, catalogs them with AWS Glue, transforms them with a Glue PySpark job into curated Parquet files, exposes the data through Athena, and builds analytics-ready models using dbt. I used Airflow for orchestration, Terraform for infrastructure, Great Expectations and dbt tests for data quality, IAM for secure access, and CloudWatch for monitoring.

## Step-by-Step Flow

1. I generated mock customer, product, and order datasets using Python.
2. I uploaded those raw files to Amazon S3 under a raw lakehouse zone.
3. I used AWS Glue Crawler to scan the S3 data and register metadata in the Glue Data Catalog.
4. I created a Glue PySpark job to read raw CSV files, clean and deduplicate records, join orders with product pricing, calculate order amount, and write curated Parquet files.
5. I partitioned the orders data by order status to improve query filtering.
6. I queried curated data using Athena external tables.
7. I created dbt staging and mart models for analytics tables.
8. I added Great Expectations and dbt tests for data validation.
9. I orchestrated the full workflow using Airflow.
10. I used Terraform to define AWS infrastructure as code.

## Why S3?

S3 is used as the lakehouse storage layer because it can store raw and curated data cheaply and works well with Glue, Athena, Redshift Spectrum, and other AWS analytics services.

## Why Glue?

Glue provides both metadata cataloging and serverless Spark-based transformation. In this project, Glue Crawler creates table metadata, and Glue Job transforms raw data into Parquet.

## Why Athena?

Athena allows SQL querying directly on S3 data without loading everything into a traditional database.

## Why dbt?

dbt is used for SQL-based transformations, modular models, testing, documentation, and analytics-ready marts.

## Why Great Expectations?

Great Expectations validates the data before it moves further into the pipeline. It checks key fields, uniqueness, accepted status values, and quantity ranges.

## Why Terraform?

Terraform makes the AWS setup repeatable. Instead of manually clicking through the AWS Console, infrastructure is declared as code.
