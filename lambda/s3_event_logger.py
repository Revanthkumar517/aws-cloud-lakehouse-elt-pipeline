import json


def lambda_handler(event, context):
    print("Received S3 event:")
    print(json.dumps(event, indent=2))

    for record in event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        print(f"New file landed: s3://{bucket}/{key}")

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "S3 event processed successfully"})
    }
