resource "aws_glue_catalog_database" "ecommerce" {
  name = var.athena_database
}

resource "aws_cloudwatch_log_group" "glue_logs" {
  name              = "/aws-glue/jobs/${var.project_name}"
  retention_in_days = 14
}

resource "aws_s3_object" "glue_job_script" {
  bucket = aws_s3_bucket.lakehouse.id
  key    = "scripts/glue/transform_raw_to_curated.py"
  source = "../glue/jobs/transform_raw_to_curated.py"
  etag   = filemd5("../glue/jobs/transform_raw_to_curated.py")
}

resource "aws_glue_crawler" "raw_crawler" {
  database_name = aws_glue_catalog_database.ecommerce.name
  name          = "ecommerce-raw-crawler"
  role          = aws_iam_role.glue_role.arn

  s3_target {
    path = "s3://${aws_s3_bucket.lakehouse.bucket}/raw/ecommerce/"
  }

  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "UPDATE_IN_DATABASE"
  }
}

resource "aws_glue_job" "raw_to_curated" {
  name     = "ecommerce-raw-to-curated-job"
  role_arn = aws_iam_role.glue_role.arn

  glue_version      = "4.0"
  worker_type       = "G.1X"
  number_of_workers = 2

  command {
    script_location = "s3://${aws_s3_bucket.lakehouse.bucket}/${aws_s3_object.glue_job_script.key}"
    python_version  = "3"
  }

  default_arguments = {
    "--job-language"                     = "python"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-metrics"                   = "true"
    "--S3_BUCKET"                        = aws_s3_bucket.lakehouse.bucket
    "--RAW_PREFIX"                       = "raw/ecommerce"
    "--CURATED_PREFIX"                   = "curated/ecommerce"
  }
}
