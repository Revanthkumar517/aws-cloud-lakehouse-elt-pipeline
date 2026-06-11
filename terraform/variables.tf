variable "aws_region" {
  description = "AWS region for lakehouse resources."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name prefix."
  type        = string
  default     = "aws-lakehouse-elt"
}

variable "s3_bucket_name" {
  description = "Globally unique S3 bucket name."
  type        = string
}

variable "athena_database" {
  description = "Athena and Glue database name."
  type        = string
  default     = "ecommerce_lakehouse"
}
