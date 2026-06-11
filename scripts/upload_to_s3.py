import os
from pathlib import Path

import boto3
from dotenv import load_dotenv


load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET = os.getenv("S3_BUCKET")
RAW_PREFIX = os.getenv("RAW_PREFIX", "raw/ecommerce")

LOCAL_RAW_DIR = Path("data/raw")

if not S3_BUCKET:
    raise ValueError("Missing S3_BUCKET in .env")


def upload_file(s3_client, local_file: Path, s3_key: str):
    print(f"Uploading {local_file} -> s3://{S3_BUCKET}/{s3_key}")
    s3_client.upload_file(str(local_file), S3_BUCKET, s3_key)


def main():
    if not LOCAL_RAW_DIR.exists():
        raise FileNotFoundError("data/raw does not exist. Run data_generator/generate_mock_data.py first.")

    s3 = boto3.client("s3", region_name=AWS_REGION)

    dataset_to_file = {
        "customers": "customers.csv",
        "products": "products.csv",
        "orders": "orders.csv",
    }

    for dataset, filename in dataset_to_file.items():
        local_file = LOCAL_RAW_DIR / filename
        s3_key = f"{RAW_PREFIX}/{dataset}/{filename}"
        upload_file(s3, local_file, s3_key)

    print("Upload complete.")


if __name__ == "__main__":
    main()
