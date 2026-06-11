# Demo Script for Recruiter or Interview

## 30-Second Pitch

I built an AWS cloud lakehouse ELT pipeline for mock e-commerce data. The pipeline ingests raw CSV files into Amazon S3, catalogs them with AWS Glue, transforms them with a Glue PySpark job into curated Parquet, queries them through Athena and Redshift Spectrum, and creates analytics-ready tables using dbt. I also added Great Expectations and dbt tests for data quality, Airflow for orchestration, Terraform for infrastructure, IAM for secure access, and CloudWatch for monitoring.

## 2-Minute Walkthrough

First, I generated mock customer, product, and order data using Python. I stored the raw files locally and validated them using Great Expectations before loading them into AWS.

Then I uploaded those files into an S3 raw zone using a boto3 ingestion script. After the files landed in S3, I used an AWS Glue crawler to scan the raw files and register metadata in the Glue Data Catalog.

Next, I created a Glue PySpark job that reads the raw CSV data, removes duplicates, standardizes data types, joins orders with product pricing, calculates order amount, and writes the output as Parquet into the curated S3 zone. I partitioned the orders dataset by order status to improve query filtering.

After that, I queried the curated data using Athena. I also created dbt staging and mart models, including `dim_customers`, `dim_products`, and `fct_orders`, so the data is ready for analytics and reporting.

For quality checks, I used Great Expectations before ingestion and dbt tests after modeling. I also added Athena validation queries to verify row counts, null keys, and revenue totals.

Finally, I used Terraform to define the AWS infrastructure and Airflow to orchestrate the pipeline steps. CloudWatch captures Glue job logs so failures can be traced and debugged.

## 5-Minute Technical Walkthrough

### 1. Storage Design

I used S3 as the main lakehouse storage layer with separate raw, curated, and analytics zones. Raw stores original CSV files. Curated stores cleaned Parquet files. Analytics stores dbt-modeled tables.

### 2. Catalog Design

I used AWS Glue Data Catalog so that S3 files can be queried as structured tables from Athena and Redshift Spectrum.

### 3. Processing Design

I used AWS Glue PySpark because it is serverless and suitable for scalable batch transformation. The transformation job joins orders with product pricing and calculates order-level revenue.

### 4. Query Layer

I used Athena to query curated Parquet directly from S3. This avoids loading everything into a traditional database and fits the lakehouse approach.

### 5. Modeling Layer

I used dbt to separate staging models from marts. Staging models clean and standardize fields. Mart models create business-friendly tables like dimensions and facts.

### 6. Quality Layer

I used Great Expectations for raw data checks and dbt tests for transformed models. This catches bad data before it reaches analytics.

### 7. Orchestration

I designed an Airflow DAG that runs generation, validation, ingestion, Glue crawler, Glue transformation, dbt execution, and Athena validation in order.

### 8. Infrastructure

I used Terraform to provision the S3 bucket, Glue database, Glue crawler, Glue job, IAM role, CloudWatch logs, and Athena workgroup.

## Simple Interview Answer

The main thing I learned is how different AWS services work together in a real data pipeline. S3 is not just storage; it becomes the lakehouse layer. Glue handles metadata and Spark transformation. Athena provides SQL access. dbt creates clean analytics models. Airflow controls the pipeline. Terraform makes the setup repeatable. Data quality checks make sure the pipeline is not just moving bad data faster.
