# AWS Cloud Lakehouse ELT Pipeline

A recruiter-facing AWS data engineering portfolio project that demonstrates a realistic **cloud lakehouse ELT pipeline** using Amazon S3, AWS Glue, Athena, Redshift Spectrum, Airflow, dbt, Terraform, Great Expectations, IAM, and CloudWatch.

This project is intentionally designed to match entry-level and associate data engineer job descriptions without pretending to be a Fortune 50 production platform. Because apparently honesty is now a differentiator.

---

## 1. Project Summary

This project builds an end-to-end AWS lakehouse pipeline for mock e-commerce data.

The pipeline ingests raw CSV files, stores them in Amazon S3, catalogs metadata using AWS Glue, transforms raw data into curated Parquet using AWS Glue PySpark, exposes curated datasets through Athena, creates analytics-ready marts using dbt, validates data quality using Great Expectations and dbt tests, and monitors execution through CloudWatch and Airflow logs.

---

## 2. Architecture

```text
Mock E-Commerce Source Data
        |
        v
Python Data Generator
        |
        v
Local Raw CSV Files
        |
        v
Python boto3 Upload Script
        |
        v
Amazon S3 Raw Zone
        |
        v
AWS Glue Crawler
        |
        v
AWS Glue Data Catalog
        |
        v
AWS Glue PySpark Transformation Job
        |
        v
Amazon S3 Curated Zone, Parquet
        |
        +------------------+
        |                  |
        v                  v
Amazon Athena        Redshift Spectrum
        |
        v
dbt Staging + Mart Models
        |
        v
Analytics Tables:
- dim_customers
- dim_products
- fct_orders
        |
        v
Validation + Monitoring:
- Great Expectations
- dbt tests
- Athena validation SQL
- CloudWatch logs
- Airflow DAG status
```

A Mermaid version is available here:

```text
docs/architecture_diagram.mmd
```

---

## 3. Business Problem

E-commerce teams need clean, reliable, analytics-ready data for revenue reporting, product performance analysis, and customer segmentation.

Raw order data usually arrives as files from multiple systems. This project simulates that workflow and creates a lakehouse pipeline that converts raw operational files into structured analytical datasets.

---

## 4. Dataset

The project uses mock e-commerce data generated with Python.

### Source Files

| File | Description |
|---|---|
| `customers.csv` | Customer profile and signup data |
| `products.csv` | Product catalog and pricing |
| `orders.csv` | Transaction-level order records |

### Key Fields

| Dataset | Important Fields |
|---|---|
| Customers | customer_id, name, email, state, signup_date |
| Products | product_id, product_name, category, unit_price |
| Orders | order_id, customer_id, product_id, order_date, quantity, order_status |

---

## 5. Lakehouse Zones

| Zone | S3 Path | Purpose |
|---|---|---|
| Raw | `s3://bucket/raw/ecommerce/` | Stores original ingested CSV files |
| Curated | `s3://bucket/curated/ecommerce/` | Stores cleaned and typed Parquet data |
| Analytics | `s3://bucket/analytics/ecommerce/` | Stores dbt-modeled reporting tables |
| Athena Results | `s3://bucket/athena-results/` | Stores Athena query output |

---

## 6. Technology Stack

| Category | Tools |
|---|---|
| Cloud | AWS S3, Glue, Athena, Redshift Spectrum, IAM, CloudWatch, Lambda |
| Processing | AWS Glue PySpark |
| Orchestration | Apache Airflow / Amazon MWAA pattern |
| Transformation | dbt |
| Quality | Great Expectations, dbt tests, Athena SQL checks |
| IaC | Terraform |
| Programming | Python, SQL, PySpark |
| Storage Format | CSV raw, Parquet curated |
| Monitoring | CloudWatch, Airflow logs |

---

## 7. ELT Flow

### Step 1: Generate Source Data

```bash
python data_generator/generate_mock_data.py
```

Creates:

```text
data/raw/customers.csv
data/raw/products.csv
data/raw/orders.csv
```

### Step 2: Validate Raw Data

```bash
python quality/validate_raw_orders.py
```

Checks:

- `order_id` is not null
- `order_id` is unique
- `customer_id` is not null
- `product_id` is not null
- `quantity` is within valid range
- `order_status` is valid

### Step 3: Upload Raw Data to S3

```bash
python scripts/upload_to_s3.py
```

Uploads files into the raw S3 zone.

### Step 4: Catalog Raw Data

AWS Glue Crawler scans raw S3 files and creates metadata tables in AWS Glue Data Catalog.

### Step 5: Transform Raw to Curated

AWS Glue PySpark job:

- Reads raw CSV from S3
- Removes duplicates
- Standardizes schema
- Joins orders with product price
- Calculates `order_amount`
- Adds ingestion timestamp
- Writes curated Parquet
- Partitions orders by `order_status`

### Step 6: Query with Athena

Athena queries curated Parquet directly from S3.

### Step 7: Build dbt Models

dbt creates:

- `stg_customers`
- `stg_products`
- `stg_orders`
- `dim_customers`
- `dim_products`
- `fct_orders`

### Step 8: Validate and Monitor

Validation is performed through:

- Great Expectations
- dbt tests
- Athena SQL checks
- CloudWatch logs
- Airflow task status

---

## 8. Data Model

```text
dim_customers
    customer_id PK
    first_name
    last_name
    email
    state
    signup_date

dim_products
    product_id PK
    product_name
    category
    unit_price

fct_orders
    order_id PK
    customer_id FK
    product_id FK
    order_date
    quantity
    order_status
    unit_price
    order_amount
    customer_state
    product_category
    completed_revenue
```

---

## 9. Data Quality Rules

| Rule | Tool | Purpose |
|---|---|---|
| order_id not null | Great Expectations / dbt | Prevent invalid order records |
| order_id unique | Great Expectations / dbt | Prevent duplicate transactions |
| quantity range check | Great Expectations | Catch invalid order quantities |
| accepted order statuses | Great Expectations | Enforce business values |
| order_amount not null | dbt | Ensure revenue calculation worked |
| Athena row count checks | Athena SQL | Validate final table completeness |

---

## 10. Terraform Resources

Terraform provisions:

- S3 lakehouse bucket
- S3 raw/curated/analytics prefixes
- Glue Catalog Database
- Glue Crawler
- Glue PySpark Job
- IAM role and policy for Glue
- Athena Workgroup
- CloudWatch Log Group

---

## 11. Airflow DAG

The DAG file is available at:

```text
airflow/dags/aws_lakehouse_elt_dag.py
```

DAG flow:

```text
generate_mock_data
    -> validate_raw_data
    -> upload_raw_files_to_s3
    -> run_glue_crawler
    -> run_glue_transform_job
    -> wait_for_glue_transform_job
    -> run_dbt_models
    -> run_athena_validation_queries
```

---

## 12. How to Run

### Prerequisites

Install:

- Python 3.10+
- AWS CLI
- Terraform
- dbt
- AWS account with permission for S3, Glue, IAM, Athena, CloudWatch

Configure AWS:

```bash
aws configure
```

### Local Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Environment File

Copy:

```bash
cp .env.example .env
```

Update:

```text
AWS_REGION=us-east-1
S3_BUCKET=your-unique-bucket-name
ATHENA_DATABASE=ecommerce_lakehouse
ATHENA_OUTPUT_LOCATION=s3://your-unique-bucket-name/athena-results/
```

### Deploy Infrastructure

```bash
cd terraform
terraform init
terraform plan -var="s3_bucket_name=your-unique-bucket-name"
terraform apply -var="s3_bucket_name=your-unique-bucket-name"
```

### Run Pipeline

```bash
python data_generator/generate_mock_data.py
python quality/validate_raw_orders.py
python scripts/upload_to_s3.py
```

Then run Glue crawler and Glue job from AWS Console or Airflow.

### Run dbt

```bash
cd dbt/aws_lakehouse_dbt_project
dbt debug
dbt run
dbt test
dbt docs generate
```

---

## 13. Proof of Work Screenshots

Add screenshots under:

```text
docs/screenshots/
```

Required screenshots are listed in:

```text
docs/screenshot_checklist.md
```

Minimum screenshots:

1. GitHub repository home page
2. S3 raw zone
3. S3 curated zone
4. Glue crawler success
5. Glue job success
6. Athena query output
7. dbt run output
8. dbt test output
9. Airflow DAG graph
10. CloudWatch logs

---

## 14. Recruiter Pitch

I built an AWS cloud lakehouse ELT pipeline that ingests e-commerce data into S3, catalogs it using AWS Glue, transforms it with Glue PySpark into Parquet, queries it through Athena and Redshift Spectrum, and models analytics tables using dbt. I used Airflow for orchestration, Terraform for infrastructure, Great Expectations and dbt tests for data quality, IAM for secure access, and CloudWatch for monitoring.

---

## 15. Resume Bullet

Designed and implemented an AWS cloud lakehouse ELT pipeline using Amazon S3, AWS Glue, Athena, Redshift Spectrum, Apache Airflow, dbt, Terraform, and Great Expectations to ingest, validate, transform, catalog, and query e-commerce data across raw, curated, and analytics zones.

---

## 16. Cost Warning

AWS resources can create charges. Destroy resources after testing:

```bash
cd terraform
terraform destroy -var="s3_bucket_name=your-unique-bucket-name"
```

Also manually check S3, Glue, Athena query results, and CloudWatch logs. AWS billing surprises are not a personality trait.
