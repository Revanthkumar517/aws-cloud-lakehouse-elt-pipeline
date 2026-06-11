# Deployment Runbook

## 1. Configure AWS CLI

```bash
aws configure
```

Confirm identity:

```bash
aws sts get-caller-identity
```

## 2. Create Local Environment

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Configure Environment Variables

```bash
cp .env.example .env
```

Update the values:

```text
AWS_REGION=us-east-1
S3_BUCKET=your-unique-bucket-name
ATHENA_DATABASE=ecommerce_lakehouse
ATHENA_OUTPUT_LOCATION=s3://your-unique-bucket-name/athena-results/
```

## 4. Deploy Terraform

```bash
cd terraform
terraform init
terraform validate
terraform plan -var="s3_bucket_name=your-unique-bucket-name"
terraform apply -var="s3_bucket_name=your-unique-bucket-name"
```

## 5. Generate and Validate Data

```bash
cd ..
python data_generator/generate_mock_data.py
python quality/validate_raw_orders.py
```

## 6. Upload to S3

```bash
python scripts/upload_to_s3.py
```

## 7. Run Glue Crawler

AWS Console:

```text
AWS Glue -> Crawlers -> ecommerce-raw-crawler -> Run
```

Or AWS CLI:

```bash
aws glue start-crawler --name ecommerce-raw-crawler
```

## 8. Run Glue Job

AWS Console:

```text
AWS Glue -> ETL Jobs -> ecommerce-raw-to-curated-job -> Run
```

Or AWS CLI:

```bash
aws glue start-job-run --job-name ecommerce-raw-to-curated-job
```

## 9. Verify Curated Output

Check S3:

```text
curated/ecommerce/customers/
curated/ecommerce/products/
curated/ecommerce/orders/
```

Orders should be partitioned by:

```text
order_status=completed/
order_status=cancelled/
order_status=returned/
order_status=pending/
```

## 10. Query Athena

Run:

```sql
SELECT order_status, COUNT(*) AS order_count, SUM(order_amount) AS total_amount
FROM ecommerce_lakehouse.curated_orders
GROUP BY order_status;
```

## 11. Run dbt

```bash
cd dbt/aws_lakehouse_dbt_project
dbt debug
dbt run
dbt test
dbt docs generate
```

## 12. Capture Screenshots

Use:

```text
docs/screenshot_checklist.md
```

## 13. Cleanup

```bash
cd terraform
terraform destroy -var="s3_bucket_name=your-unique-bucket-name"
```

Then manually confirm:
- S3 bucket deleted or empty
- Glue jobs removed
- Glue crawlers removed
- Athena query results cleaned
- CloudWatch logs removed if not needed
