output "s3_bucket_name" {
  value = aws_s3_bucket.lakehouse.bucket
}

output "glue_database_name" {
  value = aws_glue_catalog_database.ecommerce.name
}

output "glue_crawler_name" {
  value = aws_glue_crawler.raw_crawler.name
}

output "glue_job_name" {
  value = aws_glue_job.raw_to_curated.name
}

output "athena_workgroup_name" {
  value = aws_athena_workgroup.lakehouse.name
}
