resource "aws_s3_bucket" "lakehouse" {
  bucket = var.s3_bucket_name

  tags = {
    Project = var.project_name
    Layer   = "lakehouse"
  }
}

resource "aws_s3_bucket_versioning" "lakehouse_versioning" {
  bucket = aws_s3_bucket.lakehouse.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "lakehouse_encryption" {
  bucket = aws_s3_bucket.lakehouse.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_object" "raw_prefix" {
  bucket  = aws_s3_bucket.lakehouse.id
  key     = "raw/ecommerce/"
  content = ""
}

resource "aws_s3_object" "curated_prefix" {
  bucket  = aws_s3_bucket.lakehouse.id
  key     = "curated/ecommerce/"
  content = ""
}

resource "aws_s3_object" "analytics_prefix" {
  bucket  = aws_s3_bucket.lakehouse.id
  key     = "analytics/ecommerce/"
  content = ""
}

resource "aws_s3_object" "athena_results_prefix" {
  bucket  = aws_s3_bucket.lakehouse.id
  key     = "athena-results/"
  content = ""
}
