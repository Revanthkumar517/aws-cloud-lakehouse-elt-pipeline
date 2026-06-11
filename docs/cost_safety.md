# Cost Safety Notes

This project can create billable AWS resources. Do not leave resources running like a digital bonfire.

## Lower-Cost Choices

- Use S3, Glue, and Athena carefully.
- Avoid provisioning Redshift unless you really need it.
- Use small Glue worker settings for testing.
- Delete S3 data and Terraform resources after testing.
- Use Athena query limits and avoid scanning large unnecessary files.

## Cleanup

From the Terraform folder:

```bash
terraform destroy
```

Also manually verify:

- S3 bucket is empty/deleted
- Glue jobs are removed
- Crawlers are removed
- Athena query results are cleaned
- CloudWatch logs are removed if not needed
```
