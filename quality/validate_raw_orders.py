import os

import great_expectations as ge
import pandas as pd


ORDERS_PATH = "data/raw/orders.csv"
CUSTOMERS_PATH = "data/raw/customers.csv"
PRODUCTS_PATH = "data/raw/products.csv"


def validate_file_exists(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing input file: {path}")


def main():
    for path in [ORDERS_PATH, CUSTOMERS_PATH, PRODUCTS_PATH]:
        validate_file_exists(path)

    orders = ge.from_pandas(pd.read_csv(ORDERS_PATH))

    results = []
    results.append(orders.expect_column_values_to_not_be_null("order_id"))
    results.append(orders.expect_column_values_to_be_unique("order_id"))
    results.append(orders.expect_column_values_to_not_be_null("customer_id"))
    results.append(orders.expect_column_values_to_not_be_null("product_id"))
    results.append(orders.expect_column_values_to_be_between("quantity", min_value=1, max_value=10))
    results.append(
        orders.expect_column_values_to_be_in_set(
            "order_status",
            ["completed", "cancelled", "returned", "pending"],
        )
    )

    failed = [result for result in results if not result["success"]]

    if failed:
        raise ValueError(f"Data quality validation failed: {failed}")

    print("Great Expectations validation passed for raw orders.")


if __name__ == "__main__":
    main()
