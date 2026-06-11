import os
import time
from typing import Callable

import boto3


AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
ATHENA_DATABASE = os.getenv("ATHENA_DATABASE", "ecommerce_lakehouse")
ATHENA_OUTPUT_LOCATION = os.getenv("ATHENA_OUTPUT_LOCATION")

if not ATHENA_OUTPUT_LOCATION:
    raise ValueError("Missing ATHENA_OUTPUT_LOCATION")


def run_scalar_query(client, query: str) -> str:
    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            "Database": ATHENA_DATABASE,
        },
        ResultConfiguration={
            "OutputLocation": ATHENA_OUTPUT_LOCATION,
        },
    )

    query_id = response["QueryExecutionId"]

    while True:
        execution = client.get_query_execution(
            QueryExecutionId=query_id
        )

        status = execution["QueryExecution"]["Status"]
        state = status["State"]

        if state == "SUCCEEDED":
            break

        if state in {"FAILED", "CANCELLED"}:
            reason = status.get(
                "StateChangeReason",
                "No failure reason returned",
            )
            raise RuntimeError(
                f"Athena query {query_id} failed: {reason}"
            )

        time.sleep(2)

    result = client.get_query_results(
        QueryExecutionId=query_id,
        MaxResults=2,
    )

    rows = result["ResultSet"]["Rows"]

    if len(rows) < 2:
        raise RuntimeError(
            f"Athena query {query_id} returned no data row"
        )

    return rows[1]["Data"][0].get("VarCharValue", "")


def validate(
    client,
    name: str,
    query: str,
    check: Callable[[str], bool],
    expected: str,
) -> None:
    print(f"Running validation: {name}")

    value = run_scalar_query(client, query)

    print(f"Result: {value}")

    if not check(value):
        raise RuntimeError(
            f"Validation failed for {name}. "
            f"Expected {expected}, received {value}"
        )

    print(f"PASSED: {name}")


def main() -> None:
    client = boto3.client(
        "athena",
        region_name=AWS_REGION,
    )

    validations = [
        (
            "fct_orders row count",
            "SELECT COUNT(*) FROM fct_orders",
            lambda value: int(value) == 3000,
            "3000 rows",
        ),
        (
            "fct_orders null order keys",
            """
            SELECT COUNT(*)
            FROM fct_orders
            WHERE order_id IS NULL
            """,
            lambda value: int(value) == 0,
            "0 null order IDs",
        ),
        (
            "dim_customers row count",
            "SELECT COUNT(*) FROM dim_customers",
            lambda value: int(value) == 500,
            "500 rows",
        ),
        (
            "dim_products row count",
            "SELECT COUNT(*) FROM dim_products",
            lambda value: int(value) == 100,
            "100 rows",
        ),
        (
            "completed revenue is positive",
            """
            SELECT COALESCE(SUM(completed_revenue), 0)
            FROM fct_orders
            """,
            lambda value: float(value) > 0,
            "positive completed revenue",
        ),
    ]

    for name, query, check, expected in validations:
        validate(
            client=client,
            name=name,
            query=query,
            check=check,
            expected=expected,
        )

    print("All Athena validations passed successfully.")


if __name__ == "__main__":
    main()