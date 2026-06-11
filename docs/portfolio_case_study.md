# Portfolio Case Study: AWS Cloud Lakehouse ELT Pipeline

## Problem

Business teams need clean and reliable e-commerce data for sales reporting, customer analysis, and product performance tracking. Raw files are not directly suitable for reporting because they may contain duplicates, inconsistent formats, missing values, or unvalidated business fields.

## Solution

I built an AWS cloud lakehouse ELT pipeline that converts raw e-commerce files into analytics-ready tables.

## Architecture

The pipeline uses:

- S3 for raw, curated, and analytics storage
- Glue Crawler for metadata discovery
- Glue PySpark for transformation
- Athena for SQL querying over S3
- dbt for staging and mart models
- Great Expectations for validation
- Airflow for orchestration
- Terraform for infrastructure
- CloudWatch for monitoring

## Implementation

The project starts by generating mock e-commerce data using Python. The raw files are validated locally and uploaded to S3. AWS Glue then catalogs the raw data and runs a PySpark transformation job that writes curated Parquet files back to S3. Athena queries the curated data, and dbt creates analytics-ready fact and dimension tables.

## Results

The final pipeline produces:

- Clean customer dimension
- Clean product dimension
- Order fact table with revenue metrics
- Validated raw and transformed data
- Queryable Athena tables
- Repeatable Terraform-based infrastructure
- Airflow-based orchestration pattern

## Skills Demonstrated

- AWS data lakehouse architecture
- Cloud storage design
- Batch data ingestion
- PySpark transformation
- Data cataloging
- SQL analytics
- dbt modeling
- Data quality validation
- Workflow orchestration
- Infrastructure as code
- Cloud monitoring
