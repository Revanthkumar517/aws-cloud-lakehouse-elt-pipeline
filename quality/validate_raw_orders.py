import os

import great_expectations as gx
import pandas as pd


ORDERS_PATH = "data/raw/orders.csv"
CUSTOMERS_PATH = "data/raw/customers.csv"
PRODUCTS_PATH = "data/raw/products.csv"


def validate_file_exists(path: str) -> None:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing input file: {path}")


def main() -> None:
    for path in [ORDERS_PATH, CUSTOMERS_PATH, PRODUCTS_PATH]:
        validate_file_exists(path)

    orders_df = pd.read_csv(ORDERS_PATH)

    # Create an ephemeral Great Expectations context.
    context = gx.get_context()

    datasource = context.sources.add_pandas(
        name="raw_orders_pandas_datasource"
    )

    data_asset = datasource.add_dataframe_asset(
        name="raw_orders_asset"
    )

    batch_request = data_asset.build_batch_request(
        dataframe=orders_df
    )

    suite_name = "raw_orders_expectation_suite"

    context.add_or_update_expectation_suite(
        expectation_suite_name=suite_name
    )

    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite_name=suite_name,
    )

    results = [
        validator.expect_column_values_to_not_be_null(
            column="order_id"
        ),
        validator.expect_column_values_to_be_unique(
            column="order_id"
        ),
        validator.expect_column_values_to_not_be_null(
            column="customer_id"
        ),
        validator.expect_column_values_to_not_be_null(
            column="product_id"
        ),
        validator.expect_column_values_to_be_between(
            column="quantity",
            min_value=1,
            max_value=10,
        ),
        validator.expect_column_values_to_be_in_set(
            column="order_status",
            value_set=[
                "completed",
                "cancelled",
                "returned",
                "pending",
            ],
        ),
    ]

    failed_results = [
        result.to_json_dict()
        for result in results
        if not result.success
    ]

    if failed_results:
        raise ValueError(
            f"Data quality validation failed: {failed_results}"
        )

    print("Great Expectations validation passed for raw orders.")


if __name__ == "__main__":
    main()