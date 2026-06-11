# GitHub Repository Setup

## 1. Create Repository

Recommended repository name:

```text
aws-cloud-lakehouse-elt-pipeline
```

Description:

```text
End-to-end AWS cloud lakehouse ELT pipeline using S3, Glue, Athena, Redshift Spectrum, Airflow, dbt, Terraform, Great Expectations, and CloudWatch.
```

Topics:

```text
aws
data-engineering
lakehouse
elt
s3
glue
athena
redshift
airflow
dbt
terraform
great-expectations
pyspark
```

## 2. Push Code

```bash
git init
git add .
git commit -m "Initial AWS cloud lakehouse ELT pipeline project"
git branch -M main
git remote add origin https://github.com/<your-username>/aws-cloud-lakehouse-elt-pipeline.git
git push -u origin main
```

## 3. Recommended GitHub Sections

Pin this repository on your GitHub profile.

Add it to your resume as:

```text
GitHub: https://github.com/<username>/aws-cloud-lakehouse-elt-pipeline
```

Add it to LinkedIn under Projects.

## 4. Do Not Upload

Do not upload:

- `.env`
- AWS keys
- Terraform state files
- Screenshots containing account IDs
- Billing details
- IAM secrets

The `.gitignore` already blocks common unsafe files, but do not trust automation blindly. That is how horror movies and cloud bills happen.
