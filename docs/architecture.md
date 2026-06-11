# Architecture Explanation

## Why this is a Lakehouse

This project uses S3 as the storage foundation and keeps data in multiple lakehouse zones:

- Raw zone: original landing data
- Curated zone: cleaned, typed, partitioned Parquet data
- Analytics zone: modeled business tables

The design combines data lake flexibility with warehouse-style SQL access through Athena and optional Redshift Spectrum.

## Why ELT instead of ETL

The pipeline first lands raw data into S3, then transforms it after loading into the cloud storage layer. This is ELT behavior:

1. Extract from source files
2. Load into raw S3
3. Transform using Glue/dbt
4. Serve through Athena/Redshift

## Data Quality

Data quality checks are applied before and after transformation:

- Required field checks
- Primary key uniqueness
- Valid order status values
- Quantity range checks
- Null key validation
- Revenue aggregation validation

## Monitoring

CloudWatch captures Glue job logs and metrics. Airflow tracks task success/failure and controls retries.

## Security

IAM roles are used for Glue and S3 access. S3 encryption and versioning are enabled through Terraform.
