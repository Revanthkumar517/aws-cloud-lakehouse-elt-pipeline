# Screenshot Checklist for Recruiters

Screenshots matter because anyone can write “built AWS pipeline” on a resume. Screenshots prove you did not simply summon buzzwords from the cloud swamp.

Create a folder:

```text
docs/screenshots/
```

Add these screenshots before pushing to GitHub.

## Required Screenshots

### 1. GitHub Repository Home
Show:
- Project name
- README visible
- Clean folder structure

Filename:

```text
01_github_repo_home.png
```

### 2. Local Project Run
Show terminal output for:

```bash
python data_generator/generate_mock_data.py
python quality/validate_raw_orders.py
```

Filename:

```text
02_local_data_generation_validation.png
```

### 3. S3 Raw Zone
Show:

```text
s3://bucket/raw/ecommerce/customers/
s3://bucket/raw/ecommerce/products/
s3://bucket/raw/ecommerce/orders/
```

Filename:

```text
03_s3_raw_zone.png
```

### 4. Glue Crawler Success
Show:
- Crawler name
- Status succeeded
- Database name

Filename:

```text
04_glue_crawler_success.png
```

### 5. Glue Data Catalog Tables
Show:
- Raw or curated tables registered in Glue Data Catalog

Filename:

```text
05_glue_catalog_tables.png
```

### 6. Glue Job Success
Show:
- Job name
- Run status succeeded
- Duration
- Logs link if visible

Filename:

```text
06_glue_job_success.png
```

### 7. S3 Curated Zone
Show:
- Parquet output folders
- Orders partitioned by `order_status`

Filename:

```text
07_s3_curated_zone.png
```

### 8. Athena Query Result
Run:

```sql
SELECT order_status, COUNT(*) AS order_count, SUM(order_amount) AS total_amount
FROM ecommerce_lakehouse.curated_orders
GROUP BY order_status;
```

Filename:

```text
08_athena_query_result.png
```

### 9. dbt Run
Show terminal output:

```bash
dbt run
```

Filename:

```text
09_dbt_run_success.png
```

### 10. dbt Test
Show terminal output:

```bash
dbt test
```

Filename:

```text
10_dbt_test_success.png
```

### 11. Airflow DAG
Show:
- DAG graph view
- Green completed tasks

Filename:

```text
11_airflow_dag_success.png
```

### 12. CloudWatch Logs
Show:
- Glue job log stream
- Successful job logs

Filename:

```text
12_cloudwatch_logs.png
```

## Optional Strong Screenshots

- Terraform apply success
- Athena workgroup
- IAM role attached to Glue
- Redshift Spectrum external schema query
- dbt docs lineage graph
- Cost Explorer showing low spend after cleanup
