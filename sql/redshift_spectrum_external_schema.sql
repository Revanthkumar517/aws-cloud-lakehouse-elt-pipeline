-- Optional Redshift Spectrum setup.
-- Replace IAM role ARN and database name before running.

CREATE EXTERNAL SCHEMA IF NOT EXISTS spectrum_ecommerce
FROM DATA CATALOG
DATABASE 'ecommerce_lakehouse'
IAM_ROLE 'arn:aws:iam::<account-id>:role/redshift-spectrum-role'
CREATE EXTERNAL DATABASE IF NOT EXISTS;

SELECT COUNT(*)
FROM spectrum_ecommerce.curated_orders;
